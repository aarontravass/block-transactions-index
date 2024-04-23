import json

import requests
import sys

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from database import createEngine
from models import Base, Block, Transaction

from urllib.parse import urlparse


def isUrl(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def getBlocks(jsonRpcEndpoint: str, engine: Engine, blockRange: list[int]):
    blocks: list[Block] = []
    # we loop through each block number
    for blockNumber in range(blockRange[0], blockRange[1] + 1):
        # since we query by hex, we convert the block number into a hex string
        blockNumberinHex = hex(blockNumber)
        body = json.dumps({
            "method": "eth_getBlockByNumber",
            "params": [blockNumberinHex, True],
            "id": 1,
            "jsonrpc": "2.0"
        })
        # make the request
        result = requests.post(jsonRpcEndpoint, data=body, headers={"Content-Type": "application/json"})
        jsonRes = result.json()
        # check the status code
        if (result.status_code == 200 and jsonRes):

            blockObject: dict = jsonRes.get('result')

            block: Block = {}
            block['blockNumber'] = blockNumberinHex
            block['hash'] = blockObject.get('hash')
            blockTransactions = []
            for tx in blockObject.get('transactions'):
                transaction = Transaction(
                    txHash=tx.get('hash'),
                    value=tx.get('value'),
                    toAddress=tx.get('to'),
                    fromAddress=tx.get('from'),
                    blockNumber=blockNumberinHex
                )
                blockTransactions.append(transaction)
            block = Block(
                blockNumber=blockNumberinHex,
                hash=blockObject.get('hash'),
                timestamp=int(blockObject.get('timestamp'), 0) * 1000,
                transactions=blockTransactions
            )
            blocks.append(block)
        with Session(engine) as session:
            # persist the blocks to the database
            session.add_all(blocks)
            session.commit()
        print("Done with block: " + str(blockNumber))


def createModels(engine: Engine):
    Base.metadata.create_all(engine)


"""
Main function
"""


def main():
    # read system args from the commandline
    args = sys.argv[1:]
    if len(args) != 3:
        raise Exception("3 Args should be provided")
    jsonRpcEndpoint = args[0]
    # verify URL
    if not isUrl(jsonRpcEndpoint):
        raise Exception("Invalid URL")
    dbAddress = args[1]
    if 'postgresql' not in dbAddress:
        raise Exception('PostgreSQL is the supported DB. Use the provided connection string')
    blockRange = list(map(int, args[2].split('-')))
    print(blockRange)
    if blockRange[0] > blockRange[1]:
        raise ValueError("Block Range should be positive")
    # create the database engine to use.
    # here we use postgres as the engine
    engine = createEngine(dbAddress)
    # create models if they do not exist
    createModels(engine)
    # get blocks
    getBlocks(jsonRpcEndpoint, engine, blockRange)


main()

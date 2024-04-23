import json

import requests
import sys

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from database import createEngine
from models import Base, Block, Transaction


def runArgs(jsonRpcEndpoint: str, engine: Engine, blockRange: list[int]):
    blocks: list[Block] = []
    for blockNumber in range(blockRange[0], blockRange[1] + 1):
        blockNumberinHex = hex(blockNumber)
        body = json.dumps({
            "method": "eth_getBlockByNumber",
            "params": [blockNumberinHex, True],
            "id": 1,
            "jsonrpc": "2.0"
        })
        result = requests.post(jsonRpcEndpoint, data=body, headers={"Content-Type": "application/json"})
        blockObject: dict = result.json()
        if (blockObject):
            blockObject: dict = blockObject.get('result')

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
                timestamp=int(blockObject.get('timestamp'), 0)*1000,
                transactions=blockTransactions
            )
            blocks.append(block)
        with Session(engine) as session:
            session.add_all(blocks)
            session.commit()
        print("Done with block: " + str(blockNumber))


def createModels(engine: Engine):
    Base.metadata.create_all(engine)


def main():
    args = sys.argv[1:]
    jsonRpcEndpoint = args[0]
    dbAddress = args[1]
    blockRange = list(map(int, args[2].split('-')))

    engine = createEngine(dbAddress)
    createModels(engine)
    runArgs(jsonRpcEndpoint, engine, blockRange)


main();

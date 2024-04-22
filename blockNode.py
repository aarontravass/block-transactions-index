import requests
import sys

args = sys.argv[1:]


def main(args: str):
    jsonRpcEndpoint = args[0]
    db = args[1]
    blockRange = list(map(int, args[2].split('-')))

    for blockNumber in range(blockRange[0], blockRange[1] + 1):
        blockNumberinHex = hex(blockNumber)
        body = {
            "method": "eth_getBlockByNumber",
            "params": [blockNumberinHex, 'true'],
            "id": 1,
            "jsonrpc": "2.0"
        }
        result = requests.post(jsonRpcEndpoint, data=body, headers="Content-Type: application/json")
        blockObject = result.json()
        if(blockObject):
            

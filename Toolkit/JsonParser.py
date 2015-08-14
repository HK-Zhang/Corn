import json
from pprint import pprint
import sys

def jsonReader():
    with open(r"F:\PY\data\pokemon.json") as f:
        str=f.read()
        for i in range(0,32):
            str = str.replace(chr(i),'')
        data = json.loads(str)
    pprint(data)


if __name__ == "__main__":
    jsonReader()
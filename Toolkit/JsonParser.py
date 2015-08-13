import json
from pprint import pprint
import sys

def jsonReader():
    with open(r"F:\PY\data\pokemon.json") as f:
        data = json.loads(f.read())
    pprint(data)


if __name__ == "__main__":
    jsonReader()
import json
import csv
from pprint import pprint

typePokemen = {}

with open(r"F:\PY\data\pokemon.json") as f:
    strc=f.read()
    for i in range(0,32):
        strc = strc.replace(chr(i),'')
    data = json.loads(strc)

for line in data:
    if line["type"] not in typePokemen:
        typePokemen[line["type"]] = 1
    else:
        typePokemen[line["type"]] = 1 +  typePokemen.get(line["type"])

with open(r"F:\PY\data\sumPokemon.csv",'wb') as a:
    w = csv.writer(a)

    for key, value in sorted(typePokemen.items(),key=lambda x: x[1]):
        w.writerow([key.strip(),str(value)])

pprint(typePokemen)
    


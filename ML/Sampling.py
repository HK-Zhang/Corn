import sys
import csv
import random

def main():
    with open(r'F:\PY\data\spamset.csv') as f:
        ds = list(csv.reader(f,delimiter=','))
    trainSetIx = stratifiedSampling(ds,1,0.8)


    with open(r'F:\PY\data\trainging.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in trainSetIx:
            writer.writerow(ds[i])
            ds[i] = 0

    with open(r'F:\PY\data\test.csv', 'wb') as f:
        writer = csv.writer(f)
        [writer.writerow(ds[i]) for i in range(len(ds)) if ds[i]!= 0]
                
                
def stratifiedSampling(ds,stratifiedCol,splitPercent):
    stratifiedInx = {}

    for i in range(len(ds)):
        if stratifiedInx.has_key(ds[i][stratifiedCol]):
            stratifiedInx[ds[i][stratifiedCol]].append(i)
        else:
            stratifiedInx[ds[i][stratifiedCol]]=[]
            stratifiedInx[ds[i][stratifiedCol]].append(i)

    trainSetIndex=[];
    
    for i in stratifiedInx:
            trainSetIndex.extend(random.sample(stratifiedInx[i],int(splitPercent*len(stratifiedInx[i]))))
    
    return trainSetIndex


if __name__ == "__main__":
    main()
import os
import sys
import time

def main():
    with open(r'F:\PY\data\spamset.csv','a') as out:
        files = os.listdir(r'F:\PY\data\spam')
        i=0
        sys.stdout.write("Spam files: ")
        for fname in files:
            with open(r'F:\PY\data\spam\\'+fname) as f:
                data = f.readlines()
                for line in data:
                    if line.startswith('Subject:'):
                        line=line.replace(',',' ')
                        printCount(i)
                        i=i+1
                        out.write('{0},{1} \n'.format(line[8:-1],'spam'))
        files = os.listdir(r'F:\PY\data\easy_ham')
        sys.stdout.write("\n Non Spam files: ")
        i=0
        for fname in files:
            with open(r'F:\PY\data\easy_ham\\'+fname) as f:
                data = f.readlines()
                for line in data:
                    if line.startswith('Subject:'):
                        line=line.replace(',',' ')
                        printCount(i)
                        i=i+1
                        out.write('{0},{1} \n'.format(line[8:-1],'nospam'))

def printCount(cnt):
    sys.stdout.write("\b"*len(str(cnt)))
    sys.stdout.write(str(cnt+1))

if __name__ == "__main__":
    main()
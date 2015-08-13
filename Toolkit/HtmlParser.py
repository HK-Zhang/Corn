from bs4 import BeautifulSoup
import urllib
from time import sleep
from datetime import datetime
import sys

def getGoldPrice():
    url = "http://gold.hexun.com/hjxh/"
    req = urllib.urlopen(url)
    page = req.read()
    scraping = BeautifulSoup(page,"lxml")
    price =scraping.findAll("span",attrs={"id":"newprice"})[0].text
    return price

def goldPriceDemo():
    with open(r'F:\PY\data\goldPrice.txt','w') as f:
        for i in range(0,5):
            sNow = datetime.now().strftime('%I:%M:%S%p')
            price = getGoldPrice()
            f.write("{0},{1} \n ".format(sNow,price))
            sleep(50)


if __name__ == "__main__":
    goldPriceDemo()
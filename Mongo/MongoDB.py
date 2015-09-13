import pymongo
from pymongo import MongoClient
import sys
import json

client = MongoClient('mongodb://192.168.230.129:27017/')
def mongoDemo():

    #client.the_database.authenticate('root', '001111', mechanism='SCRAM-SHA-1')


    db = client.test   
    collection = db.mycol
    count = collection.count()

    print "The number of documents you have in this collection is:", count

    for item in collection.find():
        print item

    monster = {"name": "Dracula",
               "occupation": "Blood Sucker",
               "tags": ["vampire", "teeth", "bat"],
               "date":"19981010"
               }

    monster_id = collection.insert(monster)
    print monster_id
    print collection.find_one({"name": "Dracula"})

def loadDataToMongodb():
    db = client.Corpus
    tweets = db.tweets
    with open(r'F:\PY\data\testdata.txt') as f:
        data = json.loads(f.read())
        for tweet in data["rows"]:
            tweets.insert(tweet)

def groupBy():
    db = client.Corpus
    tweets = db.tweets

    #categories = tweets.group(key ={"sentiment":1}, condition = {}, initial = {"count":0},reduce = "function(obj,prev) {prev.count++;}")
    categories = tweets.group(key ={"sentiment":1}, condition = {"via":"kindle2"}, initial = {"count":0},reduce = "function(obj,prev) {prev.count++;}")

    for doc in categories:
        print doc

def aggregateBy():
    db = client.Corpus
    tweets = db.tweets
    results = tweets.aggregate([{"$group":{"_id":"$sentiment","count":{"$sum":1}}}])

    for doc in results:
        print doc

def pipelineBy():
    db = client.Corpus
    tweets = db.tweets
    results = tweets.aggregate([{"$group":{"_id":"$via","count":{"$sum":1}}},
                                {"$sort":{"via":1}},
                                {"$limit":10}])
    for doc in results:
        print doc


def aggregateAdvBy():
    db = client.Corpus
    tweets = db.tweets
    results = tweets.aggregate([{"$group":{"_id":"$via","count":{"$sum":1},"avgId":{"$avg":"$id"},"maxId":{"$max":"$id"},"minId":{"$min":"$id"}}}])

    for doc in results:
        print doc
    
                   
def main():
    #groupBy()
    #aggregateBy()
    #pipelineBy()
    aggregateAdvBy()

if __name__ == "__main__":
    main()
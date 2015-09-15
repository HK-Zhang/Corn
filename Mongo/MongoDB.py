import pymongo
from pymongo import MongoClient
from bson.code import Code
import random as ran
import sys
import csv
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
    
def mapReduce():
    db = client.Corpus
    tweets = db.tweets
    map = Code("function() {emit(this.via,1);}")
    reduce = Code("""function(key, values) { 
                        var res=0;
                        values.forEach(function(v){res +=1})
                        return {count: res};
                        }""")

    result = tweets.map_reduce(map,reduce,"via_count",query={"sentiment":2},limit =10)
    print result

    for doc in db.via_count.find():
        print(doc)
 
def insertData():
    db = client.test
    games = db.games
    players = ["LeBron James",
           "Allen Iverson",
           "Kobe Bryant",
           "Rick Barry",
           "Dominique Wilkins",
           "George Gervin",
           "Dwyane Wade",
           "Jerry West",
           "Pete Maravich",
           "Carmelo Anthony"]
    for x in range(100):
        games.insert({"player":players[ran.randint(0,9)],
                      "points":ran.randint(0,100)})
 
def aggregateMR():
    db = client.test
    games = db.games
    map = Code("function() {emit(this.player,this.points);}")
    reduce = Code("""function(key, values) { 
                        var explain={total:Array.sum(values),
                                    max:Math.max.apply(Math,values),
                                    min:Math.min.apply(Math,values),
                                    avg:Array.sum(values)/values.length}
                        return explain;
                        }""")
    result = games.map_reduce(map,reduce,"_result")
    print(result)
    for p in db["_result"].find():
        print(p)            
 
def wordCloud():
    db = client.Corpus
    tweets = db.tweets
    map = Code("""function() {
                    this.text.split(' ').forEach(
                        function(word){
                            var txt = word.toLowerCase();
                            if(!(/^@/).test(txt) && txt.length > 3 && !(/^http/).test(txt)){
                            emit(txt,1)
                            }
                        }
                    )
    }""")

    reduce = Code("""function(key,values){
                        var res = 0;
                        values.forEach(function(v){res +=1 })
                        return {count: res};
    }""")

    result = tweets.map_reduce(map,reduce,"TweetWords",query = {"sentiment":4})
    with open(r"F:\PY\data\tweetsData.csv","wb") as f:
        f_csv = csv.writer(f,delimiter = ',')
        f_csv.writerow(["text","size"])

        for doc in db.TweetWords.find().sort("value",direction = -1).limit(50):
            f_csv.writerow([doc["_id"],doc["value"]["count"]+30])
            print doc
          
                  
def main():
    #groupBy()
    #aggregateBy()
    #pipelineBy()
    #aggregateAdvBy()
    #mapReduce()
    #insertData()
    #aggregateMR()
    wordCloud()

if __name__ == "__main__":
    main()
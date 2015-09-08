import sys
import nltk


def getData():
    def bagOfWords(tweets):
        wordsList = []
        for (words, sentiment) in tweets:
            wordsList.extend(words)
        return wordsList

    def wordFeatures(wordList):
        wordList = nltk.FreqDist(wordList)
        wordFeatures = wordList.keys()
        return wordFeatures
    
    def getFeatures(doc):
        docWords = set(doc)
        feat = {}
        for word in wordFeatures:
            feat['contains(%s)' % word] = (word in docWords)
        return feat

    lists=[line.strip().split(',') for line in open(r'F:\PY\data\testdata.manual.2009.06.14.csv','r').readlines()]
    negativeTweets = [(l[5][1:-1],'negative') for l in lists if l[0]=='"2"']
    positiveTweets = [(l[5][1:-1],'positive') for l in lists if l[0]=='"4"']
    
    tweets = []
    for (words,sentiment) in positiveTweets + negativeTweets:
        wordsFiltered = [e.lower() for e in nltk.word_tokenize(words) if len(e) >=3]
        tweets.append((wordsFiltered,sentiment))

    wordFeatures = wordFeatures(bagOfWords(tweets))
    training_set = nltk.classify.apply_features(getFeatures, tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    txt='Busy day ahead of me. Also just remebered that I left peah slices in the fridge at work on Friday.'
    print("Tweet: {0} \n Sentiment: {1} \n".format(txt, classifier.classify(getFeatures(txt))))
    #classifier.classify(getFeatures('Busy day ahead of me. Also just remebered that I left peah slices in the fridge at work on Friday.'))
    
    #print(classifier.show_most_informative_features(32))






def main():
    getData()
    #print nltk.word_tokenize('Busy day ahead of me. Also just remebered that I left peah slices in the fridge at work on Friday.')

if __name__ == "__main__":
    main()

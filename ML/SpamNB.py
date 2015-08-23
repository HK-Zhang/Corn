import csv
import sys
import random

def main():
    with open(r'F:\PY\data\trainging.csv') as f:
        subjects = dict(csv.reader(f,delimiter=','))
    words,categories,texts,c_tot_words = training(subjects)
    clase = classifier('Low Cost Easy to Use Conferencing',words,categories,texts,c_tot_words)
    print("Result: {0}".format(clase))

    with open(r'F:\PY\data\test.csv') as f:
        correct = 0;
        tests = csv.reader(f,delimiter=',')
        for subject in tests:
            clase = classifier(subject[0],words,categories,texts,c_tot_words)
            if clase[0] == subject[1]:
                correct +=1
        print("Efficiency {0} of 1315".format(correct))


def list_words(text):
    words=[]
    words_tmp = text.lower().split()
    for w in words_tmp:
        if w not in words and len(w)>3:
            words.append(w)
    return words

def training(texts):
    c_words ={}
    c_categories = {}
    c_texts =0
    c_total_words = {}

    for t in texts:
        c_texts = c_texts+1

        if texts[t] not in c_categories:
            c_categories[texts[t]] =1
            c_total_words[texts[t]] = 0
        else:
            c_categories[texts[t]] =c_categories[texts[t]]+1

    for t in texts:
        words = list_words(t)

        for p in words:
            if p not in c_words:
                c_words[p] ={}

                for c in c_categories:
                    c_words[p][c]=0
            c_words[p][texts[t]] = c_words[p][texts[t]] + 1
            c_total_words[texts[t]] = c_total_words[texts[t]] + 1

    return (c_words, c_categories, c_texts,c_total_words)

def classifier(subject_line,c_words,c_categories,c_text,c_tot_words):
    category = ''
    category_prob = 0
    for c in c_categories:
        prob_c = float(c_categories[c])/float(c_text)
        words = list_words(subject_line)
        prob_total_c = prob_c

        for p in words:
            if p in c_words:
                prob_total_c = float(c_words[p][c])/float(c_tot_words[c])*prob_total_c

        if category_prob < prob_total_c:
            category = c
            category_prob = prob_total_c

    return (category, category_prob)



if __name__ == "__main__":
    main()
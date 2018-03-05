__author__ = 'Avik'

import re,nltk
#from nltk.tokenize import RegexpTokenizer
#from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
import gensim
import os
import csv

tag_to_type = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV}

def get_wordnet_pos(treebank_tag):
    return tag_to_type.get(treebank_tag[:1], wordnet.NOUN)

class Corpus:
    def __init__(self):
        self.texts = []

    def readData(self,inputdir):
        for root,dirs,files in os.walk(inputdir,topdown=False):
            fileCount = 0
            avgSpam = []
            for name in files:
                fileCount += 1
                #if fileCount > 3:
                print "filename: ",name
                with open(os.path.join(root,name),'r') as f:
                    spamCount = 0
                    reader = csv.reader(f)
                    next(reader,None)
                    rowCount = 1
                    for row in reader:
                        rowCount += 1
                        try:
                            doc = row[10]
                        except:
                            continue

                        if len(doc) > 300:
                            self.writeCleanData('../FixedHeader',name,row)
                        else:
                            spamCount += 1
                        #print doc
                        #raw_input()
                        print rowCount, name
                        if rowCount > 1000:
                            break
                    avgSpam.append(spamCount)

        avgSpam = sum(avgSpam)/float(len(avgSpam))
        print avgSpam
        #raw_input()


    def writeCleanData(self,outputdir,filename,data):
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        with open(os.path.join(outputdir,filename),'a+') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows([data])
            #f.write(data)


    def parseData(self,inputdir):
        for root,dirs,files in os.walk(inputdir,topdown=False):
            print root
            fileCount = 0
            for name in files:
                fileCount += 1
                print "filename: ",name
                with open(os.path.join(root,name),'r') as f:
                    reader = csv.reader(f)
                    next(reader,None)
                    rowCount = 1
                    for row in reader:
                        rowCount += 1
                        doc = row[10]
                        #print rowCount, name
                        self.texts.append(self.cleanData(doc))
                        if rowCount > 10:
                            break
        #return self.texts
        self.HDP()


    def cleanData(self,doc):
        shortword = re.compile(r'\W*\b\w{1,2}\b')
        nonan = re.compile(r'[^a-zA-Z ]')
        stop = stopwords.words('english') + ['paper','system','problem','author']
        lmtzr = WordNetLemmatizer()

        tag_to_type = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV}

        tokens = nltk.word_tokenize(shortword.sub('',nonan.sub('',doc.lower())))

        tokens = [token for token in tokens if not token in stop]
        tags = nltk.pos_tag(tokens)

        finalTokens = []
        for word, tag in zip(tokens, tags):
            finalTokens.append(lmtzr.lemmatize(word, get_wordnet_pos(tag[1])))

        #print ' '.join(finalTokens)
        return finalTokens

    def HDP(self):
        print len(self.texts)
        dictionary = corpora.Dictionary(self.texts)
        #print dictionary.token2id
        docTermMat = [dictionary.doc2bow(text) for text in self.texts]
        #print docTermMat
        hdp = gensim.models.hdpmodel.HdpModel(docTermMat,id2word = dictionary)
        topics = hdp.print_topics(topics=-1, topn=5)

        for i in topics:
            print i
        #hdp.save(fname='model_hdp.txt')


def main():
    corpus = Corpus()
    #corpus.readData('../CompleteAndFixedHeader')
    corpus.parseData('../FixedHeader')
    #corpus.LDA(texts)

if __name__ == '__main__':
    main()

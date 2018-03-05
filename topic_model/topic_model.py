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
import matplotlib as plt

tag_to_type = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV}

def get_wordnet_pos(treebank_tag):
    return tag_to_type.get(treebank_tag[:1], wordnet.NOUN)

def cleanData(doc):
    shortword = re.compile(r'\W*\b\w{1,3}\b')
    nonan = re.compile(r'[^a-zA-Z ]')
    #tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words('english') + ['paper','system']
    #stemmer = PorterStemmer()
    lmtzr = WordNetLemmatizer()

    tag_to_type = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV}

    #doc = doc.lower()
    tokens = nltk.word_tokenize(shortword.sub('',nonan.sub('',doc.lower())))

    #tokens = tokenizer.tokenize(doc)
    tokens = [token for token in tokens if not token in stop]
    #print tokens
    #raw_input()
    tags = nltk.pos_tag(tokens)
    #print tags
    #raw_input()

    finalTokens = []
    for word, tag in zip(tokens, tags):
        finalTokens.append(lmtzr.lemmatize(word, get_wordnet_pos(tag[1])))

    #print ' '.join(finalTokens)
    return finalTokens

    #tokens = [stemmer.stem(token) for token in tokens]
    '''
    stemmed_tokens = []
    new_tokens = []
    for token in tokens:
        try:
            stemmed_tokens.append(stemmer.stem(token))
            new_tokens.append(token)
        except:
            continue

    #print tokens,'\n'
    #print stemmed_tokens
    #raw_input()

    return stemmed_tokens
    #return new_tokens
    '''


def plot(model):
    print model


def parseData(inputdir):
    texts = []
    for root,dirs,files in os.walk(inputdir,topdown=False):
        print root
        fileCount = 0
        for name in files:
            fileCount += 1
            #if fileCount > 3:
            #    return texts
            print "filename: ",name
            with open(os.path.join(root,name),'r') as f:
                reader = csv.reader(f)
                next(reader,None)
                rowCount = 1
                for row in reader:
                    rowCount += 1
                    doc = row[10]
                    print len(doc.strip())
                    print doc,'\n'
                    raw_input()
                    #print rowCount, name
                    texts.append(cleanData(doc))
                    if rowCount > 100:
                        break

    return texts


def readLDA():
    #print docTermMat

    #ldamodel = gensim.models.ldamodel.LdaModel(docTermMat, num_topics=10, id2word = dictionary, passes=20)
    #ldamodel = gensim.models.ldamulticore.LdaMulticore(docTermMat, num_topics=20, workers=3, id2word = dictionary, passes=20)

    ldamodel = gensim.models.ldamodel.LdaModel.load('model.txt')

    print '\n'
    for i in range(20):
        print ldamodel.show_topic(i,topn=5)

    docProbMat = ldamodel.get_document_topics(docTermMat)
    print len(docProbMat)
    print docProbMat[0],'\n'
    #print ldamodel[docTermMat[199]]


    #print ldamodel.top_topics(docTermMat,num_words=10)

    #for i in ldamodel.print_topics(num_topics=10, num_words=10):
    #    print i
    #for i in range(10):
    #    print ldamodel.get_topic_terms(i)
    #    print ldamodel.print_topic(i)
    #ldamodel.save(fname='model.txt')
    return ldamodel

def LDA(texts):
    dictionary = corpora.Dictionary(texts)
    #print dictionary.token2id

    docTermMat = [dictionary.doc2bow(text) for text in texts]
    #print docTermMat

    #ldamodel = gensim.models.ldamodel.LdaModel(docTermMat, num_topics=10, id2word = dictionary, passes=20)
    #ldamodel = gensim.models.ldamulticore.LdaMulticore(docTermMat, num_topics=20, workers=3, id2word = dictionary, passes=20)

    ldamodel = gensim.models.ldamodel.LdaModel.load('model.txt')

    print '\n'
    for i in range(20):
        show_topic = ldamodel.show_topic(i,topn=5)
        print show_topic,'\n'

    docProbMat = ldamodel.get_document_topics(docTermMat)
    print docProbMat[0],'\n'
    print len(docProbMat)
    print ldamodel[docTermMat[199]]


    #print ldamodel.top_topics(docTermMat,num_words=10)

    #for i in ldamodel.print_topics(num_topics=10, num_words=10):
    #    print i
    #for i in range(10):
    #    print ldamodel.get_topic_terms(i)
    #    print ldamodel.print_topic(i)
    #ldamodel.save(fname='model.txt')
    return ldamodel


def main():
    texts = parseData('../CompleteAndFixedHeader')
    model = LDA(texts)
    #model = readLDA()
    plot(model)


if __name__ == '__main__':
    main()

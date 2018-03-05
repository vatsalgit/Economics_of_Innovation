__author__ = 'Avik'

import os
import csv
import re, nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from gensim import corpora
from os.path import expanduser
#from nltk.tag.senna import SennaTagger

home = expanduser("~")
tag_to_type = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV}

def get_wordnet_pos(treebank_tag):
    #print treebank_tag[:1], wordnet.NOUN
    return tag_to_type.get(treebank_tag[:1], wordnet.NOUN)

def readRawData(inputdir):
    '''
    Read the raw data from csv files and organize the raw data time wise.
    '''
    for root,dirs,files in os.walk(inputdir,topdown=False):
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
                    try:
                        doc = row[10]
                    except:
                        continue
                    try:
                        if re.search(r'^\d{4}$',row[5]):
                            year = row[5]
                            if len(doc) > 300:
                                writeCSV('../TimeWise',year+'.csv',row)
                    except:
                        continue
                    #if rowCount > 1000:
                    #    break

def writeCSV(outputdir,filename,data):
    '''
    Write a CSV file
    '''
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    with open(os.path.join(outputdir,filename),'a+') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows([data])


def truncateFile(filePath):
    f = open(filePath,'w')
    f.close()

def setVocab(text,fileName):
    print "setting vocab file...."
    dictionary = corpora.Dictionary(text)
    word_id = dictionary.token2id
    word_id = sorted(word_id.items(), key=lambda x:x[1])
    path = 'dataFiles/small/vocab'+fileName+'.txt'
    truncateFile(path)
    with open(path,'a') as f:
        for pair in word_id:
            f.write(pair[0] + '\n')



def parseData(inputdir):
    #texts = []
    texts = {}
    docLength = []
    for root,dirs,files in os.walk(inputdir,topdown=False):
        fileCount = 0
        for name in files:
            #print name
            if int(name.split('.')[0]) >= 2000:
                continue

            fileCount += 1
            #if fileCount > 3:
            #    break

            print "filename: ",name

            with open(os.path.join(root,name),'r') as f:
                reader = csv.reader(f)
                #next(reader,None)
                rowCount = 0
                name = name.split('.')[0]
                texts[name] = []
                for row in reader:
                    rowCount += 1
                    if (rowCount % 100 == 0):
                        print rowCount
                    if rowCount > 10000:
                        break
                    doc = row[10] + ' 3-d'
                    #print len(doc.strip())
                    #print doc,'\n'
                    #raw_input()
                    #print rowCount, name
                    #print "\noriginal:",doc,'\n'
                    doc,length = cleanData(doc)
                    #print "cleaned:",doc
                    #raw_input()
                    texts[name].append(doc)
                    docLength.append(length)

            #setVocab(texts[name],name)
            #createLDA_C_File(texts[name],name,docLength)


def writeAbstracts(inputdir):

    def writeFile(fileName,data):
        with open(fileName,'a+') as fp:
            fp.write(data + '\n')

    for root,dirs,files in os.walk(inputdir,topdown=False):
        fileCount = 0
        for name in files:
            #print name
            if int(name.split('.')[0]) != 2000:
                continue

            fileCount += 1
            #if fileCount > 3:
            #    break

            print "filename: ",name

            with open(os.path.join(root,name),'r') as f:
                reader = csv.reader(f)
                #next(reader,None)
                rowCount = 0
                name = name.split('.')[0]
                for row in reader:
                    rowCount += 1
                    if (rowCount % 100 == 0):
                        print rowCount
                    if rowCount > 10000:
                        break
                    doc = row[10]
                    writeFile('Abstracts/' + name + '.dat',doc)




def cleanData(doc):
    '''
    Perform stop word removal, lemmatization and other preprocessing steps.
    Return tokens.
    '''
    #print "cleaning data...."
    shortword = re.compile(r'\W*\b')
    nonan = re.compile(r'[^-3a-zA-Z ]')
    stop = stopwords.words('english') + ['paper','system']
    lmtzr = WordNetLemmatizer()
    #tagger = SennaTagger(home+'/senna')

    tag_to_type = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV}

    tokens = nltk.word_tokenize(nonan.sub('',doc.lower()))
    #tokens = nltk.word_tokenize(shortword.sub('',nonan.sub('',doc.lower())))
    #print "tokens:",tokens
    tokens = [token for token in tokens if not token in stop]

    #raw_input()

    tags = nltk.pos_tag(tokens)
    #print tags
    #tags = tagger.tag(tokens)
    #print '\n',tags
    #raw_input()

    #t = nltk.pos_tag(['kinect-device'])
    #print t
    #print lmtzr.lemmatize('kinect-device',get_wordnet_pos(t[0][1]))
    #print tags
    #raw_input()

    finalTokens = []
    uniqueTokens = set()
    for word, tag in zip(tokens, tags):
        #print word,tag
        #raw_input()
        token = lmtzr.lemmatize(word, get_wordnet_pos(tag[1]))
        #token = lmtzr.lemmatize(word)
        try:
            num = int(token)
            #print '\n',num,'\n'
            continue
        except:
            {}
        if len(token) < 2:
            continue
        finalTokens.append(token.strip('-'))
        uniqueTokens.add(token.strip('-'))

    #print ' '.join(finalTokens)
    return finalTokens, len(uniqueTokens)



def createLDA_C_File(texts,fileName,lengths):
    print "creating .dat file...."
    dictionary = corpora.Dictionary(texts)
    docTermMat = [dictionary.doc2bow(text) for text in texts]
    print len(docTermMat)

    #for i in range(len(docTermMat)):
    #    print docTermMat[i]
    #    print texts[i]
    #    print lengths[i],'\n'
    #raw_input()

    path = 'dataFiles/small/' + fileName + '.dat'
    truncateFile(path)
    with open(path,'a+') as f:
        for i in xrange(len(texts)):
            f.write(str(lengths[i]) + ' ')
            for j in xrange(len(docTermMat[i])):
                f.write(str(docTermMat[i][j][0]) + ':' + str(docTermMat[i][j][1]) + ' ')
            f.write('\n')

def main():
    #readRawData('../CompleteAndFixedHeader')
    parseData('../TimeWise')
    #writeAbstracts('../TimeWise')
    #print texts[0]
    #createLDA_C_File(texts)


if __name__ == '__main__':
    main()

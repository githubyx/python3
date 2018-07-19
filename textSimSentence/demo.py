#coding=utf-8
import jieba.posseg as pseg
import jieba
import datetime
import re
from gensim import corpora, models, similarities
import numpy as np

#实现句子相似度比较 相似度存在list中
#实现查询某个句子的相似度最高的另一个句子
def  test():
    fileTemp="a.b?c!你。好？吗".decode("utf-8")
    sentence=re.split(u"[.?!。？！]",fileTemp)
    print sentence


def getSentence(filename):
    result = []
    with open(filename) as f:
        fileTemp = f.read()
        fileText = fileTemp.replace(' ', '').replace('\n', '').replace('“', '').replace('”', '')
        f=fileText.decode("utf-8")
        sentence = re.split(u"[.?!。？！]", f)
        return sentence[:-1]

#分词 二维 一维为句子的分词
def senmentSentence(filename):
    result=[]
    with open(filename) as f:
        fileTemp = f.read()
        fileText=fileTemp.replace(' ','').replace(r'\n', '').replace('，', '').replace('“', '').replace('”', '').replace('、', '').replace('|', '')
        a=jieba.cut(fileText)
        b='|'.join(a)
        #sentence=b.split(u'。')
        sentence=re.split(u"[.?!。？！]", b)
        # print sentence[0]
        for i in sentence:
            c=i.split("|")
            c2=c[1:-1]
            result.append(c2)
        return result

def countMean(fileA,fileB):
    splitfileA = senmentSentence(fileA)
    splitfileB= senmentSentence(fileB)
    dictionary = corpora.Dictionary(splitfileA,splitfileB)
    doc_vectors = [dictionary.doc2bow(text) for text in splitfileA]
    scoreList=[]
    sum=0
    index = similarities.MatrixSimilarity(doc_vectors)
    for i in splitfileB:
        location=[]
        B_bow = dictionary.doc2bow(i)
        sims = index[B_bow]
        score = np.max(sims)
        location.append(np.argmax(sims))
        location.append(score)
        scoreList.append(location)
        sum = sum + score
    length=len(splitfileB)-1#去最后一个空白句子
    print "句子长度:", length
    print "平局相似度:",sum/length
    return  scoreList[:-1],sum/length



def querySentence(i,scoreList,fileA,fileB):
    sentenceA = getSentence(fileA)
    sentenceB = getSentence(fileB)
    testLoc=scoreList[i][0]
    sims=scoreList[i][1]
    return testLoc,sentenceA[testLoc],sentenceB[i],sims

def countMeantfidf(fileA,fileB):
    splitfileA = senmentSentence(fileA)
    splitfileB= senmentSentence(fileB)
    dictionary = corpora.Dictionary(splitfileA)
    doc_vectors = [dictionary.doc2bow(text) for text in splitfileA]
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    scoreList = []
    sum = 0
    index = similarities.MatrixSimilarity(tfidf_vectors)
    for i in splitfileB:
        location = []
        B_bow = dictionary.doc2bow(i)
        testtfidf=tfidf[B_bow]
        sims = index[testtfidf]
        score = np.max(sims)
        location.append(np.argmax(sims))
        location.append(score)
        scoreList.append(location)
        sum = sum + score
    length = len(splitfileB) - 1  # 去最后一个空白句子
    print "查询句子长度", length
    print "平局相似度", sum / length
    return scoreList[:-1], sum / length

if __name__=="__main__":
    filenames = ['data/textA.txt', 'data/textA.txt']
    starttime = datetime.datetime.now()
    scoreList, mean = countMean(filenames[0], filenames[1])
    # scoreList, mean = countMeantfidf(filenames[0], filenames[1])
    print scoreList
    loc,a, b, sims = querySentence(900, scoreList, filenames[0], filenames[1])
    # a, b, sims = querySentence(2000, filenames[0], filenames[1])
    print loc,":",a," ==== ",b,"\nsimilary:",sims
    endtime = datetime.datetime.now()
    print u"消耗时间秒：",(endtime-starttime).seconds


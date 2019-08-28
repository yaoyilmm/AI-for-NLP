import  numpy as np
import logging as log

#生成实验样本
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec=[0,1,0,1,0,1] #1表示侮辱性言论，0表示正常言论
    return postingList,classVec
#构建词汇表
def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document) #取两个集合的并集
    return list(vocabSet)
#词集模型 对输入的词汇表构建词向量
def setOfWords2Vec(vocabList,inputSet):
    returnVec=np.zeros(len(vocabList)) #生成零向量的array
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1 #有单词，则该位置填充0
        else: print('the word:%s is not in my Vocabulary!'% word)
    return returnVec #返回全为0和1的向量
#词袋模型
def bagOfWords2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec #返回非负整数的词向量

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix) #文档数目
    numWord=len(trainMatrix[0]) #词汇表词数目
    print("numDocs=",numTrainDocs,"numword=",numWord)
    pAbusive=sum(trainCategory)/len(trainCategory) #p1,出现侮辱性评论的概率
    p0Num=np.zeros(numWord);p1Num=np.zeros(numWord)
    p0Demon=0;p1Demon=0
    for i in range(numTrainDocs):
        if trainCategory[i]==0:
            p0Num+=trainMatrix[i] #向量相加
            p0Demon+=sum(trainMatrix[i]) #向量中1累加求和
        else:
            p1Num+=trainMatrix[i]
            p1Demon+=sum(trainMatrix[i])
    print("p0Num=", p0Num)
    print("p0Demon=", p0Demon)
    p0Vec=p0Num/p0Demon
    p1Vec=p1Num/p1Demon
    return p0Vec,p1Vec,pAbusive

def trainNB1(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWord=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/len(trainCategory)
    p0Num=np.ones(numWord)
    p1Num=np.ones(numWord)# 初始化为1
    p0Demon=2;p1Demon=2 #初始化为
    for i in range(numTrainDocs):
        if trainCategory[i]==0:
            p0Num+=trainMatrix[i]
            p0Demon+=sum(trainMatrix[i])
        else:
            p1Num+=trainMatrix[i]
            p1Demon+=sum(trainMatrix[i])
    print("p0Num=",p0Num)
    p0Vec=log(p0Num/p0Demon) #对结果求对数
    p1Vec=log(p1Num/p1Demon) #对结果求自然对数
    return p0Vec,p1Vec,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p1Vec)+np.log(pClass1)
    p0=sum(vec2Classify*p0Vec)+np.log(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

if __name__ == '__main__':
   listPosts,listClasses=loadDataSet()
   myVocabList=createVocabList(listPosts)
   print(myVocabList)
   print(setOfWords2Vec(myVocabList,listPosts[0]))
   trainMat=[]
   for postinDoc in listPosts:
       trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
   print("trainMat=",trainMat)
   p0v,p1v,pAb = trainNB0(trainMat,listClasses)
   print("p0v=", p0v)
   print("p1v=", p1v)
   print("pAb=", pAb)
   print("p0v[19]=",p0v[19])
   print("p1v[19]=", p1v[19])
   testEntry = ['love', 'my', 'dalmation']
   thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
   print(testEntry, 'classified as:', classifyNB(thisDoc, p0v, p1v, pAb))
   testEntry = ['stupid', 'garbage']
   thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
   print(testEntry, 'classified as:', classifyNB(thisDoc, p0v, p1v, pAb))

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import  pandas as pd
import re
import numpy as np
import  jieba
import matplotlib.pyplot as plt
from collections import Counter
human = """
human = 人物 行为 事务 

人物 = 我 | 吴京 | 老师 | 男主人公

行为 = 看 | 咨询 | 买

事务 = 电影 | 电影票



"""
host = """
host = 寒暄 报数 询问 业务相关 结尾
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 吴京 | 老师 | 我
打招呼 = 你好 | 您好
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = 耍一耍 | 玩一玩 | 看电影
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？"""
grammer_pattern = {}
def generate_grammer(grammer_define,split_str,grammer_pattern):
    for line in grammer_define.split('\n'):
        if not line: continue
        key,value = line.split(split_str)
        value = value.split('|')
        key = key.strip()
        grammer_pattern[key] = value
        grammer_pattern[key] = [r.split() for r in value]
    return grammer_pattern
#dic_str = generate_grammer(host,'=',grammer_pattern)
#print(dic_str)
def generate(dicStr,target):
    if target not in dicStr:
        return target
    sub_target = random.choice(dicStr[target])
    return ''.join(generate(dicStr,sub_value)for sub_value in sub_target)

#去除多余的无用字符
def token(string):
    # we will learn the regular expression next course.
    return re.findall('\w+', string)
#读取csv文件指定的列的内容，并且返回干净的内容
def readCsv(_fileName,_countName):
    fileContent = pd.read_csv(_fileName,encoding='utf-8')
    targetContent = []
    for i, v in enumerate (fileContent[_countName]):
        targetContent.append(v)
    clearContent = [''.join(token(str(b))) for b in targetContent]
    return clearContent
#读取txt文件
def readTxt(_fileName):#文件名不能当作参数传
  data = []
  for line in open('d:/train.txt' ,encoding='UTF-8'): #设置文件对象并读取每一行文件
      data.append(line)               #将每一行文件加入到list中
  cleanData = [''.join(token(str(a)))for a in data]
  return cleanData

def writefileContentTOFile(_writeToFileName,_content):
    with open("language.txt", 'w',encoding='utf-8') as f:#文件名不能当作参数传
         for a in _content:
             f.write(str(a) + '\n')

#jieba切词
def cut(string): return list(jieba.cut(string))
languageMode = readCsv('D:/movie_comments0.csv','comment') + readTxt('d:/train.txt') 
writefileContentTOFile("language.txt",languageMode) 
#获取 n-gram language model
TOKEN = []
#enumerate  同时列出数据和数据下标
for i, line in enumerate((open("language.txt",encoding='utf-8'))):
    TOKEN += cut(line.strip())
#Counter（计数器）是对字典的补充，用于追踪值的出现次数
#words_count = Counter(_TOKEN)
TOKEN = [str(t) for t in TOKEN]
TOKEN_2_GRAM = [''.join(TOKEN[i:i+2]) for i in range(len(TOKEN[:-2]))]
count = Counter(TOKEN_2_GRAM)
#print(count.most_common(10))
 #1-gram language model的概率
def prob_1(word,TOKEN):
    words_count = Counter(TOKEN)
    return words_count[word] / len(TOKEN)
#2-gram language model的概率
def prob_2(word1, word2):
    words_count_2 = Counter(TOKEN_2_GRAM)
    if word1 + word2 in words_count_2: return words_count_2[word1+word2] / len(TOKEN_2_GRAM)
    else:
        return 1 / len(TOKEN_2_GRAM)

#由2-gram language model
def get_probablity(sentence):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        #probability = prob_2(word, next_)/prob_1(word) #分母可能为0
        #if prob_1(word) == 0:#当有一项概率为0，则返回0
        #return 0
        probability = prob_2(word, next_)/len(TOKEN_2_GRAM) #老师课堂讲的方法
        sentence_pro *= probability
    return sentence_pro

def generate_best(grammer,typeStr = 'host',grammer_pattern = {}):
          dic_str = generate_grammer(grammer,'=',grammer_pattern)
          testStrDic = []
          for i in range(0,10):
                 strInfo = generate(dic_str,typeStr)
                 info = (strInfo,get_probablity(strInfo))
                 testStrDic.append(info)
          testStrDic = sorted(testStrDic, key=lambda x: x[1], reverse=True)
          print(testStrDic)
          return testStrDic[0]


print(generate_best(host))


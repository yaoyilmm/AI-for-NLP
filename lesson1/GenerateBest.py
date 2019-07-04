#!/usr/bin/env python
# -*- coding:utf-8 -*-
import test1 as gm
import  pandas as pd
import re
import numpy as np
import  jieba
import matplotlib.pyplot as plt
from collections import Counter
from functools import reduce
from operator import add, mul
filename = 'D:/movie_comments0.csv'
comments = pd.read_csv(filename,encoding='utf-8')
print(comments['comment'])

 #第二种方法
data = []
for line in open("d:/train.txt",encoding='UTF-8'): #设置文件对象并读取每一行文件
   data.append(line)               #将每一行文件加入到list中
#commentsList= comments['content'].tolist()
articles = data
print(data)
#去除多余的无用字符
def token(string):
    # we will learn the regular expression next course.
    return re.findall('\w+', string)
articles_clean = [''.join(token(str(a)))for a in articles]
targetComment = []
for i, v in enumerate (comments['comment']):
      targetComment.append(v)

#print(targetComment)
commentsClear = [''.join(token(str(b))) for b in targetComment]
articles_clean = articles_clean + targetComment
print(len(articles_clean))
with open('article_9k.txt', 'w',encoding='utf-8') as f:
    for a in articles_clean:
        f.write(str(a) + '\n')
#jieba切词
def cut(string): return list(jieba.cut(string))
TOKEN = []
#   enumerate  同时列出数据和数据下标
for i, line in enumerate((open('article_9k.txt',encoding='utf-8'))):
    TOKEN += cut(line.strip())
# Counter（计数器）是对字典的补充，用于追踪值的出现次数
words_count = Counter(TOKEN)
print(words_count.most_common(100))
#获取出现频率最高的前100个词
frequiences = [f for w, f in words_count.most_common(100)]
#绘制出现频率最高的前100个词对应的曲线
x = [i for i in range(100)]
plt.plot(x, frequiences)
plt.plot(x, np.log(frequiences))
#   1-gram language model的概率
def prob_1(word):
    return words_count[word] / len(TOKEN)

print(prob_1('我们'))
topTen1grame = TOKEN[:10]
print(topTen1grame)
before = "-"
print(before.join(topTen1grame))
TOKEN = [str(t) for t in TOKEN]
TOKEN_2_GRAM = [''.join(TOKEN[i:i+2]) for i in range(len(TOKEN[:-2]))]
topTen2grame = TOKEN_2_GRAM[:10]
print('2-grame')
print(topTen2grame)
print(''.join(topTen2grame))
words_count_2 = Counter(TOKEN_2_GRAM)

def prob_2(word1, word2):
    if word1 + word2 in words_count_2: return words_count_2[word1+word2] / len(TOKEN_2_GRAM)
    else:
        return 1 / len(TOKEN_2_GRAM)


probValue = prob_2('买', '保险')
print('买保险')
print(probValue)

def get_probablity(sentence):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probability = prob_2(word, next_)
        sentence_pro *= probability
    return sentence_pro


need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = get_probablity(s1), get_probablity(s2)
    better = s1 if p1 > p2 else s2
    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probility {}'.format(s1, p1))
    print('-' * 4 + ' {} with probility {}'.format(s2, p2))
dic_str = gm.generate_grammer(gm.host,'=',gm.grammer_pattern)
testStrDic = []
for i in range(0,10):
       str = gm.generate(dic_str,'host')
       info = (str,get_probablity(str))
       testStrDic.append(info)
print(testStrDic)
print(sorted(testStrDic, key=lambda x: x[1], reverse=True))
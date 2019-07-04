#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random

a = sorted([(2, 5), (1, 4), (5, 0), (4, 4)], key=lambda x: x[0],reverse=True)
print(a)
human = """

human = 自己 寻找 活动

自己 = 我 | 俺 | 我们 

寻找 = 看看 | 咨询 | 想找点

活动 = 保险 | 玩的

"""
host = """
host = 寒暄 报数 询问 业务相关 结尾
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = 耍一耍 | 玩一玩
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
dic_str = generate_grammer(host,'=',grammer_pattern)
print(dic_str)
def generate(dicStr,target):
    if target not in dicStr:
        return target
    sub_target = random.choice(dicStr[target])
    return ''.join(generate(dicStr,sub_value)for sub_value in sub_target)
for i in range(0,10):
    print(generate(dic_str,'host'))
human_pattern = {}
human_dic_str = generate_grammer(human,'=',human_pattern)
print(human_dic_str)
for j in range(0,10):
     print(generate(human_dic_str,'human'))


# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:18:37 2019

@author: lenovo
"""
from functools import lru_cache

'''
dp[i][j]表示word1[0...i-1]到word2[0...j-1]的编辑距离。
而dp[i][0]显然等于i，因为只需要做i次删除操作就可以了。
同理dp[0][i]也是如此，等于i，因为只需做i次插入操作就可以了。
dp[i-1][j]变到dp[i][j]需要加1，因为word1[0...i-2]到word2[0...j-1]
的距离是dp[i-1][j]，而word1[0...i-1]到word1[0...i-2]需要执行一次删除，
所以dp[i][j]=dp[i-1][j]+1；同理dp[i][j]=dp[i][j-1]+1，
因为还需要加一次word2的插入操作。如果word[i-1]==word[j-1]，
则dp[i][j]=dp[i-1][j-1]，如果word[i-1]!=word[j-1]，
那么需要执行一次替换replace操作，所以dp[i][j]=dp[i-1][j-1]+1，
以上就是状态转移方程的推导
'''
#print(solution)
class Solution:
    # @return an integer
    def minDistance(self, word1, word2):
        m=len(word1)+1; n=len(word2)+1
        dp = [[0 for i in range(n)] for j in range(m)]
        for i in range(n):
            dp[0][i]=i
        for i in range(m):
            dp[i][0]=i
        for i in range(1,m):
            for j in range(1,n):
                dp[i][j]=min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(0 if word1[i-1]==word2[j-1] else 1))
        return dp[m-1][n-1]
    
solution = {}
@lru_cache(maxsize=2**10)
def edit_distance(string1, string2):
    
    if len(string1) == 0: return len(string2)#如果string1为空，string1到string2需要添加len（string2）步
    if len(string2) == 0: return len(string1)#如果string2为空，string1到string2需要删除len(string1)步
    
    tail_s1 = string1[-1]#取出两个字符串最后的一个字符
    tail_s2 = string2[-1]
    
    candidates = [
        (edit_distance(string1[:-1], string2) + 1, '删除 {}'.format(tail_s1)),  # edit_distance(string1, string2) == edit_distance(string1 del 最后一个字符, string2) string 1 delete tail
        #
        (edit_distance(string1, string2[:-1]) + 1, '添加 {}'.format(tail_s2)),  # edit_distance(string1, string2) == edit_distance(string1 , string2 del 最后一个字符 ) then add tail of string2
    ]
    
    if tail_s1 == tail_s2:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 0, '')# 如果最后一个字符相同 edit_distance(string1, string2) == edit_distance(string1[:-1], string2[:-1]
    else:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 1, 'SUB {} => {}'.format(tail_s1, tail_s2))#如果最后一个字符不同，edit_distance(string1, string2) == edit_distance(string1[:-1], string2[:-1]+ 1 加一个替换操作

    candidates.append(both_forward)
    print(candidates)
    min_distance, operation = min(candidates, key=lambda x: x[0])#按照需要改变的步数排序，选出最快的编辑步数
    
    solution[(string1, string2)] = operation 
    
    return min_distance

edit_distance('ABCDE', 'ABCCEF')
'''
总结一下编辑距离主要分三个操作插入、删除、替换 
len(str1) = m  len(str2) = n
dp[m][n] 表示从str1到str2的编辑距离 
dp[m][n] = dp[m-1][n] + 1  对应删除
dp[m][n] =dp[m][n-1] + 1   对应插入
if str1[m - 1] == str2[n-1] 最后一项相同
    dp[m][n] = dp[m-1][n-1]
else
    dp[m][n] = dp[m-1][n-1] 对应替换
转化为函数就是老师写的上面的那个方法
'''
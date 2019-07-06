# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:09:53 2019

@author: lenovo
"""
from collections import defaultdict
import  jieba

#jieba切词
def cut(string): return list(jieba.cut(string))

def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])

def pat_match(pattern, saying):
    if not pattern or not saying: return []
    
    if is_variable(pattern[0]):
        return [(pattern[0], saying[0])] + pat_match(pattern[1:], saying[1:])
    else:
        if pattern[0] != saying[0]: return []
        else:
            return pat_match(pattern[1:], saying[1:])

def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}
i = 0
def subsitite(rule, parsed_rules):
    if not rule: return []
     # dic.get(key,value = default) 在dic中查找键为key的元素，如果没有添加该键并且指为value
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)


got_patterns = pat_match("I want ?X".split(), "I want iPhone".split())
dic = pat_to_dict(got_patterns)

rule = "What if you mean if you got a ?X".split()

#print(subsitite("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns)))

#print(['d','b']  + ['a','c'])

def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])


is_pattern_segment('?*P')

fail = [True, None]

def pat_match_with_seg(pattern, saying):
    if not pattern or not saying: return []
    
    pat = pattern[0]
    
    if is_variable(pat):#简单的单个单词匹配
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):#多个单词匹配
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail

def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    #seg_pat = seg_pat.replace('?*', '?')
    if not rest: return (seg_pat, saying), len(saying)  #pattern 只有一项  
    
    for i, token in enumerate(saying):#遍历每个单词
       # print(saying[(i + 1):])
       # print(i)
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i
    
    return (seg_pat, saying), len(saying)

def is_match(rest, saying):
    if not rest and not saying:# rest saying 全为空
        return True
    if not all(a.isalpha() for a in rest[0]):#匹配模板第一项不全是字母
        return True
    #print(rest)
    if len(rest) <= 1 or len(saying)<= 1 :
        return False
    else:
        if rest[0] != saying[0]:
            return False
        return is_match(rest[1:], saying[1:])#继续匹配剩余的内容

#print(segment_match('?*P is very good'.split(), "My dog and my cat is very good".split()))

#print(pat_match_with_seg('?*P is very good and ?*X'.split(), "My dog is very good and my cat is very cute".split()))

response_pair = {
    "I was ?*X": ["Were you really ?X ?", "I already knew you were ?X ."],
    'I need ?X': ["Why do you neeed ?X"],
    "I dont like my ?X": ["What bad things did ?X do for you?"],
    "?*X hello ?*Y": ["Hi, how do you do?"]
    
}

match = pat_match_with_seg('I was ?*X'.split(), 
                  "I was late".split())
print(match)
print('---------------')
match = subsitite("Why do you neeed ?X".split(), pat_to_dict(pat_match_with_seg('I need ?*X'.split(), 
                  "I need an iPhone".split())))
s =  pat_to_dict(pat_match_with_seg('?*X hello ?*Y'.split(),"I am mike hello lili ".split()))
#print(s)
match =" ".join(subsitite("Hi, how do you do? ?*X hello ?*Y".split(), pat_to_dict(pat_match_with_seg('?*X hello ?*Y'.split(), 
                  "I am mike hello lilei ".split()))))
#print(match)
rules = {
    '?*x你好?*y': ['你好呀', '请告诉我你的问题'],
    '?*x我想?*y': ['你觉得?y有什么意义呢？', '为什么你想?y', '你可以想想你很快就可以?y了']

}
def get_response(saying ,pattern):
    print("A:" + saying)
    for key in pattern.keys():
        match_res = pat_match_with_seg(key.split(),saying.split())
        #print(match_res)
        if match_res == fail:
            continue
        match_dic =  pat_to_dict(match_res)
        temDic = {}
        for k,v in match_dic.items():
            if is_pattern_segment(k) :k = k.replace('?*','?')
            temDic[k] = v
        result =  " ".join(subsitite(' '.join(pattern[key]).split(),temDic))
        print("B:"+ result + '\n')
        return result
       
get_response('I need money',response_pair)
get_response('I dont like my dog',response_pair)
get_response('I was late',response_pair)
get_response('I am hellen, hello ',response_pair)


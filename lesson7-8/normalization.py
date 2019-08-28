import  jieba
import  re
import  string
def cut(string):
    token =  list(jieba.cut(string))
    token = [word.strip() for word in token]
    return token
def get_stop_words_list():
    with open("./stop_words/stop_words.utf8",encoding="utf-8") as f:
       stop_words_list = f.readlines()
    return stop_words_list
#去除特殊符号
def remove_special_characters(text):
    tokens = cut(text)
    pattern = re.compile("[{0}]".format(re.escape(string.punctuation)) )#print(string.punctuation) = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    filtered_tokens =  filter(None,[pattern.sub('', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text
if __name__ == "__main__":
   s = "，{1234，。#5}是一个[456]文本特征提取##方法None。对于$每一个训练文本，它只考虑每种词汇在该训练文本中出现的频率。"
   s =  remove_special_characters(s)
   print(s)
   value =filter(None, [1, -1, 0, True, False, [1, 0, True, False], []])#去除0，False,None
   valueList = list(value)
   print(valueList)# 输出 [1, -1, True, [1, 0, True, False]]
   print(re.escape('www.python.org'))
   print(re.findall(r'w\$.py', "jw$.pyji w.py.f"))
   print(re.findall(re.escape('w$.py'), "jw$.pyji w.py.f"))
   """
   总结 
   1.re.escape(pattern) 可以对字符串中所有可能被解释为正则运算符的字符进行转义
      r'w\$.py' == re.escape('w$.py') 调用re.escape()不用对特殊字符转义，也就是加\
      re.escape(string.punctuation)则表示对标点符号都进行转义
      "[{0}]".format(re.escape(string.punctuation)) == \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^_\`\{\|\}\~
   2. filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
      该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，最后
      将返回 True 的元素放到新列表中。
      filter(None,list) 去除0，False,None
   3. pattern.sub 替换子串
      re.sub的函数原型为：re.sub(pattern, repl, string, count)
   """

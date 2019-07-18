# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 21:49:41 2019

@author: lenovo
"""

from sklearn.datasets import load_boston
import random
import matplotlib.pyplot as plt
#from icecream import ic

data = load_boston()

X, y= data['data'], data['target']

def draw_rm_and_price():
    plt.scatter(X[:, 5], y)

draw_rm_and_price()
def price(rm, k, b):
    """f(x) = k * x + b"""
    return k * rm + b
#取第五列所对应的数据，即就是房屋是几居的，获得房屋的居室数和房屋价格的关系
X_rm = X[:, 5]
k = random.randint(-100, 100)
b = random.randint(-100, 100)
price_by_random_k_and_b = [price(r, k, b) for r in X_rm]

#draw_rm_and_price()
#plt.scatter(X_rm, price_by_random_k_and_b)

def loss(y, y_hat): # to evaluate the performance 
    return sum((y_i - y_hat_i)**2 for y_i, y_hat_i in zip(list(y), list(y_hat))) / len(list(y))

#First-Method: Random generation: get best k and best b
'''
需要尝试很多次才能找到相对拟合的参数
'''
trying_times = 2000

min_loss = float('inf')
best_k, best_b = None, None

for i in range(trying_times):
    k = random.random() * 200 - 100
    b = random.random() * 200 - 100
    price_by_random_k_and_b = [price(r, k, b) for r in X_rm]

    current_loss = loss(y, price_by_random_k_and_b)
    
    if current_loss < min_loss:
        min_loss = current_loss
        best_k, best_b = k, b
       # print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))


'''
2nd-Method: Direction Adjusting
给出k,b变化的方向，如果在指定的一个方向上Loss越来越小，则继续在这个方向上调整
否则再随机一个方向
'''
        
trying_times = 2000
min_loss = float('inf')

best_k = random.random() * 200 - 100
best_b = random.random() * 200 - 100

direction = [
    (+1, -1),  # first element: k's change direction, second element: b's change direction
    (+1, +1), 
    (-1, -1), 
    (-1, +1),
]

next_direction = random.choice(direction)

scalar = 0.1

update_time = 0

for i in range(trying_times):
    
    k_direction, b_direction = next_direction
    
    current_k, current_b = best_k + k_direction * scalar, best_b + b_direction * scalar
    
    price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]

    current_loss = loss(y, price_by_k_and_b)
    
    if current_loss < min_loss: # performance became better
        min_loss = current_loss
        best_k, best_b = current_k, current_b
        
        next_direction = next_direction
        update_time += 1
        
       # if update_time % 10 == 0: 
            #print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))
    else:
        next_direction = random.choice(direction)


'''
如果我们想得到更快的更新，在更短的时间内获得更好的结果，我们需要一件事情：
找对改变的方向
如何找对改变的方向呢？
loss 按两个对应Y的差值平方再平均
2nd-method: 监督让他变化--> 监督学习
'''
def partial_k(x, y, y_hat):
    n = len(y)

    gradient = 0
    
    for x_i, y_i, y_hat_i in zip(list(x), list(y), list(y_hat)):
        gradient += (y_i - y_hat_i) * x_i
    
    return -2 / n * gradient


def partial_b(x, y, y_hat):
    n = len(y)

    gradient = 0
    
    for y_i, y_hat_i in zip(list(y), list(y_hat)):
        gradient += (y_i - y_hat_i)
    
    return -2 / n * gradient
trying_times = 5000

X, y = data['data'], data['target']

min_loss = float('inf') 

current_k = random.random() * 200 - 100
current_b = random.random() * 200 - 100

#learning_rate = 1e-04
learning_rate = 0.002

update_time = 0

for i in range(trying_times):
    
    price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
    
    current_loss = loss(y, price_by_k_and_b)

    if current_loss < min_loss: # performance became better
        min_loss = current_loss
        
        #if i % 50 == 0: 
         #print('1 When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b, min_loss))

    k_gradient = partial_k(X_rm, y, price_by_k_and_b)
    
    b_gradient = partial_b(X_rm, y, price_by_k_and_b)
    
    current_k = current_k + (-1 * k_gradient) * learning_rate

    current_b = current_b + (-1 * b_gradient) * learning_rate

X_rm = X[:, 5]
k = 11.431551629413757
b = -49.52403584539048
price_by_random_k_and_b = [price(r, k, b) for r in X_rm]

#draw_rm_and_price()
#plt.scatter(X_rm, price_by_random_k_and_b)

#作业内容 损失函数
def loss_abs(y, y_hat): # to evaluate the performance 
    return sum(abs(y_i - y_hat_i) for y_i, y_hat_i in zip(list(y), list(y_hat))) / len(list(y))

#k的偏导数
def partial_k_abs(x, y, y_hat):
    n = len(y)
    gradient = 0
    for x_i, y_i, y_hat_i in zip(list(x), list(y), list(y_hat)):
        #gradient += (y_i - y_hat_i) * x_i
         if y_i > y_hat_i:
             gradient += -1 *  x_i
         else:
             if y_i < y_hat_i:
                 gradient +=  x_i
         
    return 1 / n * gradient

#b的偏导数
def partial_b_abs(x, y, y_hat):
    n = len(y)
    gradient = 0
    
    for y_i, y_hat_i in zip(list(y), list(y_hat)):
         if y_i > y_hat_i:
             gradient += -1
         else:
             if y_i < y_hat_i:
                 gradient += 1
    
    return 1 / n * gradient

trying_times = 5000
X, y = data['data'], data['target']
min_loss = float('inf') 
current_k = random.random() * 200 - 100
current_b = random.random() * 200 - 100

learning_rate = 1e-04
#learning_rate = 0.002
update_time = 0

for i in range(trying_times):
    
    price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
    
    current_loss = loss_abs(y, price_by_k_and_b)

    if current_loss < min_loss: # performance became better
        min_loss = current_loss
        if i % 50 == 0: 
           print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b, min_loss))

    k_gradient = partial_k(X_rm, y, price_by_k_and_b)
    
    b_gradient = partial_b(X_rm, y, price_by_k_and_b)
    
    current_k = current_k + (-1 * k_gradient) * learning_rate

    current_b = current_b + (-1 * b_gradient) * learning_rate
    
X_rm = X[:, 5]
k = current_k
b = current_b
price_by_random_k_and_b = [price(r, k, b) for r in X_rm]
draw_rm_and_price()
plt.scatter(X_rm, price_by_random_k_and_b)

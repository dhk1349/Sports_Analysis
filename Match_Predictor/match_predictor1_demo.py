#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:37:06 2019

@author: donghoon
"""

'''
프로그램 디자인
모델은 단층짜리 logistic regression 사용
활성함수는 tanh fundtion을 사용: {e^z-e^(-z)}/{e^z+e^(-z)}
Loss function: -(y*log(yhat)+(1-y)log(1-yhat))
Cost function: average of loss function
Partial derivation of cost by w: 1/m*(A-Y)
Partial derivation of cost by b: 1/m(sum of (yhat-y))

input으로 특정 클럽의 경기 정보를 가져오게 된다.
각 정보는 input layer로 설정한다. 
초기 weight는 모두 0으로 설정한다. 
초기 bias 값은 0으로 설정한다.

X형은 [[match1_data],[match2_data],...[matchm_data]]와 같다.
이를 transpose시킬 것이다.

In this program, # of samples will be denoted as m,
ans numbers of variables in each line of function will be denoted as n
'''

import numpy as np
def initialize_par(x):
    #Will return parameter w and b
    dim=x.shape[0]  #dimension of x will be(n*m)
    w=np.zeros(1,dim) #dimension of w will be (1*n)
    b=0
    return w,b

def getZ(w,b,x):
    z=np.dot(w,x)+b
    return z

def tanh(z):
    #Z는 m개의 sample을 가질 것.
    A=(np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))
    return A

def propagation(Ys, w,b,x):
    Z=getZ(w,b,x)
    Y_hats=tanh(Z)
    
    num=Ys.shape[0]
    loss=-(Ys*np.log(Y_hats)+(1-Ys)*np.log(1-Y_hats))
    cost=1/num*np.sum(loss)
    dw=1/num(Y_hats-Ys)
    db=1/num(np.sum(Y_hats-Ys))
    return cost, dw,db

def train(match_stat, match_result,loop_num,learning_rate):
    x=np.asarray(match_stat).T
    w,b=initialize_par(x)
    costs=[]
    
    for i in range(loop_num):
        cost,dw,db=propagation(match_result,w,b,x)
        if i%100==0:
            costs.append(cost)
            print(i+"th train cost: "+str(cost))
        w=w-learning_rate*dw
        b=b-learning_rate*db
    
    return w,b

def test(test_data, w,b):
    x=np.asarray(test_data).T
    Z=getZ(w,b,x)
    A=tanh(Z)
    prediction=A
    for i in range(len(A)):
        if(A[0,i]>0):
            prediction[i]=1
        else:
            prediction[i]=-1
    
    return prediction


def model(train_match_stat, train_match_result, test_match_stat,test_match_result, learning_rate, loop_num):
    w,b=train(train_match_stat, train_match_result, loop_num, learning_rate)
    
    #Accuracy test on training samples
    training_prediction=test(train_match_stat,w,b)
    train_match_result=np.asarray(train_match_result)
    print("Accuracy on training samples: {}".format(100-np.mean(np.abs(training_prediction-train_match_result))*100))
    
    
    #Accuracy test on test samples
    test_prediction=test(test_match_stat, w, b)
    test_match_result=np.asarray(test_match_result)
    print("Accuracy on training samples: {}".format(100-np.mean(np.abs(test_prediction-test_match_result))*100))
    







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
    w=np.zeros((1,dim)) #dimension of w will be (1*n)
    b=0
    
    return w,b

def getZ(w,b,x):
    z=np.dot(w,x)+b
    return z

def sigmoid(z):
    #Z는 m개의 sample을 가질 것.
    A=1/(1+np.exp(-z))
    return A

def propagation(Ys, w,b,x):
    Z=getZ(w,b,x)
    Y_hats=sigmoid(Z)
    Ys=np.asarray(Ys)
    
    num=Ys.shape[0]
    loss=-(Ys*np.log(Y_hats)+(1-Ys)*np.log(1-Y_hats))
    cost=1/num*np.sum(loss)
    dw=1/num*(np.dot(x,(Y_hats-Ys).T)).T
    db=1/num*(np.sum(Y_hats-Ys))
    return cost, dw,db

def train(match_stat, match_result,loop_num,learning_rate):
    x=np.asarray(match_stat).T
    w,b=initialize_par(x)
    costs=[]
    match_result=np.asarray(match_result)
    for i in range(loop_num):
        cost,dw,db=propagation(match_result,w,b,x)
        if i%100==0:
            costs.append(cost)
            print("program is running...")
            print(cost)
        w=w-learning_rate*dw
        b=b-learning_rate*db
    
    return w,b

def test(test_data, w,b):
    x=np.asarray(test_data).T
    Z=getZ(w,b,x)
    A=sigmoid(Z)
    print(A)
    prediction=np.zeros((1,A.shape[1]))
    for i in range(A.shape[1]):     
        if(A[0,i]>0.6):
            prediction[0,i]=1
        elif A[0,i]<0.3:
            prediction[0,i]=-1
        else:
            prediction[0,i]=0
    return prediction


def model(train_match_stat, train_match_result, test_match_stat,test_match_result, learning_rate, loop_num):
    w,b=train(train_match_stat, train_match_result, loop_num, learning_rate)
    
    print("W: "+str(w)+"  B: "+str(b))
    #Accuracy test on training samples
    training_prediction=test(train_match_stat,w,b)
    train_match_result=np.asarray(train_match_result)
    print(training_prediction)
    print(train_match_result)
    print("Accuracy on training samples: {}".format(100-np.mean(np.abs(training_prediction-train_match_result))*100))
    
    
    #Accuracy test on test samples
    test_prediction=test(test_match_stat, w, b)
    test_match_result=np.asarray(test_match_result)
    print("Accuracy on training samples: {}".format(100-np.mean(np.abs(test_prediction-test_match_result))*100))





samples=[[' Arsenal ', ' Manchester United ', 46.1, 0.75, 0.8491379310344828, 1], [' Tottenham Hotspur ', ' Arsenal ', 39.8, 1.3333333333333333, 0.65748031496063, 0], [' Arsenal ', ' AFC Bournemouth ', 64.8, 1.4, 1.8786127167630058, 1], [' Arsenal ', ' Southampton ', 62.1, 1.0, 1.6820809248554913, 1], [' Huddersfield Town ', ' Arsenal ', 45.4, 0.5714285714285714, 0.8506224066390041, 1], [' Manchester City ', ' Arsenal ', 41.2, 0.16666666666666666, 0.7047308319738989, -1], [' Arsenal ', ' Cardiff City ', 70.9, 2.0, 2.543103448275862, 1], [' Arsenal ', ' Chelsea ', 35.7, 5.0, 0.5486862442040186, 1], [' West Ham United ', ' Arsenal ', 58.6, 0.6666666666666666, 1.4605263157894737, -1], [' Arsenal ', ' Fulham ', 59.6, 2.25, 1.484931506849315, 1], [' Liverpool ', ' Arsenal ', 52.1, 0.2, 1.0782778864970646, -1], [' Brighton and Hove Albion ', ' Arsenal ', 68.0, 1.3333333333333333, 2.1944444444444446, 0], [' Arsenal ', ' Burnley ', 60.1, 3.0, 1.5490196078431373, 1], [' Southampton ', ' Arsenal ', 66.2, 0.5714285714285714, 1.9842271293375395, -1], [' Arsenal ', ' Huddersfield Town ', 61.9, 2.0, 1.6253869969040247, 1], [' Manchester United ', ' Arsenal ', 55.2, 0.5714285714285714, 1.2192393736017897, 0], [' Arsenal ', ' Tottenham Hotspur ', 59.3, 1.1666666666666667, 1.4410876132930515, 1], [' AFC Bournemouth ', ' Arsenal ', 58.7, 0.8, 1.4568527918781726, 1], [' Arsenal ', ' Wolverhampton Wanderers ', 71.7, 0.6, 2.5136986301369864, 0], [' Arsenal ', ' Liverpool ', 61.8, 1.0, 1.646067415730337, 0], [' Crystal Palace ', ' Arsenal ', 57.8, 0.6666666666666666, 1.3909774436090225, 0], [' Arsenal ', ' Leicester City ', 69.1, 3.0, 2.2750809061488675, 1], [' Fulham ', ' Arsenal ', 51.1, 1.75, 1.06553911205074, 1], [' Arsenal ', ' Watford ', 63.5, 0.4, 1.8187919463087248, 1], [' Arsenal ', ' Everton ', 62.5, 0.8333333333333334, 1.7619047619047619, 1], [' Newcastle United ', ' Arsenal ', 63.7, 1.0, 1.8287461773700306, 1], [' Cardiff City ', ' Arsenal ', 72.3, 3.6666666666666665, 2.713675213675214, 1], [' Arsenal ', ' West Ham United ', 61.5, 2.0, 1.595307917888563, 1], [' Chelsea ', ' Arsenal ', 37.7, 0.5454545454545454, 0.5958333333333333, -1], [' Arsenal ', ' Manchester City ', 42.0, 0.375, 0.7225225225225225, -1]]
match_dat=[]
result=[]
for i in samples:
    temp=[]
    temp.append(i[2])
    temp.append(i[3])
    temp.append(i[4])
    match_dat.append(temp)
    result.append(i[5])

model(match_dat,result,match_dat,result,0.005,10000)











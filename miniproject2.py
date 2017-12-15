#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 12:21:39 2017

@author: jamesdawson
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

def data_loader(name):
        loc = '/home/jamesdawson/Documents/Data Analysis Project/MiniProjectAllData/Continuum_subtracted/'
        data = np.loadtxt(loc+name+'_data.txt')
        return data

def chi_squared(y_GS,y_template,sig_GS):        
        A = np.sum((y_GS*y_template)/(sig_GS**2)) /  np.sum( (y_GS**2)/(sig_GS**2))
        chi = np.sum(((y_GS-(A*y_template))/sig_GS)**2)
        return chi

def shifter(data,y_vals,velocity):
        shifted = np.zeros(len(data))
        for i in range(len(data)):
                shifted[i] = data[i] + (velocity*data[i])
        return shifted

temp = data_loader('keck_k5')
temp_x,temp_y,temp_err = temp[:,0],temp[:,1],temp[:,2]

test_data = ['gs2000_01','gs2000_02','gs2000_03','gs2000_04','gs2000_05','gs2000_06','gs2000_07','gs2000_08','gs2000_09','gs2000_10','gs2000_11','gs2000_12','gs2000_13']

data = []
for i in range(len(test_data)):
        data.append(data_loader(test_data[i]))
data = np.array(data)

test = data_loader(test_data[1])
testx,testy,testerr = test[:,0],test[:,1],test[:,2]

###     Testing the velocity change effects     ###############################
plt.figure()
plt.subplot(311)
plt.plot(temp_x,temp_y,'k')
plt.subplot(312)
plt.plot(temp_x,temp_y,'k')
plt.plot(shifter(temp_x,temp_y,0.00001),temp_y,'b',alpha=0.3)
plt.ylabel('I')
plt.subplot(313)
plt.plot(temp_x,temp_y,'k')
plt.plot(shifter(temp_x,temp_y,-0.00001),temp_y,'r',alpha=0.3)
plt.xlabel('$\lambda / \AA$')
###############################################################################

###     Spline function calculator      #######################################

x = shifter(temp_x,temp_y,-0.25)

x_new = np.linspace((x[0]-10),(x[-1]+10),10000)

f = InterpolatedUnivariateSpline(x, temp_y, k=3)

new_y = f(x_new)
new_y[np.where(x_new < testx[0])] = 0
new_y[np.where(x_new > testx[-1])] = 0

###############################################################################
'''

for k in range(len(data)):

        testx,testy,testerr = splitter(data[k][:-1,0],data[k][:-1,1],data[k][:-1,2],60)
        testx = testx[11]
        testy = testy[11]
        testerr = testerr[11]
        

        
        offset = np.arange(-30,30,0.1)
        
        chi_vals_all = []
        for j in range(len(testx)):
                chi_vals = []
                for i in range(len(offset)):
                        chi_vals.append(chi_squared(testy[j],tempy[j]+offset[i],testerr[j]))
                chi_vals_all.append(np.array(chi_vals))
        
        chi_vals_all = np.array(chi_vals_all)
        
        offset_locs = []
        for i in range(len(chi_vals_all)):
                offset_locs.append(offset[np.argmin(chi_vals_all[i])])
                
        offsets.append(np.mean(offset_locs))
        std_offsets.append(np.std(offset_locs))
 
x = np.arange(1,len(offsets)+1,1)        
plt.figure()        
plt.plot(x,offsets)
'''
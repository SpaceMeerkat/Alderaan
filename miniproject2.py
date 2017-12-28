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
        Aa = np.sum((y_GS*y_template)/(sig_GS**2))
        Ab = np.sum((y_template**2)/(sig_GS**2))
        A = Aa/Ab
        chi = np.sum( (((y_GS-(A*y_template))/sig_GS)**2) )
        return chi,A

def shifter(data,velocity):
        shifted = np.zeros(len(data))
        for i in range(len(data)):
                shifted[i] = data[i] + (velocity*data[i])
        return shifted

temp = data_loader('keck_k5')
temp_x,temp_y,temp_err = temp[:,0],temp[:,1],temp[:,2]

test_data = ['gs2000_01','gs2000_02','gs2000_03','gs2000_04','gs2000_05','gs2000_06','gs2000_07','gs2000_08','gs2000_09','gs2000_10','gs2000_11','gs2000_12','gs2000_13']

###     Testing the velocity change effects     ###############################

plt.figure()
plt.subplot(311)
plt.plot(temp_x,temp_y,'k')
plt.subplot(312)
plt.plot(temp_x,temp_y,'k')
plt.plot(shifter(temp_x,0.3),temp_y,'r',alpha=0.3)
plt.ylabel('I')
plt.subplot(313)
plt.plot(temp_x,temp_y,'k')
plt.plot(shifter(temp_x,-0.3),temp_y,'b',alpha=0.3)
plt.xlabel('$\lambda / \AA$')

###############################################################################

shift_space = np.arange(-0.003,0.003,0.000001)

###############################################################################

all_shifts = []
plus_sigma = []
minus_sigma = []

for j in range(len(test_data)):
        print(((j/len(test_data))*100),'%')
        chi_vals = []
        A_vals = []
        test = data_loader(test_data[j])
        testx,testy,testerr = test[:,0],test[:,1],test[:,2]
#        ind = np.where(testy >= 0.)
#        testy[ind] = 0
        for i in range(len(shift_space)):
                x = shifter(temp_x,shift_space[i])
                f = InterpolatedUnivariateSpline(x, temp_y, k=3)
                new_y = f(testx)
#                ind = np.where(new_y >= 0.)
#                new_y[ind] = 0
                new_y[np.where(testx < x[0])] = 0
                new_y[np.where(testx > x[-1])] = 0
                
                chi,A = chi_squared(testy,new_y,testerr)
                A_vals.append(A)
                chi_vals.append(chi)
                
        if j == 1:

                plt.figure()
                plt.plot(shift_space,chi_vals,'k-')
                plt.xlabel('Velocity shift (Vc) / $kms^{-1}$ ')
                plt.ylabel('$\chi^{2}$')
                plt.savefig('Chi_example')
                                
        minimum = np.min(chi_vals)
        ind = np.where(chi_vals<(minimum+1))
        plus_sigma.append(shift_space[np.max(ind)])
        minus_sigma.append(shift_space[np.min(ind)])

        maxim = shift_space[np.argmin(chi_vals)]
        all_shifts.append(maxim)
        
##############################################################################
plt.figure()
phase = np.array([-0.1405 ,-0.0583,0.0325,0.0998,0.1740,0.2310,0.3079,0.3699,0.4388,0.5008,0.5698,0.6371,0.7276]) 
plt.errorbar(phase,np.array(all_shifts)*(3e5),yerr=[np.array(minus_sigma)*(3e5),np.array(plus_sigma)*(3e5)],color='k',fmt='o', markersize=2, capsize=2)
plt.xlabel('Phase/$\phi$')
plt.ylabel('Velocity/$kms^{-1}$')
plt.savefig('Radial Velocity Curve For GS2000')

final_data = np.transpose(np.vstack([phase,np.array(all_shifts)*(3e5),np.array(plus_sigma)*(3e5),np.array(minus_sigma)*(3e5)]))
np.savetxt('velocity_data',final_data,delimiter=' ')

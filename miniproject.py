#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:27:15 2017

@author: jamesdawson
"""

import numpy as np
import matplotlib.pyplot as plt

###############################################################################
def template_loader(file_name):
        data = np.loadtxt('KeckTemplates/'+file_name+'.txt')        
        x = data[:,0]
        y = data[:,1]
        err = data[:,2]
        return x,y,err
###############################################################################
def gs2000_loader(file_name):
        data = np.loadtxt('GS2000/keck_gs2000_'+file_name+'.txt')       
        x = data[:,0]
        y = data[:,1]
        err = data[:,2]       
        return x,y,err
###############################################################################
def continuum_template(flux,wave):
        fit = np.zeros(len(flux))
        fit[0] = flux[5]
        av = np.zeros(len(flux))
        stds = np.zeros(len(flux))
        for i in range(0,len(flux)):
                ten = flux[i:i+10]
                stds[i] = np.std(ten)
                av[i] = np.median(ten)
                for j in range(0,10):
                        if av[i] < (av[i-50]):
                                fit[i] = av[i-50] + stds[i-50]
                                break
                        else:
                                fit[i] = av[i]
                                break
        return fit
###############################################################################
def smooth(flux,wave):
        cont = continuum_template(continuum_template(flux,wave),wave)
        return cont
###############################################################################
        
#def continuum2(flux,wave):
#        fit = np.zeros(len(flux))
#        fit[0] = flux[0]
#        av = np.zeros(len(flux))
#        stds = np.zeros(len(flux))
#        for i in range(0,len(flux)):
#                ten = flux[i:i+400]
#                stds[i] = np.std(ten)
#                av[i] = np.median(ten)
#                for j in range(0,10):
#                        if av[i] < (av[i-100] - stds[i-100]):
#                                fit[i] = av[i-100] - stds[i-100]
#                                break
#                        else:
#                                fit[i] = av[i]
#                                break
#        cont1 = np.zeros(len(flux))
#        for i in range(0,len(flux)):
#                for j in range(0,10):
#                        if fit[i] > (fit[i-500] + stds[i-500]):
#                                cont1[i] = fit[i-500] + stds[i-400]
#                                break
#                        else:
#                                cont1[i] = fit[i]
#                                break
#        return cont1

def continuum2(flux,wave):
        fit = np.zeros(len(flux))
        fit[0] = flux[5]
        stds = np.zeros(len(flux))
        for i in range(0,len(flux)):
                val = 30
                if i <= val:
                        ten = flux[i:i+val]
                        stds[i] = np.std(ten)
                        fit[i] = np.mean(ten)          
                else:
                        
                        ten = flux[i-val:i+val]
                        stds[i] = np.std(ten)
                        fit[i] = np.mean(ten)

        return fit

def smooth2(flux,wave):
        cont = continuum2(continuum2(flux,wave),wave)
        return cont

###############################################################################
def continuum_subtraction(x,y,err,continuum,name):
        loc = '/home/jamesdawson/Documents/Data Analysis Project/MiniProjectAllData/Continuum_subtracted/'
        data = y - continuum
        ind = np.where(data >= 0.)
        data[ind] = 0
        np.savetxt(loc+name+'_data.txt',np.transpose(np.vstack([x,data,err])),delimiter=' ')
###############################################################################    

### SUBTRACTING THE CONTINUUM AND SAVING RESULTING CURVES FOR GS2000 DATA ###

gs2000 = ['01','02','03','04','05','06','07','08','09','10','11','12','13']


for i in range(len(gs2000)):
        x,y,err = gs2000_loader(gs2000[i])
        continuum = smooth2(y,x)
        continuum_subtraction(x,y,err,continuum,'gs2000_'+gs2000[i])
        
###############################################################################
        
### SUBTRACT CONTINUUM FOR ANY TEMPLATE AND SAVE RESULTING CURVE ###
        
def template_cont_subtract_save(name):
        loc = '/home/jamesdawson/Documents/Data Analysis Project/MiniProjectAllData/Continuum_subtracted/'
        x,y,err = template_loader(name)
        cont = smooth(y,x)
        subtracted = y-cont
        ind = np.where(subtracted >= 0.)
        subtracted[ind] = 0
        np.savetxt(loc+name+'_data.txt',np.transpose(np.vstack([x,subtracted,err])),delimiter=' ')
        
template_cont_subtract_save('keck_k5')
        
###############################################################################
        


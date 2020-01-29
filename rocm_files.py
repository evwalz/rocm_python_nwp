# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:40:15 2020

@author: walz
"""

import numpy as np
from scipy.stats import rankdata
from scipy import interp
import matplotlib.pyplot as plt

# own functions:
from uroc import uroc, Trapezoidal

def rocm(response, predictor, path):
    """
    Creates a sequence of ROC curves and saves them to path.

    Visualizes the performances of predictors for real valued forecasting problems. 

    Parameters
    ----------
    response : 1D array_like, 1-D array containing obervation. Need to have the same length in the ``axis`` dimension as b.
	predictor : 1D array_like, 1-D array containing forecast for observation a.
    path: String, Example: /home/animation.gif 
       
    Returns
    -------
    Several png-files
    """ 
    n = response.shape[0]
    # order response and predictor increasing by response
    response_sorted_indices = np.argsort(response)
    response_sorted = response[response_sorted_indices]
    predictor_sorted = predictor[response_sorted_indices]
    response_unique, response_unique_index = np.unique(response_sorted, return_index=True)
    N = response_unique.shape[0]-1
    a = 400
    b = 1
    if a > N:
        a = N
    s = np.floor((N - 1) / (a - 1))
    hh = (2 + (a - 1) * s)
    indx_setCa = np.arange(1, hh , s)
    class_length = np.subtract(np.append(response_unique_index[2:],n),response_unique_index[1:])
    indx_setCb = np.where(class_length>n/b)
    indxsetC = np.sort(np.unique(np.concatenate((indx_setCa, indx_setCb), axis = None)))

    # compute weights
    ncontrol = (response_unique_index)[1:]
    ncontrol_split = response_unique_index[indxsetC.astype(int)]
    thresholds_split = response_unique[indxsetC.astype(int)]
    ncases_split = n - ncontrol_split
    weights_split = np.multiply(ncases_split , ncontrol_split)
    weights_all = np.multiply(ncontrol, n-ncontrol)
    weights_scale = weights_split / np.max(weights_all)

    classes_predictor = rankdata(predictor_sorted, method='dense')
    Split_classes_predictor = np.split(classes_predictor[:response_unique_index[-1]],ncontrol_split[:-1])

    # compute first roc curve
    order_predictor = predictor.argsort()[::-1]
    response_binary = np.where(np.array(response[order_predictor]) > response_unique[0], 1, 0)
    predictor_sorted = predictor[order_predictor][::-1]
    predictor_unique, predictor_unique_index = np.unique(predictor_sorted, return_index=True)
    dups = (n - 1) - predictor_unique_index[::-1]
    tpr = np.insert(np.cumsum(response_binary)[dups], 0, 0)
    fpr = np.insert(np.cumsum(response_binary == 0)[dups], 0, 0)
    tpr_weight = tpr[::-1]
    fpr_weight = fpr[::-1]
    InterPoint = np.arange(0, 1001, 1) * 0.001
    cases = n- ncontrol_split[0]
    hitrate = np.array(interp(InterPoint, fpr/ncontrol_split[0], tpr/cases))
    auc = np.round(Trapezoidal(InterPoint, hitrate),2)
    hitrate = np.append(0, hitrate)
    InterPoint_zero = np.append(0, InterPoint)
    sum_tpr_fpr = np.sum([fpr_weight, tpr_weight], axis=0)
    w = np.round(weights_scale[0],2)
    z = np.round(thresholds_split[0],2)
    fig = plt.figure()
    plt.plot(InterPoint_zero,hitrate)
    plt.plot([0,1],[0,1], '--', color='grey')
    plt.ylabel('Sensitivity')
    plt.xlabel('1 - Specificity')
    plt.text(0.7,0.2,'AUC: {:3.2f}'.format(auc))
    plt.text(0.17,0.95,'z: %s'%(z))
    plt.text(0.0,0.95,'w: {:3.2f}'.format(w))
    name = 'animate_0.png'
    fig.savefig(path + name)
    plt.close()

    for i in range(1,(indxsetC.shape[0])):
    
        sorted_split_element = np.sort(np.append(Split_classes_predictor[i],0))
        diff_split_element = np.subtract(sorted_split_element[1:],sorted_split_element[:-1])
        m = diff_split_element.shape[0]
        sum_indicator = np.repeat(np.arange(m,0,-1), diff_split_element, axis=0)
        seq_change =  sum_indicator.shape[0]
        tpr_weight[0:seq_change] = np.subtract(np.array(tpr_weight[0:seq_change]), sum_indicator) 
        fpr = np.subtract(sum_tpr_fpr, tpr_weight) / ncontrol_split[i]
    
    
        hitrate = interp(InterPoint, np.array(fpr[::-1])  ,np.array(tpr_weight[::-1]) / (n-ncontrol_split[i])) 
        auc = np.round(Trapezoidal(InterPoint, hitrate),2)
        hitrate = np.append(0, hitrate)
        w = np.round(weights_scale[i],2)
        z = np.round(thresholds_split[i],2)
        fig = plt.figure()
        plt.plot(InterPoint_zero,hitrate)
        plt.plot([0,1],[0,1], '--', color='grey')
        plt.ylabel('Sensitivity')
        plt.xlabel('1 - Specificity')
        plt.text(0.7,0.2,'AUC: {:3.2f}'.format(auc))
        plt.text(0.17,0.95,'z: %s'%(z))
        plt.text(0.0,0.95,'w: {:3.2f}'.format(w))
        name = 'animate_' + str(i) + '.png'
        fig.savefig(path + name)
        plt.close()

    fig = plt.figure()    
    uroc(response, predictor) 
    name = 'animate_' + str(indxsetC.shape[0]) + '.png'
    plt.title('UROC curve')
    fig.savefig(path+name)
    plt.close()

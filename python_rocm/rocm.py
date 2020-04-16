# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:03:05 2020

@author: walz
"""

import numpy as np
from scipy.stats import rankdata
from scipy import interp
import matplotlib.pyplot as plt
import imageio

from uroc import uroc_app, Trapezoidal

def rocm(response, predictor, path, fps = 10, b=1):
    """
    Creates a ROC movie.

    Visualizes the performances of predictors for real valued forecasting problems. 

    Parameters
    ----------
    response : 1D array_like, 1-D array containing obervation. Need to have the same length in the ``axis`` dimension as b.
	predictor : 1D array_like, 1-D array containing forecast for observation a.
    path: String, Example: /home/animation.gif 
       
    Returns
    -------
    Gif animation
    """ 
    response = np.array(response)
    predictor = np.array(predictor)
    
    if np.issubdtype(response.dtype, np.number) == False:
        raise ValueError('response must be numeric')
    if np.issubdtype(predictor.dtype, np.number) == False:
        raise ValueError('predictor must be numeric')
        
    n = response.shape[0]
    if len(predictor) != n:
        raise ValueError('response and predictor should have the same length')
    if b <= 0 or b > n or np.round(b) !=b:
        raise ValueError("invalid value for b")    
    
    response_sorted_indices = np.argsort(response)
    response_sorted = response[response_sorted_indices]
    predictor_sorted = predictor[response_sorted_indices]
    response_unique, response_unique_index = np.unique(response_sorted, return_index=True)
    N = response_unique.shape[0]-1
    if N == 0:
        raise ValueError('response must have more than one level')
    a = 400
    b = 1
    if a > N:
        indx_setC = np.arange(1, (N+1), 1)
        indxuroc = indx_setC
        
    else:
        if N <= 1000:
            split = 1
        elif N <= 10000:
            split = 10 
        elif N <= 100000:
            split = 500
        elif N <= 1000000:
            split = 5000
    #duration = 1/20
        s = np.floor((N - 1) / (a - 1))
        hh = (1 + (a - 1) * s)
        indx_setCa = np.arange(1, hh , s)
        indx_setCauroc = np.arange(1, N, split)
        class_length = np.subtract(np.append(response_unique_index[2:],n),response_unique_index[1:])
        indx_setCb = np.where(class_length>n/b)
        indx_setC = np.sort(np.unique(np.concatenate((indx_setCa, indx_setCb), axis = None)))
        indxuroc = np.sort(np.unique(np.concatenate((indx_setCauroc, indx_setCb), axis = None)))

    ncontrol = (response_unique_index)[1:]
    ncontrol_uroc = response_unique_index[indxuroc.astype(int)]
    ncontrol_split = response_unique_index[indx_setC.astype(int)]
    thresholds_split = response_unique[indx_setC.astype(int)]
    weights_split = np.multiply(ncontrol_split, n-ncontrol_split)
    weights_all = np.multiply(ncontrol, n-ncontrol)
    weights_scale = weights_split / np.max(weights_all)


    classes_predictor = rankdata(predictor_sorted, method='dense')
    Split_classes_uroc = np.split(classes_predictor[:response_unique_index[-1]],ncontrol_uroc[:-1])
    Split_classes_predictor = np.split(classes_predictor[:response_unique_index[-1]],ncontrol_split[:-1])
    # First roc curve
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

    cases = n- ncontrol_uroc[0]
    hitrate = np.array(interp(InterPoint, fpr/ncontrol_uroc[0], tpr/cases))

    auc = np.round(Trapezoidal(InterPoint, hitrate),2)
    hitrate = np.append(0, hitrate)
    InterPoint_zero = np.append(0, InterPoint)
    sum_tpr_fpr = np.sum([fpr_weight, tpr_weight], axis=0)
    lenindx = indxuroc.shape[0]
    tpru = list(tpr) 
    fpru = list(fpr)
    far_uroc, hit_uroc = uroc_app(ncontrol_uroc, tpru, fpru, n, Split_classes_uroc, lenindx)

    w = np.round(weights_scale[0],2)
    z = np.round(thresholds_split[0],2)
    images = []
    fig = plt.figure(figsize=(6,6))
    plt.plot(InterPoint_zero,hitrate)
    plt.plot([0,1],[0,1], '--', color='grey')
    plt.ylabel('Sensitivity')
    plt.xlabel('1 - Specificity')
    plt.text(0.7,0.2,'AUC: {:3.2f}'.format(auc))
    plt.text(0.17,0.95,'z: %s'%(z))
    plt.text(0.0,0.95,'w: {:3.2f}'.format(w))
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    images.append(image)
    plt.close()


    for i in range(1,(indx_setC.shape[0])):
    
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
        fig = plt.figure(figsize=(6,6))
        plt.plot(InterPoint_zero,hitrate)
        plt.plot([0,1],[0,1], '--', color='grey')
        plt.ylabel('Sensitivity')
        plt.xlabel('1 - Specificity')
        plt.text(0.7,0.2,'AUC: {:3.2f}'.format(auc))
        plt.text(0.17,0.95,'z: %s'%(z))
        plt.text(0.0,0.95,'w: {:3.2f}'.format(w))
        fig.canvas.draw()       # draw the canvas, cache the renderer
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)
        plt.close()


    cpa_approx = np.round(Trapezoidal(far_uroc, hit_uroc),2)
    fig = plt.figure(figsize=(6,6))
    plt.plot(far_uroc,hit_uroc)
    plt.plot([0,1],[0,1], '--', color='grey')
    plt.ylabel('Sensitivity')
    plt.xlabel('1 - Specificity')
    plt.text(0.7,0.2,'CPA: {:3.2f}'.format(cpa_approx))
    plt.title('UROC curve')
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    images.append(image)
    plt.close()
    

    imageio.mimsave(path, [images[i] for i in (range((len(images))))], fps=fps, loop=1)  

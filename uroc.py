# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:41:40 2020

@author: walz
"""

import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from scipy.stats import rankdata

def uroc(response, predictor):
    """
    Compute uroc curve.

    Visualizes the performances of predictors for real valued forecasting problems. 

    Parameters
    ----------
    response : 1D array_like, 1-D array containing obervation. Need to have the same length in the ``axis`` dimension as b.
	predictor : 1D array_like, 1-D array containing forecast for observation a.
       
    Returns
    -------
    Plot of uroc curve
    """  
    response_sorted_indices = np.argsort(response)
    response_sorted = response[response_sorted_indices]
    predictor_sorted = predictor[response_sorted_indices]
    farate, hitrate = compute_uroc_approx(response_sorted, predictor_sorted)
    cpa_approx = np.round(Trapezoidal(farate, hitrate),2)
    plt.plot(farate,hitrate)
    plt.plot([0,1],[0,1], '--', color='grey')
    plt.ylabel('Sensitivity')
    plt.xlabel('1 - Specificity')
    plt.text(0.7,0.2,'CPA: {:3.2f}'.format(cpa_approx))


def compute_uroc_approx(response, predictor):
    n = response.shape[0]
    response_unique, response_unique_index = np.unique(response, return_index=True)
    N = response_unique.shape[0]
    ncontrol = (response_unique_index)[1:]
    ncases = n - ncontrol
    weights_all = np.multiply(ncases, ncontrol)
    classes_predictor = rankdata(predictor, method='dense')
    Split_classes_predictor = np.split(classes_predictor[:response_unique_index[-1]], response_unique_index[1:-1])

    # compute first roc curve
    # response_binary = np.where(np.array(response) > response_unique[0],1,0)
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
    tpr_interpolated = np.array(interp(InterPoint, fpr, tpr)) * ncontrol[0]
    sum_tpr_fpr = np.sum([fpr_weight, tpr_weight], axis=0)

    for i in range(1, (N - 1)):
        sorted_split_element = np.sort(np.append(Split_classes_predictor[i], 0))
        diff_split_element = np.subtract(sorted_split_element[1:], sorted_split_element[:-1])
        m = diff_split_element.shape[0]
        sum_indicator = np.repeat(np.arange(m, 0, -1), diff_split_element, axis=0)
        seq_change = sum_indicator.shape[0]
        tpr_weight[0:seq_change] = np.subtract(np.array(tpr_weight[0:seq_change]), sum_indicator)
        fpr = np.subtract(sum_tpr_fpr, tpr_weight) / ncontrol[i]
        tpr_interpolated = interp(InterPoint, np.array(fpr[::-1]),
                                  np.array(tpr_weight[::-1]) * ncontrol[i]) + tpr_interpolated
        # final output
    tpr_interpolated_weight = tpr_interpolated / np.sum(weights_all)
    return (np.insert(InterPoint, 0, 0), np.insert(tpr_interpolated_weight, 0, 0))

def Trapezoidal(farate, hitrate):
    diff_farate = np.subtract(farate[1:],farate[:-1])
    means = np.sum([hitrate[1:],hitrate[:-1]], axis=0)*0.5
    return(np.sum(means * diff_farate))

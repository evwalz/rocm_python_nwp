# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:41:40 2019

@author: walz
"""

import numpy as np
from scipy.stats import rankdata

def cpa(a, b):
    """
    Calculate CPA coefficient.

    CPA is attains values between zero and one. Weighted probability of concordance. 

    Parameters
    ----------
    a : 1D array_like, 1-D array containing obervation. Need to have the same length in the ``axis`` dimension as b.
	b : 1D array_like, 1-D array containing forecast for observation a.
       
    Returns
    -------
    correlation : float
        CPA coefficient 
    """    
    a = np.asarray(a)
    if a.ndim > 1:
        raise ValueError("CPA only handles 1-D arrays of responses")

    b = np.asarray(b)
	
    if b.ndim > 1:
        ValueError("CPA only handles 1-D arrays of forecasts")   
  
    	# check for nans
    if np.isnan(np.sum(a)) == True:
        ValueError("response contains nan values")
		
    if np.isnan(np.sum(b)) == True:
        ValueError("forecast contains nan values")
	
    responseOrder = np.argsort(a)
    responseSort = a[responseOrder] 
    forecastSort = b[responseOrder]                
    forecastRank = rankdata(forecastSort, method='average')
    responseRank = rankdata(responseSort, method='average')
    responseClass = rankdata(responseSort, method='dense')
    
    return(np.cov(responseClass,forecastRank)[0][1]/np.cov(responseClass,responseRank)[0][1]+1)/2 
	
 
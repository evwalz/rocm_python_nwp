import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rankdata


class uroc_object:
    def __init__(self, farate, hitrate):
        self.farate = farate
        self.hitrate = hitrate
    
    def plot(self):
        farate = self.farate
        hitrate = self.hitrate
        cpa = trap(farate, hitrate)
        cpa = np.round(cpa, 2)
        plt.plot(farate,hitrate)
        plt.plot([0,1],[0,1], '--', color='grey')
        plt.ylabel('Sensitivity')
        plt.xlabel('1 - Specificity')
        plt.title("UROC curve")
        plt.text(0.7,0.2,'CPA: {:3.2f}'.format(cpa))



def uroc (response, predictor):
    """
    computes farate and hitrate of uroc curve

    Parameters
    ----------
    response : np array
        1D array of responses
    predictor : np array
        1D array of predictions

    Returns
    -------
    Object of class idr_object:
        farate : 1D array of farate
        hitrate : 1D array of hitrate
    """
    response = np.asarray(response)
    predictor = np.asarray(predictor)
    
    if response.ndim > 1:
                raise ValueError("response must be a 1-D array")
    if predictor.ndim > 1:
                raise ValueError("predictor must be a 1-D array")
    if np.isnan(np.sum(response)) == True:
        ValueError("response contains nan values")
		
    if np.isnan(np.sum(predictor)) == True:
        ValueError("predictor contains nan values")
    
    n = response.shape[0]
    response_sorted_indices = np.argsort(response)
    response_sorted = response[response_sorted_indices]
    predictor_sorted = predictor[response_sorted_indices]
    thresholds, thresholds_index = np.unique(response_sorted, return_index = True)
    N = thresholds.size
    
    if N < 2:
        raise ValueError("response must have more than one level")
    ncontrol = thresholds_index[1:]
    
    weights = (response.size - ncontrol) * ncontrol
    weights_s = np.sum(weights)
    classes_predictor = rankdata(predictor, method='dense')
    Split_classes_predictor = np.split(classes_predictor[:thresholds_index[-1]], thresholds_index[1:-1])

    # compute first roc curve
    response_binary = np.ones(n)
    response_binary[(n-ncontrol[0]):n] = 0
    
    order_predictor = predictor.argsort()[::-1]
    #response_binary = response_binary[order_predictor] 
    #response_binary = np.where(np.array(response[order_predictor]) > response_unique[0], 1, 0)
    predictor_sorted = predictor[order_predictor][::-1]
    predictor_unique, predictor_unique_index = np.unique(predictor_sorted, return_index=True)
    dups = (n - 1) - predictor_unique_index[::-1]
    tpr = np.insert(np.cumsum(response_binary)[dups], 0, 0)
    fpr = np.insert(np.cumsum(response_binary == 0)[dups], 0, 0)
    tpr_weight = tpr[::-1]
    fpr_weight = fpr[::-1]
    InterPoint = np.arange(0, 1001, 1) * 0.001
    tpr_interpolated = np.array(np.interp(InterPoint, fpr, tpr)) * ncontrol[0]
    sum_tpr_fpr = np.sum([fpr_weight, tpr_weight], axis=0)

    for i in range(1, (N - 1)):
        sorted_split_element = np.sort(np.append(Split_classes_predictor[i], 0))
        diff_split_element = np.diff(sorted_split_element)
        m = diff_split_element.shape[0]
        sum_indicator = np.repeat(np.arange(m, 0, -1), diff_split_element, axis=0)
        seq_change = sum_indicator.shape[0]
        tpr_weight[0:seq_change] = np.subtract(np.array(tpr_weight[0:seq_change]), sum_indicator)
        fpr = np.subtract(sum_tpr_fpr, tpr_weight) / ncontrol[i]
        tpr_interpolated = np.interp(InterPoint, np.array(fpr[::-1]),
                                  np.array(tpr_weight[::-1]) * ncontrol[i]) + tpr_interpolated
        # final output
    tpr_interpolated_weight = tpr_interpolated / weights_s
    return(uroc_object(farate = np.insert(InterPoint, 0, 0), hitrate = np.insert(tpr_interpolated_weight, 0, 0)))



# compute approx to cpa
def trap(farate, hitrate):
    diff_farate = np.subtract(farate[1:],farate[:-1])
    means = np.sum([hitrate[1:],hitrate[:-1]], axis=0)*0.5
    return(np.sum(means * diff_farate))




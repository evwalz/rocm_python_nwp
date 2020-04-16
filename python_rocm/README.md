## ROCM, UROC and CPA

Python functions of ROCM, UROC curve and CPA. The essential input to these functions is a response vector (obervations) and the associated prediction vector (forecast).  

The files:

1. **cpa:**

computes the coefficient of predictive ability (cpa).

2. **uroc:**

Creates a uroc curve.

3. **rocm:**

Creates a GIF animation of a roc movie.

4. **rocm_and_uroc:**

Creates GIF animation of a roc movie and PNG file of uroc curve. For large data it uses a faster but more imprecise algorithm to compute uroc curve 




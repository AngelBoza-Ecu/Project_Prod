#%%
#Import libraries
import numpy as np
import pandas as pd
from functions import aof,j

#%%
def pwf_darcy(q_test, pwf_test, q, pr, pb):
    pwf = pr - (q / j(q_test, pwf_test, pr, pb))
    return pwf

#%%
# Pwf when Pr < Pb (Saturated reservoir)
def pwf_vogel(q_test, pwf_test, q, pr, pb):
    pwf = 0.125 * pr * (-1 + np.sqrt(81 - 80 * q / aof(q_test, pwf_test, pr, pb)))
    return pwf

#%%
# Friction factor (f) from darcy-weishbach equation
def f_darcy(Q, ID, C=120):
    f = (2.083 * (((100 * Q)/(34.3 * C))**1.85 * (1 / ID)**4.8655)) / 1000
    return f

#%%
# SGOil using API
def sg_oil(API):
    SG_oil = 141.5 / (131.5 + API)
    return SG_oil

#%%
# SG average of fluids
def sg_avg(API, wc, sg_h2o):
    sg_avg = wc * sg_h2o + (1-wc) * sg_oil(API)
    return sg_avg

#%%
# Average Gradient using fresh water gradient (0.433 psi/ft)
def gradient_avg(API, wc, sg_h2o):
    g_avg = sg_avg(API, wc, sg_h2o) * 0.433
    return g_avg

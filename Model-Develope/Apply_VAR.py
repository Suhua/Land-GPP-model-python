import numpy as np
from numpy import ma
import pandas as pd
from scipy import io,misc
from scipy.io import netcdf
import datetime
import matplotlib.pylab as plt
import os
import glob
from netCDF4 import Dataset, netcdftime



#-------Define internal functions-----------------------------------------------------------------------------------------------
def look_up(value):
    lc_dic={0:'WAT',1:'ENF',2:'EBF',3:'DNF',4:'DBF',5:'MF',6:'CSH',7:'OSH',8:'WSA',\
    9:'SAV',10:'GRA',11:'WET',12:'CRO',13:'URB',14:'NEM',15:'SNO',16:'BAR'}
    return lc_dic[value]

def co_effRead(veg):
    os.chdir(r'G:\Research\modelling\model_development\data\biomeRegression')
    filename=[veg,'_reg.xlsx']
    model_fit=pd.read_excel(''.join(filename),sheetname=0,header=None)
    data=model_fit.as_matrix()
    model_fit=pd.DataFrame(data,columns=['alpha','evi','par','ta','spei','var_coe','model_result'])
    alpha=model_fit['alpha'].as_matrix()
    coeff=model_fit['var_coe'].dropna().as_matrix()
    return alpha,coeff

def mod_fit(alpha,coeff,month,r_num,c_num):
    os.chdir(r'G:\Research\modelling\model_development\data\varMap')
    mon=month-1
    evi=np.load('evi_{0}.npy'.format(mon))
    par=np.load('par_{0}.npy'.format(mon))
    ta=np.load('ta_{0}.npy'.format(mon))
    spei=np.load('spei_{0}.npy'.format(mon))
    alpha_pred=coeff[0]+coeff[1]*alpha[mon]+coeff[2]*evi[r_num,c_num]+\
        coeff[3]*par[r_num,c_num]+coeff[4]*ta[r_num,c_num]+coeff[5]*spei[r_num,c_num]
    return alpha_pred

def mod_fit_EBF(alpha,coeff,month,r_num,c_num):
    os.chdir(r'G:\Research\modelling\model_development\data\varMap')
    mon=month-1
    evi=np.load('evi_{0}.npy'.format(mon))
    par=np.load('par_{0}.npy'.format(mon))
    ta=np.load('ta_{0}.npy'.format(mon))
    spei=np.load('spei_{0}.npy'.format(mon))
    evi_lag=np.load('evi_{0}.npy'.format(mon-1))
    par_lag=np.load('par_{0}.npy'.format(mon-1))
    ta_lag=np.load('ta_{0}.npy'.format(mon-1))
    spei_lag=np.load('spei_{0}.npy'.format(mon-1))
    alpha_pred=coeff[0]+coeff[1]*alpha[mon]+coeff[2]*evi[r_num,c_num]+\
    coeff[3]*par[r_num,c_num]+coeff[4]*ta[r_num,c_num]+coeff[5]*spei[r_num,c_num]+\
    coeff[6]*alpha[mon-1]+coeff[7]*evi_lag[r_num,c_num]+\
    coeff[8]*par_lag[r_num,c_num]+coeff[9]*ta_lag[r_num,c_num]+coeff[10]*spei_lag[r_num,c_num]
    return alpha_pred

#--------Main function starts here--------------------------------------------------------------------------------------

lc=io.loadmat('G:\Research\Gridded Data\PDSI\lc.mat')['lc']
lc_valid={1:'ENF',2:'EBF',3:'DBF',4:'DBF',6:'CSH',7:'OSH',8:'WSA',\
    9:'SAV',10:'GRA',11:'WET',12:'CRO'}

for mon in range(1,4):
    alpha_pred=np.zeros([360,720])
    for r in range(0,360):
        for c in range(0,720):
            veg=look_up(lc[r,c])
            if veg is 'EBF':
                alpha,coeff=co_effRead(veg)

                if mon>2:
                    alpha_pred[r,c]=mod_fit_EBF(alpha,coeff,mon,r,c)
                else:
                    alpha_pred[r,c]=alpha[mon-1]
            if veg in lc_valid.values():
                alpha,coeff=co_effRead(veg)
                # print alpha,coeff
                if mon>1:
                    alpha_pred[r,c]=mod_fit(alpha,coeff,mon,r,c)
                else:
                    alpha_pred[r,c]=alpha[mon-1]
            else:
                alpha_pred[r,c]=0

    if mon>1:
       alpha_pred.dump('alpha_pred_{0}.npy'.format(mon))




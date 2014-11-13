
import pandas as pd
import matplotlib.pylab as plt
import statsmodels.api as sm
import numpy as np

alpha=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\alpha_sum.csv',sep=',',header=None)
ta=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\ta_sum.csv',sep=',',header=None)
precip=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\precip_sum.csv',sep=',',header=None)
vpd=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\vpd_sum.csv',sep=',',header=None)

# alpha.plot(kind='bar')
# pd.DataFrame(ta,index=ta[:,0]).plot(kind='bar')
# print alpha,ta, precip
y=alpha
y=pd.DataFrame(alpha).icol(1)
# y.plot(kind='bar')
# plt.show()
ta=pd.DataFrame(ta).icol(1)
precip=pd.DataFrame(precip).icol(1)
vpd=pd.DataFrame(vpd).icol(1)
# x1=ta
# x1.pop(1)
# y.pop(1)
# x1.pop(7)
# y.pop(7)
# x1.pop(10)
# y.pop(10)

x2=precip
# x2.pop(1)
# x2.pop(7)
# x2.pop(10)

x3=vpd
# x=np.array(x1,x3)
X=sm.add_constant(x3)
# print precip
# # fit a OSL model with intercept on Ta and Precip
est=sm.OLS(y,X).fit()
print est.summary()

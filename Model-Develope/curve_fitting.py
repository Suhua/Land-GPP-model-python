import time
import numpy as np

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
ticks=time.clock()

nee=np.load('nee_US_KS2.npy')
ppfd=np.load('ppdf_US_KS2.npy')


# ppfd=np.ma.masked_where(ppfd,ppfd<0)
# nee=np.ma.masked_where(nee,ppfd<0)
print nee, ppfd
def func(x,a,b):
    return b-a*x
popt,pcov=curve_fit(func,ppfd,nee)
print popt

print np.sqrt(np.diag(pcov))

plt.plot(ppfd,nee,'b*',ppfd,popt[1]-popt[0]*ppfd,'r--')
plt.show()
print time.clock()-ticks

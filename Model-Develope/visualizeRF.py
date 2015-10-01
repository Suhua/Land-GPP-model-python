import numpy as np
import matplotlib.pylab as plt
import glob
from mpl_toolkits import basemap
from scipy import io
list=glob.glob('*.npy')

newList=sorted(list[1:])

id=[]
for i in range(0,len(newList)):
    name=newList[i].split('_')[-1].split('.')[0]
    # print name
    id.append(int(name[2:]))
dic=dict(zip(id,newList))
# print dic.values()
lc = io.loadmat('G:\Research\Gridded Data\PDSI\lc.mat')['lc']
i=0
for path in dic.values():
    print path
    data=np.load(path)
    im=np.ma.masked_where(data==0,data)
    im=np.ma.masked_where(lc==16,im)
    fig = plt.figure()
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    lats = np.linspace(90, -90, 360)
    lons = np.linspace(-180, 180, 720)
    m = basemap.Basemap(projection='robin', lon_0=0.0, resolution='c')
    m.drawparallels(np.arange(-90, 90, 30))
    m.drawmeridians(np.arange(-180, 180, 60))
    m.drawcoastlines()
    lons, lats = np.meshgrid(lons, lats)
    im = m.pcolormesh(lons, lats, im, cmap=plt.cm.jet, latlon=True)
    mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_title('Predicted LUE map by Random Forest Regress', fontsize=24)
    cb = m.colorbar(im, 'right', size='3%')
    cb.set_clim(vmin=0, vmax=4)
    # plt.show()

    ax.set_title('{0} LUE by random forest regression'.format(mon[i]), fontsize=16)
    plt.savefig('LUErf_{0}.jpg'.format(i))

    i+=1

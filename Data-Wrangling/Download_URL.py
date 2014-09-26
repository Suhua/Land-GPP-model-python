__author__ = 'swei'
import os
import urllib
def filename(yr,mt):
if mt>9:
fn='MOD16A2_ET_0.05deg_GEO_200{0}M{1}.tif'.format(yr,mt)
else:
fn='MOD16A2_ET_0.05deg_GEO_200{0}M0{1}.tif'.format(yr,mt)
return fn
RUL='ftp://ftp.ntsg.umt.edu/pub/MODIS/NTSG_Products/MOD16/MOD16A2_MONTHLY.MERRA_GMAO_1kmALB/GEOTIFF_0.05degree/'
for yr in range(4,6):
for mt in range(1,13):
f=filename(yr,mt)
fpath=os.path.join(RUL,f)
urllib.urlretrieve(fpath,f)

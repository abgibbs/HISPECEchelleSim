# make point source spectrum with unique fluxes to pass to pyechelle
# ask ashley for psg file or use your own telluric or psg file
import numpy as np
import matplotlib.pylab as plt
import pandas as pd
from astropy.io import fits

plt.ion()

specs = ['yJ','HK']

telluric_file = './psg_out_2020.08.02_l0_800nm_l1_2700nm_res_0.001nm_lon_204.53_lat_19.82_pres_0.5826.fits'
data      = fits.getdata(telluric_file)

_,indx     = np.unique(data['Wave/freq'],return_index=True)

x         = data['Wave/freq'][indx][::2]
y         = data['Total'][indx][::2]
h2o       = data['H2O'][indx][::2]
co        = data['CO'][indx][::2]
o2        = data['O2'][indx][::2]

iHK = np.where((x>1460) & (x<2500))[0]
iyJ = np.where((x>970) & (x<1350))[0]

np.savetxt('telluric_wave_flux_yJ.csv',np.vstack((x[iyJ]/1000,y[iyJ])).T,delimiter=',')
np.savetxt('telluric_wave_flux_HK.csv',np.vstack((x[iHK]/1000,y[iHK])).T,delimiter=',')

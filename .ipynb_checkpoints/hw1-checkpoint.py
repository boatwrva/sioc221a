# SIOC221: Data Analysis 
# HW1

import numpy as np 
import matplotlib.pyplot as plt
import netCDF4
import datetime as dt 
import matplotlib.dates as mdates
import pandas as pd 


# problem1: Download 2021 SST from Scripps Pier

url = 'http://thredds.sccoos.org/thredds/dodsC/autoss/scripps_pier-2021.nc'
nc = netCDF4.Dataset(url)

time = nc['time'][:]
temp = nc['temperature'][:]
sal = nc['salinity'][:]
p = nc['pressure'][:]
chl = nc['chlorophyll'][:]
station = nc['station'][:]
lon = nc['lon'][:]; lat = nc['lat'][:]
zeta = nc['depth'][:]

# time units = 'seconds since 1970-01-01 00:00:00 UTC'

start_time = dt.datetime(1970,1,1)
time_array = np.array(time.data)
dates = [start_time + dt.timedelta(seconds=float(tt)) for tt in time_array]


# part a: produce line plot of 2021 temps

fig,ax = plt.subplots(1,1,figsize=(12,6))
plt.scatter(dates,temp,c=temp,cmap='Spectral_r') 
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B-%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gcf().autofmt_xdate()
plt.show()


# part b: compute mean and stdev 

temp_mean = np.nanmean(temp)
temp_std = np.std(temp) 



# part c: empirical probability density function (not sure how to do this)



# problem2: extending the record

years = np.arange(2005,2022) # going from 2005 to 2021
years = [str(yy) for yy in years]

url_base = 'http://thredds.sccoos.org/thredds/dodsC/autoss/scripps_pier-'
urls = [url_base+yy+'.nc' for yy in years]
time = np.array([])
temp = np.array([])
sal = np.array([])
p = np.array([])
chl = np.array([])
station = np.array([])
lon = np.array([]); lat = np.array([])
zeta = np.array([])

for n,fn in enumerate(urls):
    # read current file: 
    nc = netCDF4.Dataset(fn)
    t_now = nc['time'][:]
    t_here = nc['temperature'][:]
    s_here = nc['salinity'][:]
    p_here = nc['pressure'][:]
    c_here = nc['chlorophyll'][:]
    s_here = nc['station'][:]
    lon_here = nc['lon'][:]; lat_here = nc['lat'][:]
    z_here = nc['depth'][:]

    # append to extended record
    time = np.append(time,t_now)
    temp = np.append(temp,t_here)
    sal = np.append(sal,s_here)
    p = np.append(p,p_here)
    chl = np.append(chl,c_here)
    station = np.append(station,s_here)
    lon = np.append(lon,lon_here); lat = np.append(lat,lat_here)
    zeta = np.append(zeta,z_here)

s0 = dt.datetime(1970,1,1)
dates = [s0+dt.timedelta(seconds=float(tt)) for tt in time.data]
SP = pd.DataFrame({'dates':np.array(dates),'temp':temp,'p':p,'chl':chl}) # scripps pier df
# information I couldn't add because size requirements: 'sal':sal, 'station':station,'lon':lon,'lat':lat,'zeta':zeta}) # scripps pier df

# Q2 part a: do the same thing


# compute mean and stdev - but excluding anaomalous data

SP.temp[SP.temp>50] = np.nan
temp[temp>50] = np.nan

temp_mean = np.nanmean(SP.temp)
temp_std = np.std(SP.temp)


fig,ax = plt.subplots(1,1,figsize=(12,6))
ax.plot(dates,temp,color='tab:red') 
m = ax.axhline(y=temp_mean,linestyle='--',color='blue',label='Mean');
s1 = ax.axhline(y=temp_mean+temp_std,linestyle='--',color='tab:blue',alpha=0.7,label='Standard Deviation')
s2 = ax.axhline(y=temp_mean-temp_std,linestyle='--',color='tab:blue',alpha=0.7,label='Standard Deviation')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')) # b is short, B is long, m is number
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.tick_params(axis='x',rotation=45)
ax.set(title='Scripps Pier Temperature Measurements',xlabel='Time',ylabel=r'Temperature [ $ ^{\circ} $C]')

# fig.autofmt_xdate()
# ax.set_ylim([10,30])
ax.grid(which='major',axis='x',color='tab:gray')
handles = ['Mean','Standard Deviation']
ax.legend([m,s2],handles,loc='best')
plt.show()

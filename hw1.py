# SIOC221: Data Analysis 
# HW1

import numpy as np 
import matplotlib.pyplot as plt
import netCDF4
import datetime as dt 
import matplotlib.dates as mdates


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


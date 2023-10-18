# function for downloading temp data 

def pier_temp_download(year): 
	# created by: Victoria Boatwright; October 2023; SIOC 221A HW2
	
    # years should be an array or list of (number) years of interest
        
    import numpy as np 
    import datetime as dt 
    import pandas as pd 
    
    year_string = str(year)
    url_base = 'http://thredds.sccoos.org/thredds/dodsC/autoss/scripps_pier-'
    url = url_base+year_string+'.nc'
    

    # read current file: 
    nc = netCDF4.Dataset(url)
    # if you want the information printed as you go: print(nc)
    
    # only interested in time and temp
    time = nc['time'][:]
    temp = nc['temperature'][:]
    pressure = nc['pressure'][:]
    
    # convert to datetimes based on units of 'seconds since 1970-01-01'
    s0 = dt.datetime(1970,1,1)
    dates = [s0+dt.timedelta(seconds=float(tt)) for tt in time.data]

    return dates, temp, pressure 

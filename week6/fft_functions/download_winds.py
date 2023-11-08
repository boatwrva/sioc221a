# function to download wind data and fill missing values 

def download_winds(url=links[0],plotting=0): 
    import numpy as np 
    import matplotlib.pyplot as plt
    import xarray as xr 
    import datetime as dt 

    
    s0 = dt.datetime(1950,1,1); 

    nc = netCDF4.Dataset(url)
    # making a date array based on time units from netcdf file
    time = nc['TIME'][:]; dates = [s0+dt.timedelta(days=float(tt)) for tt in time]
    ht = nc['HEIGHT'][:]
    lon = nc['LONGITUDE'][:]; lat = nc['LATITUDE'][:]

    wind = nc['WSPD'][:]; wind[wind<0] = np.nan # make nan when not physical 
    wind = np.squeeze(wind.data) # make into a 1D array (before it was a (47605,1) shaped array)
    # make into a xarray so we can use interpolate_na function 
    dw = xr.DataArray(data=wind.data,dims="time", coords={"time": time})
    dw = dw.interpolate_na(dim='time',method="linear")
    wind = dw.values
    
    u = nc['UWND'][:]; u[u<=-998] = np.nan # make nan when fillValue
    u = np.squeeze(u.data) # make into a 1D array (before it was a (47605,1) shaped array)
    du = xr.DataArray(data=u.data,dims="time", coords={"time": time})
    du = du.interpolate_na(dim='time',method="linear") 
    u = du.values
    
    v = nc['VWND'][:]; v[v<=-998] = np.nan # make nan when fillValue
    v = np.squeeze(v.data) # make into a 1D array (before it was a (47605,1) shaped array)
    dv = xr.DataArray(data=v.data,dims="time", coords={"time": time})
    dv = dv.interpolate_na(dim='time',method="linear") 
    v = dv.values
    
    # plot if desirable
    if plotting == 1: 
        plots = [wind,u,v]; labels = ['wind speed [m/s]','u [m/s]','v [m/s]']; titles = ['Total Wind Speed', 'Zonal Wind', 'Meridionial Wind']
        fig,axes = plt.subplots(3,1,figsize=(14,20))
        fig.suptitle('Raw Wind Speed Timeseries',y=0.95,fontweight='bold')
        for nn,ax in enumerate(axes): 
            ax.grid()
            ax.plot(dates,plots[nn])
            ax.set(ylabel=labels[nn]); # ax.set(title=titles[nn])
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.tick_params(axis='x', labelrotation = -45)
        plt.show()
    
    return time, wind, u, v
    
    
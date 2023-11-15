# function for fft and spectra analysis 

def fft_analysis(data,time,demean=1,detrend=1,hanning=1,all_pars=0):
    # specifications for inputs: 
    # data_array should be size = (segments,data_in_segment); each data_in_segment column should be the same length
    # time array = should be the same size as data_array, could adapted for just a 1D vector. 
    # aka: you must window properly before using this function 
    # then, selecting whether to demean, detrend, hanning window, etc. 

    # returns: 
    # freqs: frequency array associated with spectrum/FFT
    # avg_fft: average fourier transform to plot (real & complex)
    # tot_amp: averaged spectrum 
    # err_low, err_high = high and low errors of dataset 

    import numpy as np 
    import matplotlib.pyplot as plt
    import xarray as xr 
    import datetime as dt 
    import scipy 
    from scipy import fft 
    from scipy import stats 
    
    
    # all segment lengths should be the same 
    N = len(data[0,:])  # == num_samples in each _window_
    deltat = np.diff(time)
    step = np.nanmean(deltat) # step size (in days)
    Nyq = 1/(2*step) # Nyquist frequency
    period = step*N # this is the entire segment period (in days)
    df = 1/period # fundamental frequency
    segs = len(data[:,0]) # total number of segment 
    M = segs
    
    # start workflow: analyze each segment individually 

    # fft & spectra of interest to be averaged 
    fft_oi = np.zeros((segs,N)) # real+complex FFT 
    amp_oi = np.zeros((segs,int(N/2))) # real spectra 
    
    # loop through segments
    for nn in np.arange(0,segs):
        segment = data[nn,:]
        segtime = time[nn,:]
    
        # demean & detrend 
    
        # calculate mean and linear trend 
        AA = np.array([np.ones(N), segtime]).T
        x = np.dot(np.linalg.inv(np.dot(AA.T, AA)), np.dot(AA.T, segment))
        mean = x[0]; trend = x[1]

        if demean==1: 
            segment = segment-mean # demean by calculated mean 
        
        if detrend==1: 
            segment = segment-trend*segtime # detrend from calculated trend
        
        if hanning==1: 
            # hanwin = np.cos(np.pi*segtime / period)**2 # calculate hanning window - unreliable: you want an exactly centered hanning window, so use a known independent variable
            x = np.linspace(-0.5, 0.5, N) # specify known Hanning domain
            hanwin = (np.cos(x*np.pi))**2 # Hanning values
            segment = segment*hanwin*np.sqrt(8/3) # normalize hanning window by sqrt(8/3)
            
        # compute each segment spectrum 
        # fourier transform
        fft = scipy.fft.fft(segment); 
        freq = scipy.fft.fftfreq(N,step); freq = scipy.fft.fftshift(freq); real_freq = freq[freq>=0]
        fftplot = scipy.fft.fftshift(fft)
        norm_fft = 1.0/N * np.abs(fftplot) # normalizing shifted FFT 
    
        r_idx = np.nonzero(freq>=0)
        amp = (norm_fft[r_idx])**2 # only selecting >0 to ignore complex (symmetric about x=0) - then square for amp

        # do the steps for the spectrum: 
        # normalization already done above
        amp = amp*2 # account for discarded redundant complex FFT coefficients 
        amp = amp/df # spectrum is normalized by fundamental freq
        
        fft_oi[nn,:] = norm_fft
        amp_oi[nn,:] = amp
    
        # inner loop parsevals (if desired)
        if all_pars == 1: 
            print(f"data variance & fft variance: {np.nanvar(segment):.04f} and {(np.sum(amp)*df):.04f}")

    avg_fft = np.nanmean(fft_oi,axis=0)
    tot_amp = np.nanmean(amp_oi,axis=0)
    
    # parseval's check : 
    print(f'Check Parsevals - data variance equals integral of spectrum?')
    print(f'Data variance / spectrum integration: {(np.nanvar(data) / (np.sum(tot_amp)*df) ): 0.4f} ')
    
    nu = 2*M # degrees of freedom 
    top = 1-0.05/2; bot = 0.05/2 
    err_low = nu/(scipy.stats.chi2.ppf(top, nu)); err_high = nu/(scipy.stats.chi2.ppf(bot, nu))
    
    return real_freq, avg_fft, tot_amp, err_low, err_high
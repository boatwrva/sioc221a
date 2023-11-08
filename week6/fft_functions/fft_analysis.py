# function for fft and spectra analysis 

def fft_analysis(data=wsegs,time=time_segs,demean=1,detrend=1,hanning=1):
    # specifications for inputs: 
    # data_array should be size = (segments,data_in_segment); each data_in_segment column should be the same length
    # time array = should be the same size as data_array, could adapted for just a 1D vector. 
    # aka: you must window properly before using this function 
    # then, selecting whether to demean, detrend, hanning window, etc. 
    
    # all segment lengths should be the same 
    N = len(data[0,:])  # == num_samples
    deltat = np.diff(time)
    step = np.nanmean(deltat) # step size (in days)
    Nyq = 1/(2*step) # Nyquist frequency
    period = step*N # this is the entire period (in days)
    df = 1/period # fundamental frequency
    segs = len(data[:,0])
    M = segs
    
    # start workflow: analyze each segment individually 

    # fft & spectra of interest to be averaged 
    fft_oi = np.zeros((segs,N))
    amp_oi = np.zeros((segs,int(N/2)))
    

    for nn in np.arange(0,segs):
        segment = data[nn,:]
        segtime = time[nn,:]
    
        # demean & detrend 
    
        # calculate mean and linear trend 
        AA = np.array([np.ones(N), segtime]).T
        x = np.dot(np.linalg.inv(np.dot(AA.T, AA)), np.dot(AA.T, segment))
        mean = x[0]; trend = x[1]
        mymean = np.nanmean(segment)

        if demean==1: 
            segment = segment-mean # demean by calculated mean 
        
        if detrend==1: 
            segment = segment-trend*segtime # detrend from calculated trend
        
        if hanning==1: 
            hanwin = np.cos(np.pi*segtime / period)**2 # calculate hanning window
            segment = segment*hanwin*np.sqrt(8/3) # normalize hanning window by sqrt(8/3)
            
        # compute each segment spectrum 
        # fourier 
        fft = scipy.fft.fft(segment); 
        freq = scipy.fft.fftfreq(N,step)
        freq = scipy.fft.fftshift(freq)
        fftplot = scipy.fft.fftshift(fft)
        norm_fft = 1.0/N * np.abs(fftplot)
    
        even_idx = np.arange(0,N,2)
        amp = abs(fft[even_idx])**2 # even N 
        
        # corresponding frequencies based on data length
        freqs = np.arange(0,Nyq,df) # frequency vector, in [1/day], goes from 0 to Nyquist
    
        # do the steps for the spectrum: 
        amp = amp/(N**2) # correct normalization 
        amp = amp*2 # account for discarded redundant complex FFT coefficients 
        amp = amp/df 
        
        fft_oi[nn,:] = norm_fft
        amp_oi[nn,:] = amp
    
    avg_fft = np.nanmean(fft_oi,axis=0)
    tot_amp = np.nanmean(amp_oi,axis=0)
    
    nu = 2*M # degrees of freedom 
    top = 1-0.05/2; bot = 0.05/2 
    err_low = nu/(scipy.stats.chi2.ppf(top, nu)); err_high = nu/(scipy.stats.chi2.ppf(bot, nu))
    
    return freqs, avg_fft, tot_amp, err_low, err_high
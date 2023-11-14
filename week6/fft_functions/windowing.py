# function for windowing  

def windowing(time,data,tseg=60,deltat=10): 
    # make sure time segments (tseg) must be in units of days 
    # this function will return segmented arrays (of size [#segments,#N samples of data in each segment]) from a dataset with an associated time vector 
    # time: full time dataset (in datenumbers/integers )
    # data: full dataset of interest 
    # tsegs: the number of days desired in your segmenting [ in days ]
    # deltat: the sample spacing between your datapoints [in minutes]
    # this assumes the dt is 10 min, but that could be easily changed - as long as it is in minutes!
    
    # returns: 
    # time_segs: segments with their original time stamps associated 
    # data_segs: segmented data as an array of [#segments,#N samples of data in each segment]

    import numpy as np 

    # number of tseg intervals encompassed in full dataset
    intervals = int(np.floor((time[-1]-time[0])/tseg))
    # with 50% overlaps, it will be doubled but 1 less (because start 50% and end 50%)
    cycles = (intervals*2)-1

    num_samples = int(tseg/deltat *60*24) # number of samples if taken every 10 min in 60 days 


    # can make arrays the correct size because we know how many 10 min samples will be in 60 days 
    # each array = (segment num, data within segment) 
    data_segs = np.zeros((cycles,num_samples))
    time_segs = np.zeros((cycles,num_samples))

    ind = 0
    jump = int(num_samples/2); 
    for nn in np.arange(0,cycles): 
        # looping through each segment in which we will save data 
        data_segs[nn,:] = data[ind:ind+num_samples]
        time_segs[nn,:] = time[ind:ind+num_samples]
        
        # now add to the ind (start index) and jump (number of samples in the segment = 8640)
        ind = ind + jump

    return time_segs,data_segs
    
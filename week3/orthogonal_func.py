def orthogonality(n,m): 
    # demonstrate that 2 waves are orthogonal to each other 
    # compute integral from 0 to 2*pi of functions and see if they are opposite 
    import numpy as np 
    import scipy.integrate as integrals 
    
    dt = 0.01
    time = np.arange(0,2*np.pi,dt)
    wave1 = cos(m*time)
    wave2 = cos(n*time)
    
    integral = 0
    # integrate both waves together
    for ii in np.arange(0,len(time)): 
        step = wave1[ii]*wave2[ii] # f(b) -f(a)
        integral = integral + step*dt 
        
    # compare with scipy 
    bulk = integrals.quad(lambda x: np.cos(2*np.pi*m*x)*np.cos(2*np.pi*n*x),0,2*np.pi)
    
    
    print('Are they orthogonal?')
    print(f'Integral over 2 waves = {integral}')
    
    if integral < 0.05: 
        print('Near zero --> waves are orthogonal!')
    else: 
        print('Not near zero --> waves are additive')
    return integral
    




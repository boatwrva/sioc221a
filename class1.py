# SIOC 221: Class 1

# Fibonnacci sequence example: 
N = 10; 
fs = np.array([1,N]); fs[:,:] = np.nan
fs[0] = 1; 
fs[1] = 1; 

loop = np.arange(2,N)
sum = 0
for c in loop: 
	sum = sum+fs[c]
 

c = 1; 
fs[0] = 1**2 
while c<10: 
	fs[c+1] = fs[c]+ (c+1)**2 
	c = c + 1; 




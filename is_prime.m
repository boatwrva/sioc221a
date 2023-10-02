function y = is_prime(n)
% function is_prime for finding primes 
y = 1;
i = 2; 
while i < n/2
    if rem(n,i) == 0
        y = 0;   
    end 
    i = i + 1; 
end
disp(y)
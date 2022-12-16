```
ss2 =
  Discrete-time identified state-space model:
    x(t+Ts) = A x(t) + B u(t) + K e(t)
       y(t) = C x(t) + D u(t) + e(t)
 
  A = 
              x1         x2         x3
   x1     0.9994   0.001551  9.421e-05
   x2    -0.0532     0.7004     0.3478
   x3  -0.003551     0.2915    -0.4626
 
  B = 
               u1
   x1  -0.0002102
   x2      0.1029
   x3    -0.08862
 
  C = 
             x1        x2        x3
   y1     233.5   -0.1945  -0.01466
 
  D = 
       u1
   y1   0
 
  K = 
             y1
   x1  0.002971
   x2  -0.08336
   x3    0.1112
 
Name: ss2
Sample time: 1 seconds

Parameterization:
   FREE form (all coefficients in A, B, C free).
   Feedthrough: none
   Disturbance component: estimate
   Number of free coefficients: 18
   Use "idssdata", "getpvec", "getcov" for parameters and their uncertainties.

Status:                                            
Estimated using N4SID on time domain data "mydata".
Fit to estimation data: 95.88% (prediction focus)  
FPE: 0.003947, MSE: 0.003343
```

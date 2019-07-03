import numpy as np
import pickle as pk
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit as cf

# Read avalanche size data
size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
t0 = np.array(size)**2 * 2

# k-th moments to be calculated
k = [1, 2, 3, 4, 5, 6]

# Calculate k-th moments and fitting them on linear plot
xpts1 = np.logspace(0, 3.5, 1000)
xpts2 = np.logspace(0.1, 3.5, 1000)
slopek = []

# Optimise a scaling funvtion for it
def scaling(L, a0, w0, a1, w1):
    return a0*(L**w0)*(1 - a1*L**-w1)

for val in k:
    moment = []
    for i in range(len(size)):
        f_file = open('T3_L'+str(size[i])+'.pickle', 'rb')
        avasize = pk.load(f_file)
        f_file.close()
    
        reqsize = avasize[t0[i]:]
        moment.append(np.average(np.array(reqsize).astype(float)**val))
    
    pl.figure(1)
    pl.loglog(size, moment, 'o', label = r"$k = %d$" %(val))
    slope, intercept = np.polyfit(np.log(size)/np.log(10), np.log(moment)/np.log(10), 1)
    ypts = 10**(slope*np.log(xpts1)/np.log(10) + intercept)
    pl.loglog(xpts1, ypts, '-', label = r"Linear fit of $k = %d$" %(val))
    
    # Record the slope for later
    slopek.append(slope)
    
    # Investigate corrections to scaling
    paracf, varcf = cf(scaling, np.log(size)/np.log(10), np.log(moment)/np.log(10), maxfev = 10000)
    pl.figure(2)
    pl.subplot(3, 2, val)
    scaled_moment = moment / 10**(paracf[0]*(np.log(size)/np.log(10))**paracf[1])
    pl.loglog(size, scaled_moment, 'bo', label = r"Scaled moment %d $<s^%d> / (a_0 L^{\omega_0})$" %(val, val))
    ypts2 = 10**(paracf[0]*(np.log(xpts2)/np.log(10))**paracf[1]*(1 - paracf[2]*(np.log(xpts2)/np.log(10))**(-paracf[3]))) / 10**(paracf[0]*(np.log(xpts2)/np.log(10))**paracf[1])
    pl.loglog(xpts2, ypts2, 'r-', label = "Scaling function fit with \n"+r"$a_0 = %.3f$" %(paracf[0])
    +"\n"+r"$\omega_0 = %.3f$" %(paracf[1])+"\n"+r"$a_1 = %.3f$" %(paracf[2])+"\n"+r"$\omega_1 = %.3f$" %(paracf[3]))
    pl.legend()
    pl.grid(True)
    pl.ylabel(r"Scaled moment %d $<s^%d> / (a_0 L^{\omega_0})$" %(val, val))

pl.subplot(3, 2, 1)
pl.ylim(0.7, 3)
pl.subplot(3, 2, 5)
pl.xlabel(r"System size $L$")
pl.subplot(3, 2, 6)
pl.xlabel(r"System size $L$")

pl.figure(1)
pl.legend()
pl.xlabel(r"System size $L$")
pl.ylabel(r"$k$'th moment $<s^k>$")
pl.grid(True)

# Fit the slope of each fit on a straight line, then determine D and tau_s through slope and intercept respectively
pl.figure(3)
para, var = np.polyfit(k, slopek, 1, cov = True)
tau_s = 1 - para[1] / para[0]
err_tau_s = np.sqrt(((np.sqrt(np.diag(var)[1]))/para[0])**2 + ((np.sqrt(np.diag(var)[0]))*para[1]/para[0]**2)**2)

xpts1 = np.linspace(0.5, 6.5, 1000)
ypts1 = para[0]*xpts1 + para[1]
pl.plot(k, slopek, 'bo', label = r"Slopes of $k$'th moment fits")
pl.plot(xpts1, ypts1, 'r-', label = "Linear fit with \n"+
        r"$D = %.3f \pm %.3f$" %(para[0], np.sqrt(np.diag(var)[0]))+
        "\n"+r"$\tau_s = %.3f \pm %.3f$" %(tau_s, err_tau_s))

pl.legend()
pl.grid(True)
pl.xlabel(r"$k$")
pl.ylabel(r"Slope of fit = $D (1 + k - \tau_s)$")

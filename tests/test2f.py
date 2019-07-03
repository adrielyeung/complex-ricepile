import numpy as np
import pickle as pk
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit as cf

size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Obtain standard deviation
f_file = open('T2f_sdheight.pickle', 'rb')
sd = pk.load(f_file)
f_file.close()

pl.figure()
pl.loglog(size, sd, 'bo', label = r"Standard deviation of the height $\sigma_h$")
pl.xlabel(r"System size $L$")
pl.ylabel(r"Standard deviation $\sigma_h$")
pl.grid()
pl.ylim(0.1, 10)

# Optimise a scaling funvtion for it
def scaling(L, a0, w0, a1, w1):
    return a0*(L**w0)*(1 - a1*L**-w1)

para, var = cf(scaling, np.log(size)/np.log(10), np.log(sd)/np.log(10), maxfev = 4000)

xpts = np.logspace(0.2, 3.1, 5000)
ypts = 10**(para[0]*(np.log(xpts)/np.log(10))**para[1]*(1 - para[2]*(np.log(xpts)/np.log(10))**(-para[3])))

pl.loglog(xpts, ypts, 'r-', label = r"Scaling function $a_0 L^{\omega_0} (1 - a_1 L^{-\omega_1})$ fit with"
          + "\n" + r"$a_0 = %.3f \pm %.3f$" %(para[0], np.sqrt(np.diag(var)[0])) + "\n" + r"$\omega_0 = %.3f \pm %.3f$" %(0.2388, np.sqrt(np.diag(var)[1]))
          + "\n" + r"$a_1 = %.3f \pm %.3f$" %(para[2], np.sqrt(np.diag(var)[2])) + "\n" + r"$\omega_1 = %.3f \pm %.3f$" %(para[3], np.sqrt(np.diag(var)[3])))
pl.legend()

# Divide by a0*L**w0 to obtain trend for large L - expect SD to tend towards a0*L**w0
yptsdiv = ypts / 10**(para[0]*(np.log(xpts)/np.log(10))**para[1])
sddiv = sd / 10**(para[0]*(np.log(size)/np.log(10))**para[1])

pl.figure()
pl.loglog(size, sddiv, 'bo', label = r"Scaled standard deviation $\sigma_h / a_0 L^{\omega_0}$")
pl.xlabel(r"System size $L$")
pl.ylabel(r"Scaled standard deviation $\sigma_h / a_0 L^{\omega_0}$")
pl.grid()
pl.loglog(xpts, yptsdiv, 'r-', label = r"Scaling function $(1 - a_1 L^{-\omega_1})$ fit")
pl.legend()
pl.ylim(0.1, 10)

# Save para and var for use in Task 2g
f_file1 = open('T2f_para.pickle', 'wb')
pk.dump(para, f_file1)
f_file1.close()

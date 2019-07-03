import numpy as np
import pickle as pk
import matplotlib.pyplot as pl

size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

aveheight = []

# Obtain average height
f_file = open('T2e_aveheight.pickle', 'rb')
aveheight = pk.load(f_file)
f_file.close()

# Linear fit - find a crude estimate for a_0
para, var = np.polyfit(size, aveheight, 1, cov = True)
xpts = np.linspace(0, 1050, 5000)
ypts = para[0]*xpts + para[1]

pl.figure()
pl.plot(size, aveheight, 'bo', label = r"Average height $<h>$")
pl.plot(xpts, ypts, 'r-', label = r"Linear fit with slope = %.3f $\pm$ %.3f" % (para[0], np.sqrt(np.diag(var))[0])
+"\n"+r"and intercept = %.3f $\pm$ %.3f" %(para[1], np.sqrt(np.diag(var))[1]))
pl.xlabel(r"System size $L$")
pl.ylabel(r"Average height of pile $<h>$")
pl.grid()
pl.legend()

# Determine optimum a_0 by trying to fit the required log-log plot using a range of values
testa0 = np.linspace(1.72, 1.74, 150)
a0_err = 1/750

slopevar = []

for i in range(len(testa0)):
    y = []
    for j in range(len(size)):
        y.append(abs(testa0[i] - aveheight[j] / size[j]))
    # slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(np.array(newsize))/np.log(10), np.log(y)/np.log(10))
    testpara, testvar = np.polyfit(np.log(np.array(size))/np.log(10), np.log(y)/np.log(10), 1, cov = True)
    slope_err = np.sqrt(np.diag(testvar))[0]
    slopevar.append(slope_err)
a0index = slopevar.index(min(slopevar))
mina0 = testa0[a0index]
    
pl.figure()
pl.plot(testa0, slopevar, 'o')
pl.xlabel(r"$a_0$")
pl.ylabel("Standard error in the slope of the fit")
pl.grid(True)

# Plotting "best-fit" line together with two "worst-fit" lines to compare
yfinal = mina0 - np.array(aveheight) / (np.array(size))
ybad1 = testa0[0] - np.array(aveheight) / (np.array(size))
ybad2 = testa0[-1] - np.array(aveheight) / (np.array(size))

parafinal, varfinal = np.polyfit(np.log(np.array(size))/np.log(10), np.log(yfinal)/np.log(10), 1, cov = True)

pl.figure()
pl.loglog(size, yfinal, 'o', label = r"Best-fit line with $a_0 = %.3f \pm %.3f$" % (mina0, a0_err))
pl.loglog(size, ybad1, 'o', label = r"Line with $a_0 = %.3f \pm %.3f$" % (testa0[0], a0_err))
pl.loglog(size, ybad2, 'o', label = r"Line with $a_0 = %.3f \pm %.3f$" % (testa0[-1], a0_err))
pl.xlabel(r"System size $L$")
pl.ylabel(r"($a_0 - <h>)/ L$")
pl.grid(True)

# Try polynomial fitting for the "worst-fit" lines
parabad1 = np.polyfit(np.log(np.array(size))/np.log(10), np.log(ybad1)/np.log(10), 2)
parabad2 = np.polyfit(np.log(np.array(size))/np.log(10), np.log(ybad2)/np.log(10), 2)


xptsbad = np.logspace(0.1, 3, 5000)
yptsbad1 = 10**(parabad1[0]*(np.log(xptsbad)/np.log(10))**2 + parabad1[1]*(np.log(xptsbad)/np.log(10)) + parabad1[2]) 
pl.loglog(xptsbad, yptsbad1, 'r--', label = "Quadratic fits")
yptsbad2 = 10**(parabad2[0]*(np.log(xptsbad)/np.log(10))**2 + parabad2[1]*(np.log(xptsbad)/np.log(10)) + parabad2[2])
yptsfinal = 10**(parafinal[0]*(np.log(xptsbad)/np.log(10)) + parafinal[1]) # 10**(paracurve[0]*(np.log(xptsbad)/np.log(10))*(1 - paracurve[1]*(np.log(xptsbad)/np.log(10))**(-paracurve[2]))) # 
pl.loglog(xptsbad, yptsbad2, 'r--')
pl.loglog(xptsbad, yptsfinal, 'k--', label = r"Linear fit with slope = $%.3f \pm %.3f$" %(parafinal[0], np.sqrt(np.diag(varfinal))[0]) + "\n" + "and intercept = $%.3f \pm %.3f$" % (parafinal[1], np.sqrt(np.diag(varfinal))[1]))
pl.legend()

# Calculate a_1 and w_1 from the intercept and slope respectively
a1 = 10**(parafinal[1] - np.log(mina0)/np.log(10))
w1 = -parafinal[0]
data = [mina0, a1, w1] # a_0, a_1, w_1

# Save parafinal and varfinal for use in Task 2g
f_file1 = open('T2e_para.pickle', 'wb')
pk.dump(data, f_file1)
f_file1.close()

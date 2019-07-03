import numpy as np
import pickle as pk
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit as cf

# Plot tc vs L^2 to verify theoretical relationship
size = [4, 8, 16, 32, 64, 128, 256]
avecrosstime = []

for j in size:
    crosstime = []
    if j >= 32:
        for i in [1, 2, 3, 4]:
            f_file = open('tc_'+str(j)+'_'+str(i)+'.pickle', 'rb')
            crosstimepart = pk.load(f_file)
            f_file.close()
            crosstime += crosstimepart
    else:
        for i in [1, 3]:
            f_file = open('tc_'+str(j)+'_'+str(i)+'.pickle', 'rb')
            if i == 1:
                crosstimepart = pk.load(f_file)[0]
            else:
                crosstimepart = pk.load(f_file)
            f_file.close()
            crosstime += crosstimepart
    avecrosstime.append(np.average(np.array(crosstime)))

# Confirming the L^2 relationship by plotting log <tc> vs log L to extract the exponent on L
pl.figure()
pl.loglog(np.array(size), avecrosstime, 'o', label = r"Average cross-over time $<t_c>$")

pl.xlabel(r"System size $L$")
pl.ylabel(r"Average cross-over time $<t_c>$")
pl.grid()

# Fit line to obtain slope
paraLexp, varLexp = np.polyfit(np.log(np.array(size))/np.log(10), np.log(avecrosstime)/np.log(10), 1, cov = True)

xptsLexp = np.logspace(0.5, 2.5, 1000)
yptsLexp = 10**(paraLexp[0]*np.log(xptsLexp)/np.log(10) + paraLexp[1])
pl.loglog(xptsLexp, yptsLexp, 'r-', label = "Linear fit with \n"+r"slope = $%.3f \pm %.3f$" %(paraLexp[0], np.sqrt(np.diag(varLexp)[0])))
pl.legend()

# Fit theoretical relationship <z>/2 L^2 (1 + 1/L) to find <z>
def crossover(L, avez):
    return np.log(avez / 2 * (1 + 1/L))/np.log(10)

pl.figure()
pl.plot(np.array(size), avecrosstime / np.array(size)**2, 'o', label = r"Scaled average cross-over time $<t_c>/L^2$")
pl.xlabel(r"System size $L$")
pl.ylabel(r"Scaled average cross-over time $<t_c>/L^2$")
pl.grid()

# Calculate average slopes using recurrent values for size L = 256 (more consistent)
f_file = open('T1_L256_p5.pickle', 'rb')
aveslopes = pk.load(f_file)[2*256**2 - 1:]
f_file.close()

ave_aveslope = np.average(aveslopes)

xptstc = np.linspace(3.9, 260, 1000)
yptstc = ave_aveslope/2*(1 + 1/xptstc)
yptstccon = np.ones(len(xptstc))*ave_aveslope/2

#paraavez, varavez = cf(crossover, np.log(np.array(size))/np.log(10), np.log(avecrosstime / np.array(size)**2)/np.log(10), p0 = [1.73])
#
#xptsavez = np.logspace(0.2, 2.3, 1000)
#yptsavez = 10**(paraavez[0]/2*(1 + 1/xptsavez))
pl.plot(xptstc, yptstc, 'r--', label = r"Theoretical relation $<z>(1 + 1/L)/2$")
pl.plot(xptstc, yptstccon, 'k--', label = r"Value neglecting correction to scaling $<z> / 2$")
pl.legend()

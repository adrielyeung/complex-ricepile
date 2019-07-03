import logbin6_2_2018 as lb
import numpy as np
import pickle as pk
import matplotlib.pyplot as pl

sizefile = ['T3_L2.pickle', 'T3_L4.pickle', 'T3_L8.pickle', 'T3_L16.pickle', 'T3_L32.pickle',
         'T3_L64.pickle', 'T3_L128.pickle', 'T3_L256.pickle', 'T3_L512.pickle', 'T3_L1024.pickle']

syssize = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
t0 = syssize**2 * 2

# Set scaling factor for log-binning
a = 2.0
b = -1

# Observe how trend of unbinned data changes as N changes (try N = 10^2, 3, 4, 5) for L = 256
f_file = open('T3_L'+str(syssize[b])+'.pickle', 'rb')
avasize = pk.load(f_file)
f_file.close()

pl.figure()
for i in [4, 5, 6, 7]:
    if i != 7:
        reqsize = avasize[t0[b]:t0[b] + 10**i + 1]    
    else:
        reqsize = avasize[t0[b]:]
    bins = np.arange(min(reqsize) - 1.5, max(reqsize) + 2.5, 1)
    bincentre = bins[:-1] + 0.5
    
    hist, bin_edges = np.histogram(reqsize, bins = bins, density = True) # density = True returns probability density

    # Log-bin the data
    bincentre_bin, hist_bin = lb.logbin(reqsize, scale = a)
    
    pl.subplot(2, 2, i - 3)
    if i != 7:
        pl.loglog(bincentre, hist, 'o', label = r"Unbinned, $N = 10^%d$" %(i))
        pl.loglog(bincentre_bin, hist_bin, 'r-', label = r"Binned, $N = 10^%d$" %(i))
    else:
        pl.loglog(bincentre, hist, 'o', label = r"Unbinned, $N = %.1g$" %(1e7 - t0[b]))
        pl.loglog(bincentre_bin, hist_bin, 'r-', label = r"Binned, $N = %.1g$" %(1e7 - t0[b]))
    pl.grid(True)
    pl.legend()
    pl.xlim(1, 10**7)
    pl.ylim(10**-13, 1)

pl.subplot(2, 2, 1)
pl.ylabel(r"Probability of $s$ $P(s; L)$")
pl.subplot(2, 2, 3)
pl.xlabel(r"Avalanche size $s$")
pl.ylabel(r"Probability of $s$ $P(s; L)$")
pl.subplot(2, 2, 4)
pl.xlabel(r"Avalanche size $s$")

# Plot probabilities for all sizes L
pl.figure()
for item in range(len(syssize)):
    f_file = open(sizefile[item], 'rb')
    avasize = pk.load(f_file)
    f_file.close()
    
    reqsize = avasize[t0[item]:]
    
    # Log-bin the data
    bincentre_bin, hist_bin = lb.logbin(reqsize, scale = a)
    
    pl.loglog(bincentre_bin, hist_bin, '-', label = r"$L = %d$" %(syssize[item]))
    pl.grid(True)
    pl.legend()
    pl.xlabel(r"Avalanche size $s$")
    pl.ylabel(r"Probability of $s$ $P(s; L)$")

    # Save data from last plot (largest L) for Task 3b
    f_file1 = open('T3_size'+str(syssize[item])+'.pickle', 'wb')
    pk.dump(bincentre_bin, f_file1)
    f_file1.close()
    
    f_file2 = open('T3_prob'+str(syssize[item])+'.pickle', 'wb')
    pk.dump(hist_bin, f_file2)
    f_file2.close()

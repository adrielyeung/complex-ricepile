import numpy as np
import pickle as pk
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit as cf

unsmoothed = ['T2_L2.pickle', 'T2_L4.pickle', 'T2_L8.pickle', 'T2_L16.pickle', 
            'T2_L32.pickle', 'T2_L64.pickle', 'T2_L128.pickle', 'T2_L256.pickle',
            'T2_L512.pickle', 'T2_L1024.pickle']

size = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
t0 = np.array(size)**2 * 2

# read data
f_file = open('T2e_para.pickle', 'rb')
aveheightpara = pk.load(f_file)
f_file.close()

a0av = aveheightpara[0]
a1av = aveheightpara[1]
w1av = aveheightpara[2]

f_file1 = open('T2f_para.pickle', 'rb')
sigmaheightpara = pk.load(f_file1)
f_file1.close()

a0sig = sigmaheightpara[0]
w0sig = sigmaheightpara[1]
a1sig = sigmaheightpara[2]
w1sig = sigmaheightpara[3]

reqheight = []

# Read average height
f_file2 = open('T2e_aveheight.pickle', 'rb')
aveheight = pk.load(f_file2)
f_file2.close()

gauss_x = np.array([])
gauss_y = np.array([])
# Obtain individual heights
for item in range(len(unsmoothed)):
    # read data
    f_file = open(unsmoothed[item], 'rb')
    height = pk.load(f_file)
    f_file.close()
    
    reqheight = height[t0[item]:]
    # Set bins
    bins = np.arange(min(reqheight) - 1.5, max(reqheight) + 2.5, 1)
    bincentre = bins[:-1] + 0.5
    
    # Obtain probability of height
    hist, bin_edges = np.histogram(reqheight, bins = bins, density = True) # density = True returns probability density
    
    # Plot unscaled probabilty vs height
    pl.figure(100)
    pl.plot(bincentre, hist, '-', label = r"$L =$ %d" % (size[item]))
    
    # Plot scaled probability vs scaled height
    pl.figure(101)
    scaled_hist = (a0sig*(size[item]**w0sig)*np.sqrt(2*np.pi)*hist)
    scaled_bincentre = (bincentre - aveheight[item])/(np.sqrt(2)*a0sig*(size[item]**(w0sig))) #(bincentre - a0av*size[item]*(1 - a1av*size[item]**-w1av))/(np.sqrt(2)*a0sig*(size[item]**(w0sig)))
    pl.plot(scaled_bincentre, scaled_hist, 'o', label = r"$L =$ %d" % (size[item]))
    gauss_x = np.append(gauss_x, scaled_bincentre)
    gauss_y = np.append(gauss_y, scaled_hist)
    pl.figure(102)
    pl.semilogy(scaled_bincentre, scaled_hist, 'o', label = r"$L =$ %d" % (size[item]))
    
pl.figure(100)
pl.xlabel(r"Height $h$")
pl.ylabel(r"Height probability $P(h; L)$")
pl.legend()
pl.grid()
pl.xlim(0,)
pl.ylim(0,)

pl.figure(101)
pl.xlabel(r"Scaled height $h' = (h - a_{0h} L(1 - a_{1h} L^{-\omega_{1h}})) / L^{\omega_{0\sigma}}$")
pl.ylabel(r"Scaled probability $P' = a_{0 \sigma} L^{\omega_{0 \sigma}} \sqrt{2 \pi} P(h; L)$")
pl.grid()

pl.figure(102)
pl.xlabel(r"Scaled height $h' = (h - a_{0h} L(1 - a_{1h} L^{-\omega_{1h}})) / L^{\omega_{0\sigma}}$")
pl.ylabel(r"Scaled probability $P' = a_{0 \sigma} L^{\omega_{0 \sigma}} \sqrt{2 \pi} P(h; L)$")
pl.legend()
pl.grid()

# Perform Gaussian fit to confirm theoretical prediction
def Gauss(x, mu, sigma, a):
    return a*np.exp(-(x - mu)**2 / (2*sigma**2))

para, var = cf(Gauss, gauss_x, gauss_y, p0 = [0, 1, 0.12])
xpts = np.linspace(-30, 40, 500)
ypts = para[2]*np.exp(-(xpts - para[0])**2 / (2*para[1]**2))
pl.figure(101)
#pl.plot(gauss_x, gauss_y, 'k-')
pl.plot(xpts, ypts, 'r-', label = "Gaussian fit with \n" + r"$<h'> = %.3f \pm %.3f$ and" % (para[0], np.sqrt(np.diag(var)[0]))+"\n"+r"$\sigma_{h'} = %.3f \pm %.3f$" % (para[1], np.sqrt(np.diag(var)[1])))
pl.legend()

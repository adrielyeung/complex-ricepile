import pickle as pk
import numpy as np
import matplotlib.pyplot as pl

smoothed = ['T2_L2s.pickle', 'T2_L4s.pickle', 'T2_L8s.pickle', 'T2_L16s.pickle', 
            'T2_L32s.pickle', 'T2_L64s.pickle', 'T2_L128s.pickle', 'T2_L256s.pickle',
            'T2_L512s.pickle', 'T2_L1024s.pickle']

size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

xfit = [] # points used for fitting for t/L^2 << 1
yfit = []

pl.figure()
for item in range(len(smoothed)):
    # read data
    f_file = open(smoothed[item], 'rb')
    scaleheight = pk.load(f_file)
    scaleheight = np.array(scaleheight)/size[item]
    f_file.close()
    
    x = np.arange(len(scaleheight))/size[item]**2
    
    # Collect all points to be fitted for t/L^2 << 1 (< 0.1)
    for i in range(len(x)):
        if x[i] > 0 and x[i] <= 1e-1:
            xfit.append(x[i])
            yfit.append(scaleheight[i])

    pl.loglog(x, scaleheight, label = r"$L$ = %d" % (size[item]))
    pl.legend(loc = "lower right")
    pl.grid(True)
    pl.xlabel(r'Scaled time $t/L^2$')
    pl.ylabel(r'Scaled height of the pile $\tilde{h}/L$')
    #pl.xlim(1, 1e6)
    #pl.ylim(1, )
    
logxfit = np.log(xfit)/np.log(10)
logyfit = np.log(yfit)/np.log(10)
para, var = np.polyfit(logxfit, logyfit, 1, cov = True)

# Plot fitted line
xpts = np.logspace(-7, 1, 5000)
ypts = 10**(para[0]*np.log(xpts)/np.log(10) + para[1]) # relationship determined by taking exponential of 
pl.loglog(xpts, ypts, 'k--', label = "Linear fit with slope = %s $\pm$ %s" % ("%.5f" %(para[0]), "%.5f" %(np.sqrt(np.diag(var))[0])))
pl.legend(loc = "lower right")

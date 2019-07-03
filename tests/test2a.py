import pickle as pk
import matplotlib.pyplot as pl

# plot data files
unsmoothed = ['T2_L2.pickle', 'T2_L4.pickle', 'T2_L8.pickle', 'T2_L16.pickle', 
            'T2_L32.pickle', 'T2_L64.pickle', 'T2_L128.pickle', 'T2_L256.pickle',
            'T2_L512.pickle', 'T2_L1024.pickle']

smoothed = ['T2_L2s.pickle', 'T2_L4s.pickle', 'T2_L8s.pickle', 'T2_L16s.pickle', 
            'T2_L32s.pickle', 'T2_L64s.pickle', 'T2_L128s.pickle', 'T2_L256s.pickle',
            'T2_L512s.pickle', 'T2_L1024s.pickle']

size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

pl.figure()
for i in range(len(unsmoothed)):
    # read data
    f_file = open(unsmoothed[i], 'rb')
    
    y = pk.load(f_file)
    f_file.close()
    
    x = range(len(y))
    
    pl.plot(x, y, label = r"$L$ = %d" % (size[i]))
pl.legend(loc = "upper left")
pl.grid(True)
pl.xlabel(r"Time $t$")
pl.ylabel(r"Height of the pile $h$")
pl.xlim(1, 1e7)
#pl.ylim(1, )

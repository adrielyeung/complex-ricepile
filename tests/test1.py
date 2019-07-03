import pickle as pk
import matplotlib.pyplot as pl

# plot data files
size = [4, 8, 16, 32, 64, 128, 256]
p = [0, 5, 1]

for j in range(len(p)):
    pl.figure()
    for i in range(len(size)):
        # read data
        f_file = open('T1_L'+str(size[i])+'_p'+str(p[j])+'.pickle', 'rb')
        
        y = pk.load(f_file)
        f_file.close()
        
        x = range(len(y))
        
        if p[j] != 5:
            pl.semilogx(x, y, label = r"$L$ = %d, $p$ = %.1f" % (size[i], p[j]))
        else:
            pl.semilogx(x, y, label = r"$L$ = %d, $p$ = %.1f" % (size[i], p[j]/10))
        pl.legend(loc = "lower right")
    pl.grid(True)
    pl.xlabel(r"Time $t$")
    pl.ylabel(r"Average slope $<z>$")
    #pl.xlim(1, 1e6)
    #pl.ylim(1, )

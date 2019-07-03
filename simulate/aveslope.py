import ricepile as rp
import numpy as np
import pickle as pk

L = 128
N_add = 1e6

p = 0.5

aveslope = []

riceoslo = rp.oslo(L, p)

for i in np.arange(N_add):
    riceoslo.driverel()
    aveslope.append(np.average(riceoslo.z))
    print(i)

f_file = open('T1_L128_p5.pickle', 'wb')
pk.dump(aveslope, f_file)
f_file.close()

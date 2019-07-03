import ricepile as rp
import numpy as np
import pickle as pk

L = 512
N_add = 10**7

p = 0.5

height = []
size = []

riceoslo = rp.oslo(L, p)

for i in range(N_add):
    sizenew = riceoslo.driverel()
    height.append(riceoslo.h[0])
    size.append(sizenew)
    #print(i)

f_file1 = open('T2_L512.pickle', 'wb')
pk.dump(height, f_file1)
f_file1.close()

f_file2 = open('T3_L512.pickle', 'wb')
pk.dump(size, f_file2)
f_file2.close()

import numpy as np
import pickle as pk
import matplotlib.pyplot as pl

size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Load data
# Largest system size to find tau_s
f_file = open('T3_size'+str(size[-1])+'.pickle', 'rb')
avasizelarge = pk.load(f_file)
f_file.close()

f_file1 = open('T3_prob'+str(size[-1])+'.pickle', 'rb')
avaproblarge = pk.load(f_file1)
f_file1.close()

# Find slope for sizes from 10^2 to 10^4 - linear fit in this range
x = []
y = []

for i in range(len(avasizelarge)):
    if avasizelarge[i] >= 10**2 and avasizelarge[i] <= 10**4:
        x.append(avasizelarge[i])
        y.append(avaproblarge[i])

para, var = np.polyfit(np.log(x)/np.log(10), np.log(y)/np.log(10), 1, cov = True)

tau_s = - para[0] # tau_s
err_tau_s = np.sqrt(np.diag(var)[0])

# Define L^D as the maximum of the 'bump', i.e. having the greatest difference from the trend
maxindex = []
for i in size[:-1]: # neglect largest L since it is used for comparison
    f_file2 = open('T3_prob'+str(i)+'.pickle', 'rb')
    avaprobcurrent = pk.load(f_file2)
    f_file2.close()
    diff = []
    for j in range(len(avaprobcurrent)):
        diff.append(np.log(avaprobcurrent[j])/np.log(10) - np.log(avaproblarge[j])/np.log(10))
    maxindex.append(diff.index(max(diff)))

# Manually add index for the largest L
maxindex.append(-5)
maxsize = []
for i in maxindex:
    maxsize.append(avasizelarge[i])

# Neglect L = 2 in the fit because it's shape is irregular and also too few points
para1, var1 = np.polyfit(np.log(size[1:])/np.log(10), np.log(maxsize[1:])/np.log(10), 1, cov = True)

D = para1[0] # D
err_D = np.sqrt(np.diag(var1))[0]

# Data collapse
pl.figure()
for i in size:
    xcoll = []
    ycoll = []
    f_file3 = open('T3_size'+str(i)+'.pickle', 'rb')
    avasize = pk.load(f_file3)
    f_file3.close()
    f_file4 = open('T3_prob'+str(i)+'.pickle', 'rb')
    avaprob = pk.load(f_file4)
    f_file4.close()
    for j in range(len(avasize)):
        ycoll.append((avasize[j]**tau_s)*avaprob[j])
        xcoll.append(avasize[j] / (i**D))
    pl.loglog(xcoll, ycoll, '-', label = r"$L = %d$" % (i))

pl.legend()
pl.grid(True)
pl.xlabel(r"Scaled avalanche size $s / L^D$")
pl.ylabel(r"Scaled probability $s^{\tau_s}\tilde{P}_N (s; L)$")

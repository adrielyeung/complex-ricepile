import pickle as pk
import numpy as np

unsmoothed = ['T2_L2.pickle', 'T2_L4.pickle', 'T2_L8.pickle', 'T2_L16.pickle', 
            'T2_L32.pickle', 'T2_L64.pickle', 'T2_L128.pickle', 'T2_L256.pickle',
            'T2_L512.pickle', 'T2_L1024.pickle']

size = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
t0 = np.array(size)**2 * 2

aveheight = []

# Obtain average height
for item in range(len(unsmoothed)):
    # read data
    f_file = open(unsmoothed[item], 'rb')
    height = pk.load(f_file)
    f_file.close()

    aveheight.append(np.average(np.array(height[int(t0[item]):])))
    
# Save average height as file for Task 2e, 2g
f_file2 = open('T2e_aveheight.pickle', 'wb')
pk.dump(aveheight, f_file2)
f_file2.close()

import numpy as np
import pickle as pk

# Smooth out height data using a moving average
# read data
f_file = open('T2_L128.pickle', 'rb')
height = pk.load(f_file)
f_file.close()

aveheight = []

for i in range(len(height)):
    if i >= 25 and i <= len(height) - 25: # not the first or last 25 points
        W = 25 # temporal window
    elif i < 25:
        W = i # average over i points below (beginning) and above
    else:
        W = len(height) - i # average over i points below and above (end)
    aveheight.append(np.average(height[i - W:i + W + 1]))

f_file1 = open('T2_L128s.pickle', 'wb')
pk.dump(aveheight, f_file1)
f_file1.close()

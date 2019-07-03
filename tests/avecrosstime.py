import ricepile as rp
import pickle as pk

L = 16#[4, 8, 16, 32, 64, 128, 256]
num_repeat = 10**5 # number of cross-over time values to be obtained

record_time = 0#[0, 0, 0, 575, 2704, 11892, 50833]

p = 0.5

crosstime = []
for i in range(num_repeat):
    riceoslo = rp.oslo(L, p)
    current_time = 0
    stop = False
    while stop == False:
        stop = riceoslo.driverel(True)
        current_time += 1
    crosstime.append(current_time)

f_file = open('tc_16_3_power5.pickle', 'wb')
pk.dump(crosstime, f_file)
f_file.close()

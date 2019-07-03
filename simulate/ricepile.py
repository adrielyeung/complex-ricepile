import numpy as np

class oslo:
    """
    Generates a system using the Oslo model where the system size can be varied.
    The slopes at each position (defined as the height between the current site
    and the next) are kept track of.
    """
    def __init__(self, L, p):
        """
        __init__ - initialises the oslo model object
        
        Inputs:
        L : integer, system size
        p : float, probability of threshold slope = 1
    
        Data attributes:
        self.L : system size
        self.h : height at each site
        self.z : local slope between each site and the next
        self.zth : threshold slope at each site, chosen at random being either
        1 or 2
        """
        self.L = L
        self.p = p
        self.h = np.zeros(L)
        self.z = np.zeros(L)
        self.zth = np.random.choice([1, 2], L, p=[p, 1 - p])
        
    def driverel(self, crossover = False):
        """
        Adds a grain at site 1. Then relax the system if any local slope is 
        greater than the threshold slope at that site.
        
        Input:
        crossover : determines whether cross-over time is required (Task 2d) or
        the height (Task 2) or avalanche size (Task 3) instead.
        
        Outputs:
        if crossover == True:
            stop : boolean, determining whether cross-over time is reached
        if crossover == False:
            size : avalanche size recorded due to the addition of this grain            
        """
        self.h[0] += 1
        self.z[0] += 1
        i = 0
        if crossover == True:
            stop = False # this returns when the cross-over time has been reached and stops the addition of grains
        else:
            size = 0 # Avalanche size counter
        while i < self.L:
            # relax
            while self.z[i] > self.zth[i]:
                if crossover == False:
                    size += 1
                self.h[i] -= 1 # current site drops grain
                if i < self.L - 1: # not last site
                    self.h[i + 1] += 1 # next site gains grain
                    self.z[i] -= 2
                    self.z[i + 1] += 1
                    # choose new threshold slope
                    self.zth[i] = np.random.choice([1, 2], 1, p=[self.p, 1 - self.p])
                    if i > 0: # not first site
                        self.z[i - 1] += 1
                        i -= 1 # check if previous site needs relaxing again
                        continue
                else: # i = L - 1, last site
                    self.z[i] -= 1
                    self.z[i - 1] += 1
                    # choose new threshold slope
                    self.zth[i] = np.random.choice([1, 2], 1, p=[self.p, 1 - self.p])
                    if crossover == True:
                        stop = True # this notifies the iterating function to stop
                    i -= 1 # check if previous site needs relaxing again
                    continue
            i += 1                
        if crossover == True:
            return stop
        else:
            return size
    
import random as rn
import math

def funExpon(mean):
    U = rn.uniform(0,1)
    return -(mean)*math.log(U)
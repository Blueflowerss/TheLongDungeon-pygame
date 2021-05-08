import math
import noise
def first_n_digits(num, n):
    return num // 10 ** (int(math.log(num, 10)) - n + 1)
def generateNoise(value,x,y,octaves,min,max,seed,raw=False):
    tmpNoise = noise.snoise4(x*0.01,y * 0.01,value*0.01,value*0.01)
    tmpNoise += noise.snoise4(x*0.01,y*0.01,value*0.02,value*0.02)
    tmpNoise += noise.pnoise2(x*0.01,y*0.01)
    tmpNoise /= 3
    color_world = 0
    if not raw:
        if min < tmpNoise < max:
            color_world = 1
        return color_world
    else:
        return tmpNoise
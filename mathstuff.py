import math
import noise
import globals
import random
def first_n_digits(num, n):
    return num // 10 ** (int(math.log(num, 10)) - n + 1)
def generateNoise(value,x,y,min,max,seed,raw=False,octaves=3):
    if octaves == 1:
        tmpNoise = noise.snoise4(x*0.01,y * 0.01,value*0.01,value*0.01)
    elif octaves == 2:
        tmpNoise = noise.snoise4(x * 0.01, y * 0.01, value * 0.01, value * 0.01)
        tmpNoise += noise.snoise4(x * 0.01, y * 0.01, value * 0.02, value * 0.02)
    elif octaves == 3:
        tmpNoise = noise.snoise4(x * 0.01, y * 0.01, value * 0.01, value * 0.01)
        tmpNoise += noise.snoise4(x * 0.01, y * 0.01, value * 0.02, value * 0.02)
        tmpNoise += noise.pnoise2(x * 0.01, y * 0.01)
    elif octaves == 4:
        tmpNoise = noise.snoise2(x * 0.001, y * 0.001)
    tmpNoise /= octaves
    color_world = 0
    if not raw:
        if min < tmpNoise < max:
            color_world = 1
        return color_world
    else:
        return tmpNoise
def weigtedChances(list,chances):
    random.seed(globals.seed)
    randomList = random.choices(list,weights=chances,k=5)
    return randomList
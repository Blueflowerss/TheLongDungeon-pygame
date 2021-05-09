import globals
import random
worldData = {}
worldTerrain = {
    "plains":0.09,"mountains":0.04
}
worldChances = {}
def initialize():
    global worldData
def ready():
    global worldData
    worldData = globals.readFromFile("./data/worldtype.json",True)
    for type in worldData:
        worldChances[type] = worldData[type]["chance"]

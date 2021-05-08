import globals
worldData = {}
def initialize():
    global worldData
def ready():
    global worldData
    worldData = globals.readFromFile("./data/worldtype.json",True)
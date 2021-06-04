import globals
import random
import classes
worldData = {}
worldTerrain = {
    "plains":0.08,"mountains":0.04
}
worldChances = {}
def initialize():
    global worldData
def ready():
    global worldData
    worldData = globals.readFromFile("./data/worldtype.json",True)
    for type in worldData:
        worldChances[type] = worldData[type]["chance"]

def prepareWorld(universe):
    if globals.multiverse[universe].worldType["buildings"]:
        pass
        #classes.WorldGen.populateSquare(index)
    if globals.multiverse[universe].worldType["treeGen"]:
        for number in range(1,globals.multiverse[universe].worldType["treeAmount"]):
            xPos,yPos = int(random.uniform(1,globals.worldSize)),int(random.uniform(1,globals.worldSize))
            globals.multiverse[universe].loadedTerrain[xPos,yPos] = classes.Tile(xPos,yPos,globals.tileHash[globals.multiverse[universe].
                                                                                 worldType["ground"]],globals.multiverse[universe])
            #print(str(xPos)+" "+str(yPos))

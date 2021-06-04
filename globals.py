import classes
import json
import os
import pickle
import worlds
multiverse = {}
seed = 5552
chunkSize = 16
worldSize = 1024
currentUniverse = 0
actionLog = []
alteredUniverses = {}
seed = 5000
nextActor = 0
playerId = 0
tileDictionary = {}
tileHash = {}
def insertToActionLog(text):
    actionLog.append(text)
    if len(actionLog) > 5:
        actionLog.pop(0)
def initialize():
    global multiverse
    global currentUniverse
    global chunkSize
def createUniverse(index):
    if index not in multiverse:
        multiverse[index] = classes.Universe(index)
        quickload(index)
        worlds.prepareWorld(index)
def ready():
    global tileDictionary
    tileDictionary = readFromFile("./data/tiles.json",jsonize=True)
    for item in tileDictionary.values():
        tileHash[item["name"]] = item["spriteId"]
    createUniverse(currentUniverse)
def readFromFile(filePath,jsonize=False):
    if os.path.exists(filePath):
        with open(filePath,"r") as f:
            if jsonize:
                return json.loads(f.read())
            else:
                return f.read()
            f.close()
    else:
        raise Exception("ReadFromFile: file path invalid.")
def ifMethodExists(object,methodString):
    testingMethod = getattr(object, methodString, None)
    if callable(testingMethod):
        return True
    else:
        return False
def quicksave(universeNumber):

    savedUniverse = {"tiles":{},"entities":{}}
    if not os.path.exists("worlddata/world"+str(universeNumber)):
        os.mkdir("worlddata/world"+str(universeNumber))
        with open("worlddata/world"+str(universeNumber)+"/world.json","w"): pass
    with open("worlddata/world"+str(universeNumber)+"/world.json", "r") as f:
        file = f.read()
        if file:
            save = json.loads(file)
            savedUniverse["tiles"] = save["tiles"]
        f.close()
        #i'll finish this later, god i'm tired
        #UPDATE, it's finished!
        if universeNumber in multiverse:
            savedUniverse["tiles"][str(universeNumber)] = {}
            savedUniverse["entities"][str(universeNumber)] = {}
            object = multiverse[universeNumber].alteredTerrain.values()
            for item in object:
                savedUniverse["tiles"][str(universeNumber)][str(int(item.pos[0]))+" "+str(int(item.pos[1]))] = item.id
            with open("worlddata/world" + str(universeNumber) + "/entities.json", "wb") as world:
                pickle.dump(multiverse[universeNumber].worldEntities,world)
            with open("worlddata/world"+str(universeNumber)+"/world.json","w") as world:
                json.dump(savedUniverse,world)
                world.close()
            with open("worlddata/world"+str(universeNumber)+"/actors.dat","wb") as world:
                #pickle.dump(multiverse[universeNumber].actors,world)
                world.close()
            with open("data/player.dat","wb") as playerData:
                if currentUniverse in multiverse:
                    if playerId in multiverse[currentUniverse].actors:
                        Player = multiverse[currentUniverse].actors[playerId]
                        Data = {"pos":Player.pos,"universe":Player.currentUniverse}
                        pickle.dump(Data,playerData)
                playerData.close()
def quickload(universeNumber):
    savedUniverse = {"tiles":{}}
    if os.path.exists("worlddata/world"+str(universeNumber)+"/world.json"):
        with open("worlddata/world"+str(universeNumber)+"/world.json","r") as f:
            file = f.read()
            save = json.loads(file)
            if save:
                if multiverse[universeNumber]:
                    for object in save["tiles"][str(universeNumber)]:
                        pos = object.split()
                        tile = save["tiles"][str(universeNumber)][object]
                        if universeNumber in multiverse:
                            multiverse[universeNumber].alteredTerrain[int(pos[0]), int(pos[1])] = classes.Tile(int(pos[0]),int(pos[1]),tile,multiverse[universeNumber])
                        else:
                            createUniverse(universeNumber)
                            multiverse[universeNumber].alteredTerrain[int(pos[0]), int(pos[1])] = [int(pos[0]), int(pos[1]),tile]
                    if os.path.exists("worlddata/world" + str(universeNumber) + "/entities.json") and os.stat("worlddata/world" + str(universeNumber) + "/entities.json").st_size > 0:
                        with open("worlddata/world" + str(universeNumber) + "/entities.json", "rb") as entites:
                            print(universeNumber)
                            print(pickle.load(entites))
                            #multiverse[universeNumber].worldEntities.append(classes.Entity(int(pos[0]),int(pos[1]),"door"))
    if os.path.exists("worlddata/world" + str(universeNumber) + "/actors.dat"):
        with open("worlddata/world" + str(universeNumber) + "/actors.dat", "rb") as f:
            #multiverse[universeNumber].actors = pickle.load(f)
            f.close()
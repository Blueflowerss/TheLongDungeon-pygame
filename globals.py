import classes
import imageThings
import json
import os
import pickle
import pygame
import worlds

multiverse = {}
director = None
keyLocked = False
resolution = (600,600)
chunkSize = 16
worldSize = 1024
boardDistancing = 32

screen = pygame.display.set_mode(resolution)

currentUniverse = 0

actionLog = []
alteredUniverses = {}
seed = 5000
nextActor = 0
playerId = 0
#build stuff
buildType = 0
entityType = 0

images = imageThings.readSprites(resolution)
tileDictionary = {}
entityDictionary = {}
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
    global entityDictionary
    entityDictionary = classes.classFactory.objects.database
    tileDictionary = readFromFile("./data/tiles.json",jsonize=True)
    for item in tileDictionary.values():
        tileHash[item["name"]] = item["spriteId"]
    createUniverse(currentUniverse)
def readFromFile(filePath,jsonize=False,raiseException=True):
    if os.path.exists(filePath):
        with open(filePath,"r") as f:
            if jsonize:
                return json.loads(f.read())
            else:
                return f.read()
            f.close()
    elif raiseException:
        raise Exception("ReadFromFile: file path invalid.")
    else:
        return ""
def ifMethodExists(object,methodString):
    testingMethod = getattr(object, methodString, None)
    if callable(testingMethod):
        return True
    else:
        return False
def entityCreator(classType,sprite=None,pos=(0,0)):

    if classType in entityDictionary:
        entityType = entityDictionary[classType]
        entity = eval("classes."+entityType["class"]+"("+str(pos[0])+","+str(pos[1])+","+"\""+entityType["name"]+"\""+")")
        if "flags" in entityType:
            entity.flags= entityType["flags"]
        if sprite:
            entity.sprite = sprite
        elif "sprite" in entityType:
            entity.sprite = entityType["sprite"]
        return entity
    else:
        print("something's wrong with the entity creator")
def markForSaving(universeNumber):
    multiverse[universeNumber].flags["altered"] = 0
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
            savedUniverse["type"] = multiverse[universeNumber].worldType["internalName"]
            object = multiverse[universeNumber].alteredTerrain
            for pos in object:
                item = object[pos]
                savedUniverse["tiles"][str(universeNumber)][str(int(pos[0]))+" "+str(int(pos[1]))] = item.id
            with open("worlddata/world" + str(universeNumber) + "/entities.json", "wb") as entityFile:
                classes.WorldManager.unloadEntities(universeNumber)
                savedEntities = []
                for entity in multiverse[universeNumber].worldEntities:
                    if "noSave" not in entity.flags:
                        data = {}
                        for attribute in entity.__dict__:
                            if attribute in classes.classFactory.saveableData:
                                data[attribute] = entity.__dict__[attribute]
                        data["devname"] = entity.devname
                        savedEntities.append(data)
                pickle.dump(savedEntities,entityFile)
                entityFile.close()
            with open("worlddata/world"+str(universeNumber)+"/world.json","w") as worldFile:
                json.dump(savedUniverse,worldFile)
                worldFile.close()
            with open("worlddata/world"+str(universeNumber)+"/actors.dat","wb") as actorFile:
                classes.WorldManager.unloadActors(universeNumber)
                savedActors = {}
                for actor in multiverse[universeNumber].worldActors:
                    if "noSave" not in multiverse[universeNumber].worldActors[actor].flags:
                        savedActors[actor] = multiverse[universeNumber].worldActors[actor]
                pickle.dump(savedActors,actorFile)
                actorFile.close()
def savePlayer():
    with open("data/player.dat", "wb") as playerData:
        if currentUniverse in multiverse:
            if playerId in multiverse[currentUniverse].actors:
                Player = multiverse[currentUniverse].actors[playerId]
                Data = {"pos": Player.pos, "universe": Player.currentUniverse}
                pickle.dump(Data, playerData)
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
                            multiverse[universeNumber].alteredTerrain[int(pos[0]), int(pos[1])] = classes.Tile(tile,multiverse[universeNumber])
                        else:
                            createUniverse(universeNumber)
                            multiverse[universeNumber].alteredTerrain[int(pos[0]), int(pos[1])] = [int(pos[0]), int(pos[1]),tile]
                    if os.path.exists("worlddata/world" + str(universeNumber) + "/entities.json"):
                        with open("worlddata/world" + str(universeNumber) + "/entities.json", "rb") as entites:
                            if os.fstat(entites.fileno()).st_size > 0:
                                    tempEntity = pickle.load(entites)
                                    for entity in tempEntity:
                                        newEntity = classes.classFactory.getObject(entity["devname"])
                                        if newEntity != None:
                                            for attribute in entity:
                                                if hasattr(newEntity,attribute):
                                                    setattr(newEntity,attribute,entity[attribute])
                                            classes.classFactory.initObject(newEntity)
                                            multiverse[universeNumber].worldEntities.append(newEntity)
                                        else:
                                            print("Couldn't create entity.")
                    if "save" in save:
                        multiverse[universeNumber].worldType = readFromFile("./data/worldtype.json",True)[save["type"]]
                    if os.path.exists("worlddata/world" + str(universeNumber) + "/actors.dat"):
                        with open("worlddata/world" + str(universeNumber) + "/actors.dat", "rb") as f:
                            global nextActor
                            actors = pickle.load(f)
                            nextActor += len(actors)
                            multiverse[universeNumber].worldActors = actors
                            f.close()
def save_and_quit():
    for universe in multiverse.keys():
        savePlayer()
        if "altered" in multiverse[universe].flags:
            quicksave(universe)

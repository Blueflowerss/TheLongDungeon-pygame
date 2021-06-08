import pygame
import globals
import mathstuff
import math
import random
import worlds
from operator import sub
import functions
from events import Events
clock = pygame.time.Clock()

class Tile:
    def __init__(self,x,y,id,universe):
        if str(id) in globals.tileDictionary:
            tile = globals.tileDictionary[str(id)]
        else:
            tile = globals.tileDictionary[str(globals.tileHash[universe.worldType["ground"]])]
        self.type = tile["behavior"]
        self.spriteId = tile["spriteId"]
        self.name = tile["name"]
        self.id = id
        self.pos = (x,y)
        self.width = 32
        self.height = 32
class Worldtile:
    def __init__(self,x,y,universe,generateStructures=False):
        self.pos = (x,y)
        self.tiles = {}
        self.entities = []
        originX,originY = 0 + self.pos[0] * globals.chunkSize, 0 + self.pos[1] * globals.chunkSize
        for xTile in range(0,globals.chunkSize):
             for yTile in range(0,globals.chunkSize):
                 xPos,yPos = xTile + self.pos[0] * globals.chunkSize,yTile + self.pos[1] * globals.chunkSize
                 if xPos > -1 and yPos > -1 and xPos < globals.worldSize and yPos < globals.worldSize:
                    if (xPos,yPos) in universe.alteredTerrain:
                        self.tiles[xPos,yPos] = universe.alteredTerrain[xPos,yPos]
                    elif (xPos,yPos) in universe.loadedTerrain:
                        self.tiles[xPos,yPos] = universe.loadedTerrain[xPos,yPos]
                    else:
                        perlinTile = mathstuff.generateNoise(universe.index, (xPos), (yPos),worlds.worldTerrain[universe.worldType["terrain"]],1,globals.seed)
                        if perlinTile == 1 and universe.worldType["mountains"]:
                            tile = Tile(xPos,yPos,globals.tileHash[universe.worldType["ground"]],universe)
                            self.tiles[(xPos,yPos)] = tile
                        else:
                            tile = Tile(xPos,yPos,globals.tileHash[universe.worldType["grass"]],universe)
                            self.tiles[(xPos,yPos)] = tile
        toBeDeleted = []
        for entity in universe.worldEntities:
            if entity.pos[0] in range(originX,originX+globals.chunkSize) and entity.pos[1] in range(originY,originY+globals.chunkSize):
                toBeDeleted.append(entity)
                universe.entities.append(entity)
        for entity in toBeDeleted:
            universe.worldEntities.remove(entity)
        if universe.worldType["treeGen"]:
            for number in range(2,universe.worldType["treeAmount"]):
                random.seed(universe.index*xPos*yPos*number)
                spot = random.randint(xPos - globals.chunkSize, xPos), random.randint(yPos - globals.chunkSize,
                                                                       yPos)
                if (spot[0],spot[1]) in self.tiles and (spot[0],spot[1]) not in universe.alteredTerrain:
                    if self.tiles[spot[0],spot[1]].type == "empty":
                        self.tiles[spot[0],spot[1]] = Tile(spot[0],spot[1],globals.tileHash[universe.worldType["tree"]],universe)
class TextInput:
    def __init__(self,x,y,width,height,mode):
        self.pos = (x,y)
        self.dimensions = (width,height)
        self.active = True
        self.mode = mode
    def process(self,text):
        def teleport():
            actor = globals.multiverse[globals.currentUniverse].actors[0]
            if len(text.split()) > 1:
                if text.split()[0].isdigit() and text.split()[1].isdigit():
                    dest  = (int(text.split()[0]),int(text.split()[1]))
                    WorldManager.loadWorldTile(int(dest[0]/globals.chunkSize),int(dest[1]/globals.chunkSize),2,globals.currentUniverse)
                    actor.pos = int(dest[0]),int(dest[1])
        def teleportstep():
            actor = globals.multiverse[globals.currentUniverse].actors[0]
            newText = text.replace("-",chr(45))
            newText = newText.replace("\r","")
            if newText:
                dest = int(newText)
                functions.attemptTravel(actor,globals.currentUniverse,dest,True)
        modes = {"teleport":teleport,"teleportstep":teleportstep}
        if self.mode in modes:
            modes[self.mode]()
class WorldManager:
    def loadWorldTile(x,y,renderDistance,universe):
        ourUniverse = globals.multiverse[universe]
        chunkMove = x,y
        for number in range(-renderDistance, renderDistance):
            for number1 in range(-renderDistance, renderDistance):
                if (chunkMove[0] + number, chunkMove[1] + number1) in ourUniverse.gameBoards:
                    pass
                else:
                    ourUniverse.gameBoards[chunkMove[0] + number, chunkMove[1] + number1] = Worldtile(
                        chunkMove[0] + number, chunkMove[1] + number1,ourUniverse,True)
    def unloadWorldTile(universe,renderDistance=0,centerOfDeletion=(0,0)):
        ourUniverse = globals.multiverse[universe]
        toBeDeleted = []
        entitiesHitList = []
        for object in ourUniverse.gameBoards.values():
                dist = tuple(map(lambda i, j: i - j, (int(centerOfDeletion[0]/16),int(centerOfDeletion[1]/16)),object.pos))
                if abs(dist[0]) > renderDistance or abs(dist[1]) > renderDistance:
                    toBeDeleted.append(object)
        for entity in ourUniverse.entities:
            dist = tuple(map(lambda i, j: i - j, centerOfDeletion,entity.pos))
            if abs(dist[0]) > 100 or abs(dist[1]) > 100:
                ourUniverse.worldEntities.append(entity)
                entitiesHitList.append(entity)
        for object in toBeDeleted:
            ourUniverse.gameBoards.pop(object.pos)
        for entity in entitiesHitList:
            ourUniverse.entities.remove(entity)
        entitiesHitList = None
    def unloadEntities(universe):
        ourUniverse = globals.multiverse[universe]
        hitlist = []
        for entity in ourUniverse.entities:
            ourUniverse.worldEntities.append(entity)
            hitlist.append(entity)
        for entity in hitlist:
            ourUniverse.entities.remove(entity)
class WorldGen:
    def _generate_building(mode,X,Y,width,height,universe):
        def room():
            for x in range(0,width):
                for y in range(0,height):
                    if universe in globals.multiverse:
                        ourUniverse = globals.multiverse[universe]
                        if x==0 or x==width-1 or y==0 or y==height-1:
                            ourUniverse.loadedTerrain[X+x,Y+y] = (X+x,Y+y,2)
                    else:
                        globals.multiverse[universe] = Universe(universe)
                        ourUniverse = globals.multiverse[universe]
                        ourUniverse.loadedTerrain[X + x, Y + y] = (X + x, Y + y,2)
        def square():
            for x in range(0,width):
                for y in range(0,height):
                    if universe in globals.multiverse:
                        ourUniverse = globals.multiverse[universe]
                        ourUniverse.loadedTerrain[X+x,Y+y] = [X+x,Y+y,2]
                    else:
                        globals.multiverse[universe] = Universe(universe)
                        ourUniverse = globals.multiverse[universe]
                        ourUniverse.loadedTerrain[X + x, Y + y] = [X + x, Y + y,2]

        keys = {"room":room,"square":square}
        if mode in keys:
            keys[mode]()


#BASE ENTITIES
class Universe:
    def __init__(self,index,type=None):
        self.index = index
        self.objects = []
        self.actors = {}
        self.board = {}
        self.entities = []
        self.worldEntities = []
        self.objectMap = {}
        self.gameBoards = {}
        self.loadedTerrain = {}
        self.alteredTerrain = {}
        self.altered = False
        if type == None:
            randNumber = int(self.index/20)
            tempNumber = -500000
            random.seed(randNumber)
            choices = []
            if randNumber != tempNumber:
                tempNumber = randNumber
                choices = (random.choices(list(worlds.worldChances.keys()), list(worlds.worldChances.values()), k=20))
            self.worldType = worlds.worldData[list(choices)[self.index%len(choices)]]
        else:
            self.worldType = type
class Entity:
    def __init__(self,x,y,type):
        self.pos = (x,y)
        self.type = type
        self.id = type
class steppingEntity(Entity):
    def __init__(self,x,y,type):
        super().__init__(x,y,type)
    def step(self,distance,origin):
        print(origin+distance)
class Actor(Entity):
    def __init__(self,x,y,id,universe):
        super().__init__(x, y, type)
        self.important = True
        self.type = "actor"
        self.spriteId = 3
        self.id = id
        self.tempchunkPos = (int(self.pos[0]/16),int(self.pos[1]/16))
        self.actionPointsMax = 5
        self.actionPointsRegen = 1
        self.HP = 10
        self.maxHP = 10
        self.currentUniverse = universe
    def move_object(object, amount):
        globals.initialize()
        ourUniverse = globals.multiverse[globals.currentUniverse]
        if (object.pos[0] + amount[0], object.pos[1] + amount[1]) in ourUniverse.board:
            curBoard = ourUniverse.board[tuple(map(sum, zip(object.pos, amount)))]
            move = tuple(map(sum, zip(object.pos, amount)))
            chunkMove = (int(move[0] / globals.chunkSize), int(move[1] / globals.chunkSize))
            def actor():
                pass
            def wall():
                pass
            def door():
                if ourUniverse.objectMap[move].blocks == True:
                    pass
                else:
                    empty()
            def empty():
                object.pos = curBoard.pos
            collisions = {"actor": actor, "wall": wall, "empty": empty,"door":door}
            if (curBoard.pos) in ourUniverse.objectMap:
                target = ourUniverse.objectMap[curBoard.pos]
                if target.type is not None:
                    if target.type in collisions:
                        collisions[target.type]()
                    else:
                        pass
            elif (curBoard.pos) in ourUniverse.board:
                target = ourUniverse.board[curBoard.pos]
                if target.type in collisions:
                    collisions[target.type]()
            else:
                collisions["empty"]()
class furniture(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        self.blocks = False
class furnitureUsable(furniture):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        self.state = False
        self.sprites = None
    def _interact(self):
        if self.state:
            self.state = False
        else:
            self.state = True
#ENTITIES
class Player(Actor):
    def __init__(self,x,y,id,universe):
        super().__init__(x,y,id,universe)
        self.type = "actor"
        self.spriteId = 3
        WorldManager.loadWorldTile(self.tempchunkPos[0], self.tempchunkPos[1], 3, self.currentUniverse)
    def _process(self):
            chunkPos = (int(self.pos[0] / globals.chunkSize), int(self.pos[1] / globals.chunkSize))
            if chunkPos != self.tempchunkPos:
                WorldManager.loadWorldTile(chunkPos[0], chunkPos[1], 3, globals.currentUniverse)
                WorldManager.unloadWorldTile(globals.currentUniverse,3, self.pos)
                self.tempchunkPos = chunkPos
class Enemy(Actor):
    def __init__(self,x,y,id,universe):
        super().__init__(self,x,y,id,universe)
        self.type = "enemy"
        self.spriteId = 3
        self.pos = (x,y)
        self.id = id
        self.actionPointsMax = 5
        self.actionPointsRegen = 1
        self.HP = 10
        self.maxHP = 10
        self.currentUniverse = 0
    def _process(self):
        globals.initialize()
        ourUniverse = globals.multiverse[globals.currentUniverse]
        if 0 > 3:
            target = ourUniverse.actors[0]
            direction = pygame.math.Vector2(tuple(map(sub,target.pos,self.pos))).normalize()
            direction = (math.floor(direction.x),math.floor(direction.y))
            self.move_object(direction)
class Door(furnitureUsable):
    def __init__(self, x, y, type):
        super().__init__(x,y,type)
        jsonObject = globals.readFromFile("data/entityType.json", True)[type]
        self.sprites = (jsonObject["trueSprite"], jsonObject["falseSprite"])
    def _process(self):
        if self.state:
            self.blocks = True
        else:
            self.blocks = False





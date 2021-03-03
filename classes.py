import pygame
import globals
import math
import numpy as np
from operator import sub
import functions
clock = pygame.time.Clock()
class Tile:
    def __init__(self,x,y,id):
        def empty():
            self.type = "empty"
            self.spriteId = 4
            self.pos = (x,y)
            self.width = 32
            self.height = 32
        def wall():
            self.type = "wall"
            self.spriteId = 2
            self.pos = (x,y)
            self.width = 32
            self.height = 32
        matchCase = {"empty":empty,"wall":wall}
        if id in matchCase:
            matchCase[id]()
class Worldtile:
    def __init__(self,x,y,chunkSize):
        self.x = x
        self.y = y
        self.tiles = {}
        for x in range(0,chunkSize):
            for y in range(0,chunkSize):
                tile = Tile(x*self.x,y*self.y,"empty")
                self.tiles[(x,y)] = tile
class Universe:
    def __init__(self,index):
        self.index = index
        self.objects = []
        self.items = []
        self.board = {}
        self.objectMap = {}
        self.gameBoards = {}
class Actor():
    def __init__(self,x,y):
        self.type = "enemy"
        self.spriteId = 2
        self.pos = (x,y)

    def _process(self):
        pass
    def move_object(object,amount):
        globals.initialize()
        ourUniverse = globals.multiverse[globals.currentUniverse]
        if (tuple(map(sum, zip(object.pos, amount)))) in ourUniverse.board:
            curBoard = ourUniverse.board[tuple(map(sum, zip(object.pos, amount)))]
            def actor():
                pass
            def wall():
                pass
            def empty():
                object.pos=curBoard.pos
            def enemy():
                pass
            collisions = {"actor":actor,"wall":wall,"empty":empty,"enemy":enemy}
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
           # else:
            #w    collisions["empty"]()
class Enemy:
    def __init__(self,x,y):
        self.type = "enemy"
        self.spriteId = 3
        self.pos = (x,y)
    def _process(self):
        globals.initialize()
        ourUniverse = globals.multiverse[globals.currentUniverse]
        if len(ourUniverse.objects) > 0:
            target = ourUniverse.objects[0]
            direction = pygame.math.Vector2(tuple(map(sub,target.pos,self.pos))).normalize()
            direction = (math.floor(direction.x),math.floor(direction.y))
            self.move_object(direction)
    def move_object(object,amount):
        globals.initialize()
        ourUniverse = globals.multiverse[globals.currentUniverse]
        if (tuple(map(sum, zip(object.pos, amount)))) in ourUniverse.board:
            curBoard = ourUniverse.board[tuple(map(sum, zip(object.pos, amount)))]
            def actor():
                pass
            def wall():
                pass
            def empty():
                object.pos=curBoard.pos
            def enemy():
                pass
            collisions = {"actor":actor,"wall":wall,"empty":empty,"enemy":enemy}
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
            #else:
                collisions["empty"]()
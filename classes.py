import pygame
import globals
import math
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

class Universe:
    def __init__(self,index):
        self.index = index
        self.objects = []
        self.items = []
        self.board = {}
        self.objectMap = {}
class Actor():
    def __init__(self,x,y):
        self.type = "enemy"
        self.spriteId = 2
        self.pos = (x,y)

    def _process(self):
        pass
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
            self.move_object()
    def move_object(amount):
        globals.initialize()
        ourUniverse = globals.multiverse[globals.currentUniverse]
        if (tuple(map(sum, zip(self.pos, amount)))) in ourUniverse.board:
            curBoard = ourUniverse.board[tuple(map(sum, zip(pos, amount)))]
            def actor():
                pass
            def wall():
                pass
            def empty():
                self.pos=curBoard.pos
            collisions = {"actor":actor,"wall":wall,"empty":empty}
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
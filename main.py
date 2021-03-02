import pygame
import functions
import globals
import classes
import os
from enum import Enum
from ast import literal_eval
dirPath = "sprites"
clock = pygame.time.Clock()


images = []
for file in os.listdir(dirPath):
    images.append(pygame.image.load(os.path.join("sprites",file)))
for number in range(0,len(images)):
    images[number] = pygame.transform.scale(images[number],(32,32))
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Ariel",24)
resolution = (800,1000)
screen = pygame.display.set_mode(resolution,pygame.RESIZABLE)
images.append(pygame.image.load(r"/home/ajaag/Pictures/kumoniko.png"))
boardDistancing = 35
cameraOffsetX = 0
cameraOffsetY = 0
scale = 0
activeBoard = {}
globals.initialize()
globals.ready()
ourUniverse = globals.multiverse[globals.currentUniverse]
def change_distance_size(amount):
    global boardDistancing
    boardDistancing += amount
    #print(boardDistancing)
for number in range(2,5):
    #ourUniverse["objects"].append(classes.Actor(number,1))
    ourUniverse.objects.append(classes.Actor(20,10))
for number in range(2,5):
    ourUniverse.objects.append(classes.Enemy(2*8,5))
boxSize = 50
for x in range(1,boxSize):
    for y in range(1,boxSize):
        if x == 1 or x == boxSize-1 or y == 1 or y == boxSize-1:
            shape = classes.Tile(x,y,"wall")
        else:
            shape = classes.Tile(x, y, "empty")
        ourUniverse.board[x,y] = shape
            #collisions[target["type"]]()
class control(Enum):
    MOVE = 1
    DIG = 2
currentControl = control.MOVE
def keyHandler(key):
    def DIG(direction):
        tile = tuple(map(sum, zip(ourUniverse.objects[0].pos,direction)))
        functions.alter_tile(tile,"empty")
        global currentControl
        currentControl = control.MOVE
    def MOVE(direction):
        functions.move_object(ourUniverse.objects[0], direction)
    def controlHandler(direction):
        if direction:
            mode = {1:MOVE,2:DIG}
            if currentControl.value in mode:
                mode[currentControl.value](direction)
    def up():
        controlHandler((0,-1))
    def down():
        controlHandler((0,1))
    def left():
        controlHandler((-1,0))
    def right():
        controlHandler((1,0))
    def lowerLeft():
        controlHandler((-1,1))
    def lowerRight():
        controlHandler((1,1))
    def upperLeft():
        controlHandler((-1, -1))
    def upperRight():
        controlHandler((1, -1))
    def escape():
        quit()
    def v():
        global currentControl
        currentControl = control.DIG
    def q():
        change_distance_size(5)
        _render_screen()
    def e():
        change_distance_size(-5)
        _render_screen()
    def z():
        pass
    def c():
        pass
    keys = {119:up,115:down,97:left,100:right,113:q,101:e,27:escape,122:escape,99:c,118:v,1073741913:lowerLeft,1073741914:down,1073741915:lowerRight,1073741918:right,1073741916:left,
            1073741919:upperLeft,1073741920:up,1073741921:upperRight}
    if key in keys:
        keys[key]()
    _update()


def _render_text(text):
    return font.render(text,False,(255,255,255))

def _render_screen():

    screen.fill((0, 0, 0))
    if len(ourUniverse.objects) > 0:
        cameraOffsetX, cameraOffsetY = ourUniverse.objects[0].pos[0] * -boardDistancing + resolution[0]/2, ourUniverse.objects[0].pos[1] * -boardDistancing + resolution[1] / 2
    for object in ourUniverse.board.values():
        screen.blit(images[object.spriteId],(object.pos[0] * boardDistancing + cameraOffsetX, object.pos[1] * boardDistancing + cameraOffsetY))

    for object in ourUniverse.objects:
        if object.pos[0] < object.pos[0] * boardDistancing + cameraOffsetX+resolution[0]/2 and object.pos[1] < object.pos[1] * boardDistancing + cameraOffsetY+resolution[1]/2:
            screen.blit(images[3],(object.pos[0] * boardDistancing + cameraOffsetX, object.pos[1] * boardDistancing + cameraOffsetY))
    screen.blit(_render_text(str(ourUniverse.objects[0].pos)), (25, 5))
def _update_board():
    ourUniverse.objectMap = {}
    for object in ourUniverse.objects:
        ourUniverse.objectMap[object.pos] = object
        #Process what the object does
        object._process()
def _update():
    _update_board()
    _render_screen()
_update()
while True:
    globals.initialize()
    pygame.event.pump()
    #USED FOR COLLISIONS
    ########## RENDERING
    mousePos = pygame.mouse.get_pos()
    mousePos = {"X":mousePos[0],"Y":mousePos[1]}

    for event in pygame.event.get():
        pygame.key.set_repeat(150,50)
        if event.type == pygame.KEYDOWN:
          if "key" in event.__dict__:
              pressed = event.__dict__["key"]
              keyHandler(pressed)
        elif event.type == pygame.VIDEORESIZE:
            resolution = pygame.display.get_window_size()

    #CAMERA

    #######
    pygame.display.flip()
    clock.tick(60)
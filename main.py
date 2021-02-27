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

for number in range(1,5):
    #ourUniverse["objects"].append(classes.Actor(number,1))
    ourUniverse.objects.append(classes.Actor(number,1))
for x in range(1,50):
    for y in range(1,50):
        shape = classes.Tile(x,y)
        ourUniverse.board[x,y] = shape

            #collisions[target["type"]]()
class control(Enum):
    MOVE = 1
    INPUT = 2
currentControl = control.MOVE
def keyHandler(key):
    def w():
        global direction
        direction = (0,-1)
    def s():
        global direction
        direction = (0,1)
    def a():
        global direction
        direction = (-1,0)
    def d():
        global direction
        direction = (1,0)
    def escape():
        quit()
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
    keys = {119:w,115:s,97:a,100:d,113:q,101:e,27:escape,122:escape,99:c}
    if key in keys:
        keys[key]()
    def INPUT():
        pass
    def MOVE():
        global direction
        functions.move_object(ourUniverse.objects[0], direction)
        direction = (0,0)
    mode = {1:MOVE,2:INPUT}
    if currentControl.value in mode:
        mode[currentControl.value]()

    _update()
def _render_screen():
    screen.fill((0, 0, 0))

    if len(ourUniverse.objects) > 0:
        cameraOffsetX, cameraOffsetY = ourUniverse.objects[0].x * -boardDistancing + resolution[0]/2, ourUniverse.objects[0].y * -boardDistancing + resolution[1] / 2
    cameraXmin,cameraXmax = int(-cameraOffsetX/boardDistancing), int(-cameraOffsetX/boardDistancing+resolution[0]/2)
    cameraYmin, cameraYmax = int(-cameraOffsetY / boardDistancing), int(-cameraOffsetY / boardDistancing + resolution[1] / 2)

    for object in ourUniverse.board.values():
        screen.blit(images[4],(object.x * boardDistancing + cameraOffsetX, object.y * boardDistancing + cameraOffsetY))

    for object in ourUniverse.objects:
        if object.x < object.x * boardDistancing + cameraOffsetX+resolution[0]/2 and object.y < object.y * boardDistancing + cameraOffsetY+resolution[1]/2:
            screen.blit(images[3],(object.x * boardDistancing + cameraOffsetX, object.y * boardDistancing + cameraOffsetY))
def _update_board():
    ourUniverse.objectMap = {}
    for object in ourUniverse.objects:
        ourUniverse.objectMap[object.x,object.y] = object
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

    #screen.blit(image,(0,0))

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
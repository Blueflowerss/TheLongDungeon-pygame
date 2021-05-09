import pygame
import functions
import globals
import classes
import mathstuff
import os
import pickle
import worlds
from enum import Enum
dirPath = "sprites"
clock = pygame.time.Clock()
tempImages = {"images_alpha":{},"images_nostretch":{}}
images ={}
imagekeys = []
for file in sorted(os.listdir(dirPath)):
    if file.endswith("_A"):
        tempImages["images_alpha"][int(file[:4])] = (pygame.image.load(os.path.join("sprites",file)))
        imagekeys.append(int(file[:4]))
    elif file.endswith("_nostretch"):
        tempImages["images_nostretch"][int(file[:4])] = (pygame.image.load(os.path.join("sprites",file)))
        imagekeys.append(int(file[:4]))
    else:
        images[int(file[:4])] = (pygame.image.load(os.path.join("sprites",file)))
        imagekeys.append(int(file[:4]))
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Ariel",24)
resolution = (600,600)
screen = pygame.display.set_mode(resolution,pygame.RESIZABLE)
for number in imagekeys:
    if number in images:
        images[number] = pygame.transform.scale(images[number],(32,32))
        images[number] = images[number].convert()
    elif number in tempImages["images_alpha"]:
        tempImages["images_alpha"][number] = pygame.transform.scale(tempImages["images_alpha"][number], (32, 32))
        images[number] = tempImages["images_alpha"][number].convert_alpha()
    elif number in tempImages["images_nostretch"]:
        images[number] = tempImages["images_nostretch"][number].convert_alpha()

#board related stuff
boardDistancing = 32
cameraOffsetX = 0
cameraOffsetY = 0
currentBoard = 0
buildType = 0
#multiverse related stuff
worlds.ready()
globals.initialize()
globals.ready()

ourUniverse = globals.multiverse[globals.currentUniverse]
#actor related stuff
currentActor = 0
#window related stuff
text = ""
guiInput = {}
currentWindow = ""

if os.path.exists("data/player.dat"):
    if os.stat("data/player.dat").st_size > 0:
        with open("data/player.dat", "rb") as f:
            player = pickle.load(f)
            if player["universe"] in globals.multiverse:
                functions.prepareUniverse(player["universe"])
                globals.multiverse[player["universe"]].actors[globals.playerId] =\
                    classes.Actor(player["pos"][0], player["pos"][1], globals.playerId, player["universe"])
            else:
                globals.multiverse[player["universe"]] = classes.Universe(player["universe"])
                functions.prepareUniverse(player["universe"])
                globals.multiverse[player["universe"]].actors[globals.playerId] =\
                    classes.Actor(player["pos"][0], player["pos"][1], globals.playerId, player["universe"])
            globals.currentUniverse = player["universe"]
            globals.nextActor += 1
else:
    ourUniverse.actors[globals.playerId] = classes.Actor(50, 50, 0, 0)
globals.insertToActionLog("For controls check Readme!")
for number in range(0,1):
    pass
    #ourUniverse.actors[globals.nextActor] = classes.Enemy(10,10,globals.nextActor,0)
    #globals.nextActor += 1   #collisions[target["type"]]()
#for number in range(0,5):
#    ourUniverse.gameBoards[(number,number)] = classes.Worldtile(number,number,16)
class control(Enum):
    MOVE = 1
    DIG = 2
    BUILD = 3
currentControl = control.MOVE
def keyHandler(key):

    def DIG(direction):
        ourUniverse = globals.multiverse[globals.currentUniverse]
        tile = tuple(map(sum, zip(ourUniverse.actors[currentActor].pos,direction)))
        functions.alter_tile(tile,globals.tileHash[str(globals.multiverse[globals.currentUniverse].worldType["grass"])])
        global currentControl
        _update_board(ourUniverse)
        currentControl = control.MOVE
    def BUILD(direction):
        ourUniverse = globals.multiverse[globals.currentUniverse]
        tile = tuple(map(sum, zip(ourUniverse.actors[currentActor].pos,direction)))
        tiles = list(globals.tileDictionary)
        functions.alter_tile(tile,tiles[buildType%len(globals.tileDictionary)])
        global currentControl
        _update_board(ourUniverse)
        currentControl = control.MOVE
    def MOVE(direction):
        globals.multiverse[globals.currentUniverse].actors[currentActor].move_object(direction)
    def controlHandler(direction):
        if direction:
            mode = {1:MOVE,2:DIG,3:BUILD}
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
            for universe in globals.multiverse.keys():
                globals.quicksave(universe)
            quit()
    def v():
        global currentControl
        currentControl = control.DIG
    def q():
        global buildType
        buildType -= 1
    def e():
        global buildType
        buildType += 1
    def z():
        global text
        global currentWindow
        text = ""
        guiInput["teleportstep"] = classes.TextInput(50,270,120,60,"teleportstep")
        currentWindow = "teleportstep"
    def x():
        global text
        global currentWindow
        text = ""
        guiInput["teleport"] = classes.TextInput(50,200,120,60,"teleport")
        currentWindow = "teleport"
    def c():
        global currentControl
        currentControl = control.BUILD
    def travelForward():
        functions.attemptTravel(globals.multiverse[globals.currentUniverse].actors[currentActor],globals.currentUniverse,globals.currentUniverse+1)
        _update(globals.multiverse[globals.currentUniverse])
    def travelBackward():
        functions.attemptTravel(globals.multiverse[globals.currentUniverse].actors[currentActor], globals.currentUniverse, globals.currentUniverse-1)
        _update(globals.multiverse[globals.currentUniverse])
    def D4C():
        global boardDistancing
        boardDistancing += 8
    def spawnActor():
        global boardDistancing
        boardDistancing -= 8
    def clearInput():
        global text
        global guiInput
        if currentWindow in guiInput:
            guiInput[currentWindow].process(text)
            guiInput.pop(currentWindow)
        text = ""
        guiInput = {}
    keys = {119:up,115:down,97:left,100:right,113:q,101:e,27:escape,122:z,99:c,118:v,1073741913:lowerLeft,1073741914:down,1073741915:lowerRight,1073741918:right,1073741916:left,
            1073741919:upperLeft,1073741920:up,1073741921:upperRight,120:x,106:travelBackward,107:travelForward,44:D4C,46:spawnActor,
            13:clearInput}
    #print(key)
    if key in keys:
        keys[key]()
    for universe in globals.multiverse.values():
        _update(universe)
def _render_text(text):
    return font.render(text,False,(255,255,255))
def _render_screen(universe):
    screen.fill((0, 0, 0))
    global currentActor
    if currentActor in universe.actors:
        cameraOffsetX, cameraOffsetY = universe.actors[currentActor].pos[0] * -boardDistancing + resolution[0]/2, universe.actors[currentActor].pos[1] * -boardDistancing + resolution[1] / 2
    else:
        cameraOffsetX, cameraOffsetY = 0,0
    for object in universe.board.values():
        #add tiling
        screen.blit(images[object.spriteId],(object.pos[0] * boardDistancing + cameraOffsetX, object.pos[1] * boardDistancing + cameraOffsetY))
    for object in universe.actors.values():
        screen.blit(images[3],(object.pos[0] * boardDistancing + cameraOffsetX, object.pos[1] * boardDistancing + cameraOffsetY))
    for action in range(0,len(globals.actionLog)):
        screen.blit((_render_text(globals.actionLog[action])),(0,80+20*action))
    if currentActor in universe.actors:
        screen.blit(_render_text(str(universe.actors[currentActor].pos)), (25, 5))
        screen.blit(_render_text(str((int(universe.actors[currentActor].pos[0]/globals.chunkSize),int(universe.actors[currentActor].pos[1]/globals.chunkSize)))), (25, 25))
    else:
        screen.blit(_render_text("Actor not!"), (25, 5))
    for menu in guiInput.values():
        pygame.draw.rect(screen,(128,128,128),(menu.pos,menu.dimensions))
        if currentWindow in guiInput:
            screen.blit(_render_text(menu.mode), (menu.pos))
            screen.blit(_render_text(text),(menu.pos[0],menu.pos[1]+20))
    screen.blit(_render_text(str(list(globals.tileDictionary)[buildType%len(globals.tileDictionary)])), (60, 50))
    screen.blit(_render_text("universe "+str(globals.currentUniverse)), (resolution[0]/2-20, 20))
    screen.blit(_render_text(str(globals.multiverse[globals.currentUniverse].worldType["name"])), (resolution[0] / 2 - 20,40))
    screen.blit(images[globals.tileDictionary[list(globals.tileDictionary)[buildType%len(globals.tileDictionary)]]["spriteId"]],(10,50))
    screen.blit(_render_text(str(pygame.mouse.get_pos())), (10, 40))
def _update_objects(universe):
    universe.objectMap = {}
    for actor in universe.actors.values():
        universe.objectMap[actor.pos] = actor
        actor._process()
    for object in universe.objects:
        universe.objectMap[object.pos] = object
        #Process what the object does
        object._process()
def _update_board(universe):
    universe.board = {}
    for board in universe.gameBoards.values():
        for tile in board.tiles.values():
            universe.board[tile.pos] = tile
def _update(universe):
    #process actors and objects
    _update_objects(universe)
    #process changes on the board
    _update_board(universe)
    #render this mess
    if currentActor in universe.actors:
        _render_screen(universe)
for universe in globals.multiverse:
    _update(globals.multiverse[universe])
while True:
    globals.initialize()
    pygame.event.pump()
    mousePos = pygame.mouse.get_pos()
    mousePos = {"X":mousePos[0],"Y":mousePos[1]}
    for event in pygame.event.get():
        pygame.key.set_repeat(250,50)
        if event.type == pygame.KEYDOWN:
          if "key" in event.__dict__:
              text += event.__dict__["unicode"]
              pressed = event.__dict__["key"]
              keyHandler(pressed)
        elif event.type == pygame.VIDEORESIZE:
            resolution = pygame.display.get_window_size()

    #CAMERA

    #######
    pygame.display.flip()
    clock.tick(60)

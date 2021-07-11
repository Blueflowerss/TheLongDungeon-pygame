from enum import Enum

import classes,scenes
import functions
import globals
import pygame,pygame_gui,GUI
import worlds


class control(Enum):
    MOVE = 1
    DIG = 2
    BUILD = 3
    INTERACT = 4
    BUILDENTITY = 5
currentControl = control.MOVE
currentActor = globals.playerId
def keyHandler(scene,key):
    def DIG(direction):
        ourUniverse = globals.multiverse[globals.currentUniverse]
        tile = tuple(map(sum, zip(ourUniverse.actors[currentActor].pos,direction)))
        functions.alter_tile(tile,globals.tileHash[str(globals.multiverse[globals.currentUniverse].worldType["grass"])])
        global currentControl
        worlds._update_board(ourUniverse)
        currentControl = control.MOVE
    def BUILD(direction):
        ourUniverse = globals.multiverse[globals.currentUniverse]
        tile = tuple(map(sum, zip(ourUniverse.actors[currentActor].pos,direction)))
        tiles = list(globals.tileDictionary)
        functions.alter_tile(tile,tiles[globals.buildType%len(globals.tileDictionary)])
        global currentControl
        worlds._update_board(ourUniverse)
        currentControl = control.MOVE
    def BUILDENTITY(direction):
        ourUniverse = globals.multiverse[globals.currentUniverse]
        pos = tuple(map(sum, zip(ourUniverse.actors[currentActor].pos,direction)))
        entity = globals.entityCreator(str(list(globals.entityDictionary)[globals.entityType % len(globals.entityDictionary)]),pos=(pos[0],pos[1]))
        ourUniverse.flags["altered"] = 0
        ourUniverse.entities.append(entity)
        global currentControl
        worlds._update_board(ourUniverse)
        currentControl = control.MOVE
    def MOVE(direction):
        globals.multiverse[globals.currentUniverse].actors[currentActor].move_object(direction)
    def INTERACT(direction):
        ourUniverse = globals.multiverse[globals.currentUniverse]
        tile = tuple(map(sum, zip(ourUniverse.actors[currentActor].pos,direction)))
        if tile in ourUniverse.objectMap:
            entity = ourUniverse.objectMap[tile]
            if "interactible" in entity.flags:
                entity._interact()
        global currentControl
        worlds._update_board(ourUniverse)
        currentControl = control.MOVE
    def controlHandler(direction):
        if direction:
            mode = {1:MOVE,2:DIG,3:BUILD,4:INTERACT,5:BUILDENTITY}
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
    def middle():
        controlHandler((0,0))
    def escape():
        scene.director.change_scene(scenes.menuScene)
    def v():
        global currentControl
        currentControl = control.DIG
    def q():
        global buildType
        globals.buildType -= 1
    def e():
        globals.buildType += 1
    def z():
        pass
    def x():
        pass
    def c():
        global currentControl
        currentControl = control.BUILD
    def travelForward():
        functions.attemptTravel(globals.multiverse[globals.currentUniverse].actors[currentActor],globals.currentUniverse,globals.currentUniverse+1)
        worlds._update(globals.multiverse[globals.currentUniverse])
    def travelBackward():
        functions.attemptTravel(globals.multiverse[globals.currentUniverse].actors[currentActor], globals.currentUniverse, globals.currentUniverse-1)
        worlds._update(globals.multiverse[globals.currentUniverse])
    def D4C():
        globals.entityType -= 1
    def spawnActor():
        globals.entityType += 1
    def clearInput():
        pass
    def placeEntity():
        global currentControl
        currentControl = control.BUILDENTITY
    def yetAnotherDebugButton():
        scene.director.GUI["teleport"] = GUI.teleportMenu(scene.director.manager)
    def interact():
        global currentControl
        currentControl = control.INTERACT
    keys = {"w":up,"s":down,"a":left,"d":right,"q":q,"e":e,"\x1b":escape,"z":z,"c":c,"v":v,1073741913:lowerLeft,1073741914:down,1073741915:lowerRight,1073741918:right,1073741916:left,
            1073741919:upperLeft,1073741920:up,1073741921:upperRight,1073741917:middle,"x":x,"j":travelBackward,"k":travelForward,44:D4C,46:spawnActor,
            13:clearInput,32:interact,98:placeEntity,103:yetAnotherDebugButton}
    if key.type == pygame.KEYDOWN:
        if key.unicode in keys:
            keys[key.unicode]()
        elif key.key in keys:
            keys[key.key]()
    elif key.type == pygame.QUIT:
        print("ass")
    worlds._update(globals.multiverse[globals.currentUniverse])
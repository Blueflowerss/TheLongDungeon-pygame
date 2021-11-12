import os
import pickle

import pygame

import classes
import functions
import globals
import scenes
import worlds,classFactory
clock = pygame.time.Clock()
classFactory.loadObjects()
pygame.init()
pygame.font.init()
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.key.set_repeat(300,50)
#board related stuff
#multiverse related stuff
worlds.ready()
globals.initialize()
globals.ready()

director = scenes.Director()
director.change_scene(scenes.menuScene)
globals.director = director
#actor related stuff
globals.createUniverse(0)
ourUniverse = globals.multiverse[0]
currentActor = 0
#window related stuff
text = ""
guiInput = {}
currentWindow = ""
print("Another hello from Blueflowers.")
if os.path.exists("data/player.dat"):
    if os.stat("data/player.dat").st_size > 0:
        with open("data/player.dat", "rb") as f:
            player = pickle.load(f)
            if player["universe"] in globals.multiverse:
                globals.createUniverse(player["universe"])
                globals.multiverse[player["universe"]].actors[globals.playerId] =\
                    classes.Player(player["pos"][0], player["pos"][1], globals.playerId, player["universe"])
            else:
                globals.createUniverse(player["universe"])
                globals.multiverse[player["universe"]].actors[globals.playerId] =\
                    classes.Player(player["pos"][0], player["pos"][1], globals.playerId, player["universe"])
            globals.currentUniverse = player["universe"]
            globals.nextActor += 1
    else:
        ourUniverse.actors[globals.playerId] = classes.Player(50, 50, 0, 0)
        globals.nextActor += 1
        print(1)
else:
    ourUniverse.actors[globals.playerId] = classes.Player(50, 50, 0, 0)
    globals.nextActor += 1
    print(2)
if globals.readFromFile("data/splashtext.txt") != "":
    globals.insertToActionLog(globals.readFromFile("data/splashtext.txt"))
else:
    globals.insertToActionLog("For controls check Readme!")
director.loop()
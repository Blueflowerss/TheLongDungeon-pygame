import os
import pickle

import pygame

import classes
import functions
import globals
import scenes
import worlds,classFactory
clock = pygame.time.Clock()
tempImages = {"images_alpha":{},"images_nostretch":{}}
images ={}
imagekeys = []
pygame.init()
pygame.font.init()
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.key.set_repeat(300,50)
#board related stuff

#multiverse related stuff
worlds.ready()
globals.initialize()
globals.ready()
classFactory.loadItems()
director = scenes.Director()
director.change_scene(scenes.menuScene)
globals.director = director
ourUniverse = globals.multiverse[globals.currentUniverse]
#actor related stuff
currentActor = 0
#window related stuff
text = ""
guiInput = {}
currentWindow = ""
print("Another hello from Zeya.")
if os.path.exists("data/player.dat"):
    if os.stat("data/player.dat").st_size > 0:
        with open("data/player.dat", "rb") as f:
            player = pickle.load(f)
            if player["universe"] in globals.multiverse:
                functions.prepareUniverse(player["universe"])
                globals.multiverse[player["universe"]].actors[globals.playerId] =\
                    classes.Player(player["pos"][0], player["pos"][1], globals.playerId, player["universe"])
            else:
                globals.multiverse[player["universe"]] = classes.Universe(player["universe"])
                functions.prepareUniverse(player["universe"])
                globals.multiverse[player["universe"]].actors[globals.playerId] =\
                    classes.Player(player["pos"][0], player["pos"][1], globals.playerId, player["universe"])
            globals.currentUniverse = player["universe"]
            globals.nextActor += 1
    else:
        ourUniverse.actors[globals.playerId] = classes.Player(50, 50, 0, 0)
        globals.nextActor += 1
else:
    ourUniverse.actors[globals.playerId] = classes.Player(50, 50, 0, 0)
    globals.nextActor += 1
if globals.readFromFile("data/splashtext.txt") != "":
    globals.insertToActionLog(globals.readFromFile("data/splashtext.txt"))
else:
    globals.insertToActionLog("For controls check Readme!")
director.loop()
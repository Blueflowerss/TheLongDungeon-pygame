import pygame
import classes
multiverse = {}
currentUniverse = 0
def initialize():
    global multiverse
    global currentUniverse

def createUniverse(index):
    multiverse[index] = classes.Universe(index)
def ready():
    createUniverse(currentUniverse)

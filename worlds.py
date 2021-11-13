import globals
import random
import classes
import imageThings,pygame
#handles world types
worldData = {}
worldTerrain = {
    "plains":0.08,"mountains":0.04
}
worldChances = {}
resolution = (600,600)

def initialize():
    global worldData
def ready():
    global worldData
    worldData = globals.readFromFile("./data/worldtype.json",True)
    for type in worldData:
        worldChances[type] = worldData[type]["chance"]

def prepareWorld(universe):
    if globals.multiverse[universe].worldType["buildings"]:
        pass
        #classes.WorldGen.populateSquare(index)
def _update_objects(universe):
    universe.objectMap = {}
    aliveActors = []
    for actor in universe.actors.values():
        if actor.pos in universe.objectMap:
            universe.objectMap[actor.pos].append(actor)
        else:
            universe.objectMap[actor.pos] = []
        if actor.alive:
            aliveActors.append(actor)
    for object in universe.entities:
        #gotta create a list of objects at the coordinate, then add objects to that list
        #Objectmap is essentially a collision map, without it you couldn't interact with anything.
        def addAllObjects():
            if object.pos in universe.objectMap:
                universe.objectMap[object.pos].append(object)
            else:
                universe.objectMap[object.pos] = []
                addAllObjects()
        addAllObjects()
        # Process what the object does
        if globals.ifMethodExists(object, "_process"):
            object._process()
    for actor in aliveActors:
        actor._process()

def _update_board(universe):
    universe.board = {}
    for board in universe.gameBoards.values():
        for tile in board.tiles:
            universe.board[tile] = board.tiles[tile]

def _update():
    for universe in globals.multiverse:
        universe = globals.multiverse[universe]
        # process actors and objects
        _update_objects(universe)
        # process changes on the board
        _update_board(universe)
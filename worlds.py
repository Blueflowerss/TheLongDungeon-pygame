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
images = imageThings.readSprites((600,600))
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
    if globals.multiverse[universe].worldType["treeGen"]:
        for number in range(1,globals.multiverse[universe].worldType["treeAmount"]):
            xPos,yPos = int(random.uniform(1,globals.worldSize)),int(random.uniform(1,globals.worldSize))
            globals.multiverse[universe].loadedTerrain[xPos,yPos] = classes.Tile(globals.tileHash[globals.multiverse[universe].
                                                                                 worldType["ground"]],globals.multiverse[universe])
            #print(str(xPos)+" "+str(yPos))
def _render_screen(screen,universe):
    def _render_text(text):
        return font.render(text, False, (255, 255, 255))

    boardDistancing = globals.boardDistancing
    resolution = screen.get_size()
    # necessary?
    font = pygame.font.SysFont("Ariel", 24)
    screen.fill((80, 80, 80))
    universe = globals.multiverse[globals.currentUniverse]
    currentActor = globals.playerId
    if globals.playerId in universe.actors:
        cameraOffsetX, cameraOffsetY = universe.actors[currentActor].pos[0] * -boardDistancing + resolution[
            0] / 2, universe.actors[currentActor].pos[1] * -boardDistancing + resolution[1] / 2
    else:
        cameraOffsetX, cameraOffsetY = 0, 0
    for pos in universe.board:
        object = universe.board[pos]
        if (pos[0], pos[1] - 1) in universe.board and (pos[0], pos[1] + 1) in universe.board and (
                pos[0] + 1, pos[1]) in universe.board and (pos[0] - 1, pos[1]) in universe.board:
            if "blocks" in universe.board[pos[0], pos[1] - 1].flags \
                    and "blocks" in universe.board[pos[0], pos[1] + 1].flags \
                    and "blocks" in universe.board[pos[0] + 1, pos[1]].flags \
                    and "blocks" in universe.board[pos[0] - 1, pos[1]].flags:
                pass
            else:
                screen.blit(images[object.spriteId], (
                    pos[0] * boardDistancing + cameraOffsetX, pos[1] * boardDistancing + cameraOffsetY))
    for object in universe.entities:
        if "spriteOffset" in object.flags:
            offset = object.flags["spriteOffset"]
            screen.blit(images[object.sprite], (
                (object.pos[0] * boardDistancing + cameraOffsetX) + offset[0],
                (object.pos[1] * boardDistancing + cameraOffsetY) + offset[1]))
        else:
            screen.blit(images[object.sprite], (
                object.pos[0] * boardDistancing + cameraOffsetX,
                object.pos[1] * boardDistancing + cameraOffsetY))
    for object in universe.actors.values():
        screen.blit(images[3], (
            object.pos[0] * boardDistancing + cameraOffsetX, object.pos[1] * boardDistancing + cameraOffsetY))
    for action in range(0, len(globals.actionLog)):
        screen.blit((_render_text(globals.actionLog[action])), (0, 80 + 20 * action))
    if currentActor in universe.actors:
        screen.blit(_render_text(str(universe.actors[currentActor].pos)), (25, 5))
        screen.blit(_render_text(str((int(universe.actors[currentActor].pos[0] / globals.chunkSize),
                                      int(universe.actors[currentActor].pos[1] / globals.chunkSize)))),
                    (25, 25))
    else:
        screen.blit(_render_text("Actor not!"), (25, 5))
    screen.blit(_render_text(str(list(globals.tileDictionary)[globals.buildType % len(globals.tileDictionary)])),
                (60, 50))
    screen.blit(
        _render_text(str(list(globals.entityDictionary)[globals.entityType % len(globals.entityDictionary)])),
        (10, 190))
    screen.blit(_render_text("earth " + str(globals.currentUniverse)), (resolution[0] / 2 - 20, 20))
    screen.blit(_render_text(str(globals.multiverse[globals.currentUniverse].worldType["name"])),
                (resolution[0] / 2 - 20, 40))
    screen.blit(globals.images[globals.tileDictionary[
        list(globals.tileDictionary)[globals.buildType % len(globals.tileDictionary)]]["spriteId"]], (10, 50))
    screen.blit(_render_text(str(pygame.mouse.get_pos())), (10, 40))

def _update_objects(universe):
    universe.objectMap = {}
    aliveActors = []
    for actor in universe.actors.values():
        universe.objectMap[actor.pos] = actor
        if actor.alive:
            aliveActors.append(actor)
    for object in universe.entities:
        universe.objectMap[object.pos] = object
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
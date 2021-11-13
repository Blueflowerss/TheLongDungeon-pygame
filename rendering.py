import pygame,globals,imageThings,classes
images = imageThings.readSprites((600,600))
def _render_screen(screen,universe):
    def _render_text(text):
        return font.render(text, False, (255, 255, 255))
    renderLayers = [[],[],[],[],[]]
    boardDistancing = globals.boardDistancing
    resolution = screen.get_size()
    # necessary?
    font = pygame.font.SysFont("Ariel", 24)
    screen.fill((80, 80, 80))
    universe = globals.multiverse[globals.currentUniverse]
    currentActor = globals.playerId
    #check to see if player actor exists, then center the camera around them
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
                renderLayers[3].append((images[object.spriteId], (
                    pos[0] * boardDistancing + cameraOffsetX, pos[1] * boardDistancing + cameraOffsetY)))
    for object in universe.entities:
        if "spriteOffset" in object.flags:
            renderLayers[1].append((images[object.sprite], (
                (object.pos[0] * boardDistancing + cameraOffsetX),
                (object.pos[1] * boardDistancing + cameraOffsetY))))
        else:
            renderLayers[2].append((images[object.sprite], (
                object.pos[0] * boardDistancing + cameraOffsetX,
                object.pos[1] * boardDistancing + cameraOffsetY)))
    for object in universe.actors.values():
        renderLayers[2].append((images[3], (
            object.pos[0] * boardDistancing + cameraOffsetX, object.pos[1] * boardDistancing + cameraOffsetY)))
    for action in range(0, len(globals.actionLog)):
        renderLayers[0].append(((_render_text(globals.actionLog[action])), (0, 80 + 20 * action)))

    renderLayers[0].append(
        (_render_text(str(list(globals.tileDictionary)[globals.buildType % len(globals.tileDictionary)])),
         (60, 50)))
    renderLayers[0].append((
        _render_text(str(list(globals.entityDictionary)[globals.entityType % len(classes.classFactory.objects.database)].__dict__[
                            "devname"])),(10, 190)))
    renderLayers[0].append((_render_text("earth " + str(globals.currentUniverse)), (resolution[0] / 2 - 20, 20)))
    renderLayers[0].append((globals.images[globals.tileDictionary[
        list(globals.tileDictionary)[globals.buildType % len(globals.tileDictionary)]]["spriteId"]], (10, 50)))
    #Debug info
    if globals.debugInfo:
        if currentActor in universe.actors:
            renderLayers[0].append((_render_text(str(universe.actors[currentActor].pos)), (25, 5)))
            renderLayers[0].append((_render_text(str((int(universe.actors[currentActor].pos[0] / globals.chunkSize),
                                          int(universe.actors[currentActor].pos[1] / globals.chunkSize)))),
                        (25, 25)))
        else:
            renderLayers[0].append((_render_text("Actor not!"), (25, 5)))
        renderLayers[0].append((_render_text(str(globals.multiverse[globals.currentUniverse].worldType["name"])),
                    (resolution[0] / 2 - 20, 40)))

        renderLayers[0].append((_render_text(str(pygame.mouse.get_pos())), (10, 40)))
    renderLayers.reverse()
    for layer in renderLayers:
        for image in layer:
            screen.blit(image[0],image[1])

import pygame,GUI,globals
interactions = {"door": "openDoor","sign":"readSign"}
def interaction(interactionName,entity):
    def openDoor():
        if entity.state == False:
            entity.state = True
            entity.sprite = entity.spriteTrue
            try:
                entity.flags.remove("blocks")
            except:
                pass
        else:
            entity.state = False
            entity.sprite = entity.spriteFalse
            entity.flags.append("blocks")
    def readSign():
        globals.director.GUI["signMenu"] = GUI.signMenu(globals.director.manager, entity)

    if interactionName in interactions:
        func = interactions[interactionName]
        eval(func+"()")
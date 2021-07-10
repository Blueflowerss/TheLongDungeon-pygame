import pygame,pygame_gui,globals,functions,worlds,mathstuff
def inputHandler(director,userEvent):
    if userEvent.user_type == pygame_gui.UI_BUTTON_PRESSED:
        if userEvent.ui_object_id == "#teleportMenu.#Confirm":
            if mathstuff.is_number(director.GUI["teleport"].X.get_text()) and mathstuff.is_number(director.GUI["teleport"].Y.get_text()) \
                    and mathstuff.is_number(director.GUI["teleport"].stepWorld.get_text()):
                X = int(director.GUI["teleport"].X.get_text())
                Y = int(director.GUI["teleport"].Y.get_text())
                step = int(director.GUI["teleport"].stepWorld.get_text())
                globals.multiverse[globals.currentUniverse].actors[globals.playerId].pos = (X,Y)
                if step != globals.currentUniverse:
                    functions.attemptTravel(globals.multiverse[globals.currentUniverse].actors[globals.playerId],
                                            globals.currentUniverse, step,True)
                    worlds._update(globals.multiverse[step])

class teleportMenu:
    def __init__(self,manager):
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50, 50, 250, 250), manager,"Be teleport Anywhere!",object_id="#teleportMenu")
        self.X = pygame_gui.elements.UITextEntryLine(pygame.Rect(0,35,55,30), manager, container=self.container,object_id="#Xinput")
        self.Y = pygame_gui.elements.UITextEntryLine(pygame.Rect(55,35, 55, 30), manager, container=self.container,object_id="#Yinput")
        self.stepWorld = pygame_gui.elements.UITextEntryLine(pygame.Rect(0, 90, 55, 30), manager, container=self.container,
                                                     object_id="#stepInput")
        if globals.playerId in globals.multiverse[globals.currentUniverse].actors:
            universe = globals.multiverse[globals.currentUniverse]
            self.X.set_text(str(universe.actors[globals.playerId].pos[0]))
            self.Y.set_text(str(universe.actors[globals.playerId].pos[1]))
            self.stepWorld.set_text(str(globals.currentUniverse))
        self.Confirm = pygame_gui.elements.UIButton(pygame.Rect(25,60,60,30),"Confirm",manager,container=self.container,object_id="#Confirm")

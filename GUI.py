import pygame,pygame_gui,globals,functions,worlds,mathstuff,scenes
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
        elif userEvent.ui_object_id == "#mainMenu.#start":
            director.manager.clear_and_reset()
            director.change_scene(scenes.playScene)
        elif userEvent.ui_object_id == "#mainMenu.#quit":
            globals.save_and_quit()
            director.quit_flag = True

class teleportMenu:
    def __init__(self,manager):
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50, 50, 250, 250), manager,"Be teleport Anywhere!",object_id="#teleportMenu")
        self.X = pygame_gui.elements.UITextEntryLine(pygame.Rect(0,35,55,30), manager, container=self.container,object_id="#Xinput")
        self.X.set_allowed_characters("numbers")
        self.Y = pygame_gui.elements.UITextEntryLine(pygame.Rect(55,35, 55, 30), manager, container=self.container,object_id="#Yinput")
        self.Y.set_allowed_characters("numbers")
        self.stepWorld = pygame_gui.elements.UITextEntryLine(pygame.Rect(0, 90, 55, 30), manager, container=self.container,
                                                     object_id="#stepInput")
        if globals.playerId in globals.multiverse[globals.currentUniverse].actors:
            universe = globals.multiverse[globals.currentUniverse]
            self.X.set_text(str(universe.actors[globals.playerId].pos[0]))
            self.Y.set_text(str(universe.actors[globals.playerId].pos[1]))
            self.stepWorld.set_text(str(globals.currentUniverse))
        self.Confirm = pygame_gui.elements.UIButton(pygame.Rect(25,60,60,30),"Confirm",manager,container=self.container,object_id="#Confirm")
class mainMenu:
    def __init__(self,manager):
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50, 50, 250, 250), manager, "This is the main menu, stop laughing.",
                                                      object_id="#mainMenu")
        print(self.container.rect)
        self.start = pygame_gui.elements.UIButton(pygame.Rect(self.container.rect[2]/3,self.container.rect[3]/3,60,30),
                                                  "Start",manager,container=self.container,object_id="#start",)
        self.quit = pygame_gui.elements.UIButton(pygame.Rect(self.container.rect[2]/3,(self.container.rect[3]/3)+30, 60, 30), "Exit", manager,
                                                  container=self.container, object_id="#quit")
        self.container.close_window_button.disable()
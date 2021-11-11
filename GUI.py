import pygame,pygame_gui,globals,functions,worlds,mathstuff,scenes,interactions
def inputHandler(director,userEvent):
    #print(userEvent)
    if userEvent.user_type == pygame_gui.UI_BUTTON_PRESSED:
        globals.keyLocked = False
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
        elif userEvent.ui_object_id == "#signMenu.#Confirm":
            globals.keyLocked = False
            menu = director.GUI["signMenu"]
            menu.entity.text = menu.textEntry.text
            globals.markForSaving(globals.currentUniverse)
        elif userEvent.ui_object_id == "#mainMenu.#start":
            director.manager.clear_and_reset()
            director.change_scene(scenes.playScene)
        elif userEvent.ui_object_id == "#mainMenu.#quit":
            globals.save_and_quit()
            director.quit_flag = True
    elif userEvent.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
        globals.keyLocked = True
    elif userEvent.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
        globals.keyLocked = False
    elif userEvent.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
        if userEvent.ui_object_id == "#menuinteract.#selectionList":
            entity = director.GUI["interact"].items[int(userEvent.text[0])]
            functions.interactWithEntity(entity)
            director.GUI["interact"].container.kill()
class teleportMenu:
    def __init__(self,manager):
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50, 50, 250, 250), manager,"Become anywhere!",object_id="#teleportMenu")
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
class signMenu:
    def __init__(self,manager,entity):
        self.entity = entity
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50,50,500,120 ), manager,"Sign",object_id="#signMenu")
        self.textEntry = pygame_gui.elements.UITextEntryLine(pygame.Rect(0,0,460,30), manager, container=self.container,object_id="#input")
        self.textEntry.set_text(entity.text)
        self.Confirm = pygame_gui.elements.UIButton(pygame.Rect(220,30,60,30),"Write",manager,container=self.container,object_id="#Confirm")
class mainMenu:
    def __init__(self,manager):
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50, 50, 250, 250), manager, "This is the main menu, stop laughing.",
                                                      object_id="#mainMenu")
        self.start = pygame_gui.elements.UIButton(pygame.Rect(self.container.rect[2]/3,self.container.rect[3]/3,60,30),
                                                  "Start",manager,container=self.container,object_id="#start",)
        self.quit = pygame_gui.elements.UIButton(pygame.Rect(self.container.rect[2]/3,(self.container.rect[3]/3)+30, 60, 30), "Exit", manager,
                                                  container=self.container, object_id="#quit")
        self.container.close_window_button.disable()
class interactionMenu:
    def __init__(self,manager):
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50,50,250,250),manager, "What do you wish to do?",
                                                      object_id="#interactMenu")
class itemList:
    def __init__(self,manager,listOfItems,menu_id):
        #menu_id allows genetic selection menus
        stringItemList = []
        self.items = listOfItems
        index = 0
        for item in listOfItems:
            stringItemList.append(str(index)+" - "+item.displayname)
            index += 1
        self.container = pygame_gui.elements.UIWindow(pygame.Rect(50,50,250,250),manager, "Objects",
                                                      object_id="#menu"+menu_id)
        self.container.set_dimensions((250,15+30*len(stringItemList)))
        self.selection_list = pygame_gui.elements.UISelectionList(pygame.Rect(0,0,150,25*len(stringItemList)),stringItemList,
                                                                  manager,container=self.container,object_id="#selectionList")

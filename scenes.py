import pygame,pygame_gui,sys,globals,os,pickle,functions,classes,imageThings,input,worlds,GUI,rendering
clock = pygame.time.Clock()
class Director:
    def __init__(self):
        self.screen = globals.screen
        pygame.display.set_caption("The Long Dungeon")
        self.scene = None
        self.resolution = globals.resolution
        self.manager = pygame_gui.UIManager(self.resolution)
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.GUI = {}
    def loop(self):
        while not self.quit_flag:
            time = self.clock.tick(40)
            # Exit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
                elif event.type == pygame.VIDEORESIZE:
                    self.resolution = event.size
                    self.manager = pygame_gui.UIManager((self.screen.get_size()))
                    self.scene.__init__(self.scene,self)
                self.scene.on_event(self,event)
            self.scene.on_update(self)
            self.scene.on_draw(self,screen=self.screen)
            pygame.display.flip()
    def change_scene(self, scene):
        self.scene = scene
        self.scene.__init__(self.scene,self)
    def quit(self):
        self.quit_flag = True
class Scene:
    def __init__(self, director):
        self.director = director
    def on_update(self):
        raise NotImplementedError("on_update abstract method must be defined in subclass.")
    def on_event(self, event):
        raise NotImplementedError("on_event abstract method must be defined in subclass.")
    def on_draw(self, screen):
        raise NotImplementedError("on_draw abstract method must be defined in subclass.")
#scenes and shit
class playScene:
    def __init__(self,director):
        Scene.__init__(self,director)
    def on_update(self):
        time_delta = clock.tick(60) / 1000.0
        self.manager.update(time_delta)

    def on_event(self,event):
        if event.type == pygame.KEYDOWN:
            input.keyHandler(self.scene,event)
        elif event.type == pygame.USEREVENT:
            #hacky, like this whole project, re-render the screen when GUI is altered
            GUI.inputHandler(self,event)
            #for some reason GUI disables key repeat
            pygame.key.set_repeat(300,50)
        self.manager.process_events(event)

    def on_draw(self,screen):
        rendering._render_screen(self.screen, globals.currentUniverse)
        self.manager.draw_ui(self.screen)


class menuScene:
    def __init__(self,director):
        Scene.__init__(self,director)
        director.GUI["main"] = GUI.mainMenu(director.manager)
    def on_update(self):
        time_delta = clock.tick(60) / 1000.0
        self.manager.update(time_delta)
    def on_event(self,event):
        if event.type == pygame.QUIT:
            self.quit_flag = True
        elif event.type == pygame.USEREVENT:
            GUI.inputHandler(self,event)
        self.manager.process_events(event)
    def on_draw(self,screen):
        screen.fill((80, 80, 80))
        self.manager.draw_ui(self.screen)

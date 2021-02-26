import pygame
clock = pygame.time.Clock()
class Tile:
    def __init__(self,x,y):
        self.type = "wall"
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
class Universe:
    def __init__(self,index):
        self.index = index
        self.objects = []
        self.items = []
        self.board = {}
        self.objectMap = {}
class Actor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.type = "enemy"
        self.image = pygame.Surface((50,50))
        self.x = y
        self.y = y

    def _process(self):
        pass
class Enemy:
    def __init__(self,x,y):
        self.type = "enemy"
        self.x = y
        self.y = y
        self.width = 20
        self.height= 20
    def _process(self):
        pass
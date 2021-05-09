import pygame_gui
import pygame

clock = pygame.time.Clock()
pygame.init()
pygame.font.init()

font = pygame.font.SysFont("Ariel",24)
resolution = (600,600)
screen = pygame.display.set_mode(resolution,pygame.RESIZABLE)
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))
manager = pygame_gui.UIManager((800,800))
button_layout_rect = pygame.Rect(30, 20, 100, 20)
buttons = {}

container = pygame_gui.elements.UIWindow(pygame.Rect(50,50,250,250),manager,"ass")
textValue = pygame_gui.elements.UITextEntryLine(pygame.Rect(0,0,20,20),manager,parent_element=container)
increaseValue = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 40), (100, 20)),
                                            text='Increase',
                                            manager=manager,container=container)
decreaseValue = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                            text='Decrease',
                                            manager=manager,container=container)
someInventory = [{"name":"sword","price":50},{"name":"potato","price":"20"},{"name":"important shit","price":"20"},{"name":"good potion","price":"20"}]

slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(0,50,300,20),0,(-100,-2100),manager)
value = 0
class Inventory:
    def __init__(self,x,y,height,width):
        global someInventory
        tempInventory = []
        index = 0
        for item in someInventory:
            tempInventory.append((item["name"]+" "+str(item["price"]),str(index)))
            index += 1
        inventoryContainer = pygame_gui.elements.UIWindow(pygame.Rect(x, y, height, width), manager)
        self.inventory = pygame_gui.elements.UISelectionList(pygame.Rect(0,0,height/2,width/2),tempInventory,manager,container=inventoryContainer)
window = Inventory(20,20,300,300)
def _render_text(text):
    return font.render(text,False,(255,255,255))
def buttonManager(event):
    def increase():
        global value
        value += 1
    def decrease():
        global value
        value -= 1
    buttons = {increaseValue:increase,decreaseValue:decrease}
    if event.ui_element in buttons:
        buttons[event.ui_element]()
def windowManager(event):
    def button():
        buttonManager(event)
    def textEntryFinish():
        if event.ui_element == textValue:
            print(textValue.text)
    def sliderMoved():
        if event.ui_element == slider:
            global value
            value = slider.get_current_value()
    def selectedNew():
        if event.ui_element == window.inventory:
            item = someInventory[window.inventory.get_single_selection()]
    keys = {pygame_gui.UI_BUTTON_PRESSED:button,pygame_gui.UI_TEXT_ENTRY_FINISHED:textEntryFinish,pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:sliderMoved,
            pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:selectedNew}
    print(event.ui_element)
    if event.user_type in keys:
        keys[event.user_type]()
while True:
    time_delta = clock.tick(60) / 1000.0
    screen.blit(background, (0, 0))
    screen.blit(_render_text(str(value)), (25, 5))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.USEREVENT:
            windowManager(event)
        manager.process_events(event)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.update()

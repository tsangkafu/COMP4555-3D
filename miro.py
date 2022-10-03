######################################################

import os, sys, random, re

INSTALL_ATTEMPTS = 0
while 1==1:
    try:
        import pygame, pygame_menu
        from screeninfo import get_monitors
        break
    except:
        if INSTALL_ATTEMPTS == 1: input("*** Failure installing missing dependencies.\nPress ENTER to close application."); quit()
        INSTALL_ATTEMPTS += 1
        os.system('python -m pip install pygame')
        os.system('python -m pip install pygame_menu')
        os.system('python -m pip install screeninfo')

#######################################################
# GLOBALS

WINDOW = None # this holds the obj for the game window
MENU = None # this holds the menu

# this holds things like the ball model etc. MODELS["ball"]:
MODELS = {} # ex. MODELS["ball"] = {"pygame":"the pygame object", "shape": "ecliplse", xSpeed:4, ySpeed:5}

#------------------------------------------------------
# COLORS

LIGHT_GRAY_COLOR = (200, 200, 200)

#######################################################
# INITIALIZE

def run():
    pygame.init()
    load_window()
    load_menu()
    display_menu()
 
#------------------------------------------------------

# this also launches the game window
def load_window():
    global WINDOW

    for monitorObj in get_monitors():
        if not monitorObj.is_primary: continue
        x = monitorObj.width
        y = monitorObj.height
        break

    WINDOW = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    pygame.display.set_caption('Pong - Group 3')

#------------------------------------------------------

# https://pygame-menu.readthedocs.io/en/4.2.8/
def load_menu():
    global MENU
    
    # loads the menu and sets the layout
    windowX, windowY = get_window_dimensions()
    MENU = pygame_menu.Menu('SELECT MODE', windowX, windowY, theme=pygame_menu.themes.THEME_DARK)
    # add options
    modeFuncNamesArr = get_mode_function_names()
    for modeFuncName in modeFuncNamesArr:
        MENU.add.button(prettify_mode_function_name(modeFuncName), globals()[modeFuncName]) # globals()[funcName] allows to pass the function as string
    # quit button
    MENU.add.button('Quit', pygame_menu.events.EXIT)

def prettify_mode_function_name(funcName): return funcName.replace("mode_", "").replace("_", " ").title()

def get_mode_function_names():
    l = []
    for key, value in globals().items():
        if callable(value) and value.__module__ == __name__ and key.startswith("mode_"):
            l.append(key)
    return l

#------------------------------------------------------

def display_menu():
    MENU.mainloop(WINDOW)

#######################################################
# MODES
# to create a model: pygame.Rect(xCoord, yCoord, xSize, ySize)

def mode_standard():
    MODELS["ball"] = {"pygame":generate_pygame_model("middle", "middle", 30, 30), "shape":"ellipse", "xSpeed":7, "ySpeed":7}
    MODELS["player"] = {"pygame":generate_pygame_model("right", "middle", 10, 140), "shape":"rect", "xSpeed":0, "ySpeed":6}
    MODELS["opponent"] = {"pygame":generate_pygame_model("left", "middle", 10, 140), "shape":"rect", "xSpeed":7, "ySpeed":7}
    MODELS["line"] = {"pygame":generate_pygame_model("middle", "middle", 3, get_window_dimensions()[1]), "shape":"rect", "xSpeed":0, "ySpeed":0}
    play_game()

#------------------------------------------------------

# the x and y coordiantes can either be a number or a word: left, right, middle, random
def generate_pygame_model(xCoord, yCoord, xSize, ySize):
    # first conver coordinates from words to numbers if they are
    coordsArr = [xCoord, yCoord]
    sizesArr = [xSize, ySize]
    for i in range(len(coordsArr)):
        if not re.match(r"^(left|right|middle|random)$", coordsArr[i]): continue
        coordText = coordsArr[i]
        modelSizeInDirection = sizesArr[i]
        windowSizeInDirection = get_window_dimensions()[i]
        if coordText == "middle": coordsArr[i] = (windowSizeInDirection/2)-(modelSizeInDirection/2)
        elif coordText == "left": coordsArr[i] = modelSizeInDirection
        elif coordText == "right": coordsArr[i] = windowSizeInDirection-modelSizeInDirection
        elif coordText == "random": coordsArr[i] = random.randint(modelSizeInDirection, windowSizeInDirection-modelSizeInDirection) # min, max
    xCoord, yCoord = coordsArr

    # then return the object
    return pygame.Rect(xCoord, yCoord, xSize, ySize)

#######################################################
# PLAYING THE GAME

def play_game():
    clock = pygame.time.Clock()
    display_models()
    while 1==1: # game loop
        for event in pygame.event.get():
            result = event_processor(event)
            if result == "update": display_models()
            elif result == "end game": return

#------------------------------------------------------

# screen top, left edge = 0
def event_processor(event):
    if hasattr(event, "key"):
        if event.key == pygame.K_UP:
            move_model("player", "-")
            return "update"
        elif event.key == pygame.K_DOWN:
            move_model("player", "+")
            return "update"
        elif event.key == pygame.K_ESCAPE:
            return "end game"
    return "nothing important"

def move_model(modelKey, plusOrMinus):
    global MODELS
    times = 1 if plusOrMinus == "+" else -1
    MODELS[modelKey]["pygame"].x += times * MODELS[modelKey]["xSpeed"]
    MODELS[modelKey]["pygame"].y += times * MODELS[modelKey]["ySpeed"]

#------------------------------------------------------

def display_models():
    WINDOW.fill(pygame.Color('grey12'))
    for modelKey in MODELS:
        shape = MODELS[modelKey]["shape"]
        if shape == "ellipse": pygame.draw.ellipse(WINDOW, LIGHT_GRAY_COLOR, MODELS[modelKey]["pygame"])
        elif shape == "rect": pygame.draw.rect(WINDOW, LIGHT_GRAY_COLOR, MODELS[modelKey]["pygame"])
    pygame.display.flip() # this updates the display

#######################################################
# OTHER

def get_window_dimensions():
    return pygame.display.get_surface().get_size() # returns (x,y)

#######################################################

run()
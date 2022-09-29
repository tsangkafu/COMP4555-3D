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
MODELS = {} # this holds things like the ball model etc. <> BALL:

#######################################################
# INITIALIZE

def run():
    pygame.init()
    load_window()
    load_menu()
    while 1==1: display_menu()
 
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

#######################################################
# MODES

def mode_standard():
    global MODELS
    print("hello")
    MODELS["ball"] = {"shape":"ellipse", "size":[30,30], "initCoords":["middle","middle"], "speed":[7,7]}
    MODELS["player"] = {"shape":"rect", "size":[10,140], "initCoords":["right","middle"], "speed":[0,7]}
    MODELS["opponent"] = {"shape":"rect", "size":[10,140], "initCoords":["left","middle"], "speed":[0,7]}
    play_game()

#######################################################
# PLAYING THE GAME

def play_game():
    convert_models_to_pygame_compatible()
    # game loop
    # if input = some button go back to main menu (just stop this function with return)

#------------------------------------------------------

# the "models" created in the modes_ functions are simply to make it easier on the developer
# this function converts them to the actual objects they need to be for the pygame
# the originals can still be accessd in MODELS[blag_orig], so you will still have access to size speed shape etc
def convert_models_to_pygame_compatible():
    global MODELS

    for modelKey in list(MODELS):
        # first convert initial coordinates text to numbers
        for i in range(2): # one for x, one for y
            coordText = MODELS[modelKey]["initCoords"][i]
            if not re.match(r"^(middle|left|right|random)$", coordText): break
            modelSizeInDirection = MODELS[modelKey]["size"][i]
            windowSizeInDirection = get_window_dimensions()[i]

            if coordText == "middle": MODELS[modelKey]["initCoords"][i] = (windowSizeInDirection/2)-(modelSizeInDirection/2)
            elif coordText == "left": MODELS[modelKey]["initCoords"][i] = modelSizeInDirection
            elif coordText == "right": MODELS[modelKey]["initCoords"][i] = windowSizeInDirection-modelSizeInDirection
            elif coordText == "random": MODELS[modelKey]["initCoords"][i] = random.randint(modelSizeInDirection, windowSizeInDirection-modelSizeInDirection) # min, max

        # then convert to pygame compatible
        MODELS[f"{modelKey}_orig"] = MODELS[modelKey] # so you still have access to size speed shape etc.
        xCoord, yCoord = MODELS[modelKey]["initCoords"]
        xSize, ySize = MODELS[modelKey]["size"]
        MODELS[modelKey] = pygame.Rect(xCoord, yCoord, xSize, ySize)

#######################################################
# OTHER

def get_window_dimensions():
    return pygame.display.get_surface().get_size() # returns (x,y)

def display_menu():
    MENU.mainloop(WINDOW)

#######################################################

run()
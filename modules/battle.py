import pyautogui as pg
from src.utils.image import locateImage, locateAllImage
from functools import lru_cache

folder_path_container = 'img/container/'
folder_path = 'img/icons/'

@lru_cache(maxsize=None)
def getBattleIcon():
    battleIconPosition = locateImage(folder_path + 'battle')
    if battleIconPosition is None:
        return None
    return battleIconPosition

@lru_cache(maxsize=None)
def getBattleContainer():
    battleIconPosition = getBattleIcon()
    if battleIconPosition is None:
        return None
    
    bottomContainerPositions = locateAllImage(folder_path_container + 'closeButton')
    if bottomContainerPositions is None:
        return None
        
    for pos in bottomContainerPositions:
        if battleIconPosition.top < pos.top:
            bottomContainerPosition = pos
            break

    return (int(battleIconPosition.left + 21), int(battleIconPosition.top + 12), int(132), int(bottomContainerPosition.top - battleIconPosition.top))

@lru_cache(maxsize=None)
def getContainerSlots(container):
    return container[3] // 22

def getMonsters() -> int:
    battleContainer = getBattleContainer()
    if battleContainer is None:
        return None

    monsters = 0
    possibleMonsters = getContainerSlots(battleContainer)

    for index in range(possibleMonsters):
        y = 22 * index + 15
        if pg.pixelMatchesColor(battleContainer[0], battleContainer[1] + y, (0, 0, 0)):
            monsters += 1
        else:
            return monsters
        
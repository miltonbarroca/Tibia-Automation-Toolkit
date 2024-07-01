from src.utils.image import locateImage
import os
from functools import lru_cache
import pyautogui as pg
from conf import Constants

folder_path = 'img/status/'

@lru_cache(maxsize=None)
def getHpIcon():
    hpIconPosition = locateImage(folder_path + 'heart', center=True)
    if hpIconPosition is None:
        return 
    return hpIconPosition

def getHpBar(icon):
    return int(icon.x + 10), int(icon.y)

def getBarPercentage(bar, colors):
    barSize = Constants.BarSize
    low, high = 0, barSize - 1

    if pg.pixelMatchesColor(bar[0] + barSize - 3, bar[1], colors):
        return 100
    
    while low < high:
        mid = (low + high) // 2
        if pg.pixelMatchesColor(bar[0] + mid, bar[1], colors):
            low = mid + 1
        else:
            high = mid

    if low == 0 and not pg.pixelMatchesColor(bar[0], bar[1], colors):
        return 0
    else:
        return (low * 100) // barSize

def getHpPercentage():
    hpIcon = getHpIcon()
    if hpIcon is None:
        return None
    
    bar = getHpBar(hpIcon)
    return getBarPercentage(bar, Constants.LifeColor)

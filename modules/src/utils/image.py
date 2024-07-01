import pyautogui as pg

def locateImage(image: str, grayscale: bool = True, confidence: float = 0.85, center: bool = False):
    if not image.endswith('.png'):
        image += '.png'
    screenshot = pg.screenshot()
    if not center:
       return pg.locate(image, screenshot, grayscale=grayscale, confidence=confidence)
    else:
        return pg.center(pg.locate(image, screenshot, grayscale=grayscale, confidence=confidence))
    
def locateAllImage(image: str, grayscale: bool = True, confidence: float = 0.85, center: bool = False):
    if not image.endswith('.png'):
        image += '.png'
    screenshot = pg.screenshot()
    return list(pg.locateAll(image, screenshot, grayscale=grayscale, confidence=confidence))
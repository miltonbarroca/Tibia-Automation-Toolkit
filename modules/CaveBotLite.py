import pyautogui as pg
import time
import actions
from threading import Thread
import json
from conf import Constants
import CheckStatus
import keyboard

'''
USE ESSE MODULO PARA HUNTS MAIS SIMPLES COMO STONEREFINER OU ITENS DE IMBUI
'''


def main():

    while True:
        with open(f'scripts/{Constants.SCRIPT_NAME}.json', 'r') as file:
            data = json.loads(file.read())
            while True:
                if actions.check_battle():
                    pg.press('space')
                    time.sleep(9)
                    actions.get_loot()
                    break
                else:
                    for item in data:
                        actions.next_box(item['path'], item['wait'])
                        if actions.check_battle():
                            pg.press('space')
                            time.sleep(12)
                            actions.get_loot()
                            break


if __name__ == "__main__":
    keyboard.wait('h')
    main()

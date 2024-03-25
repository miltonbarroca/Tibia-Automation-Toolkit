import pyautogui as pg
import time
import threading
import time
import random
import json
import my_thread
import CheckStatus
import actions
import AutoEquip
from conf import Constants
from pynput import keyboard
from pynput.keyboard import Listener

def kill_box():
    while actions.check_battle():
        print('matando box...')
        if event_th.is_set():
            return
        pg.press('9')
        if not actions.check_battle() or event_th.is_set():
            return
        time.sleep(random.uniform(2, 2.5))
        pg.press('space')
        pg.press('8')
        if not actions.check_battle() or event_th.is_set():
            return
        time.sleep(random.uniform(2, 2.5))
        pg.press('9')
        if not actions.check_battle() or event_th.is_set():
            return
        time.sleep(random.uniform(2, 2.5))
        pg.press('0')
        pg.press('space')
        if not actions.check_battle() or event_th.is_set():
            return
        time.sleep(random.uniform(2, 2.5))
def check_player():
    try:
        pg.locateOnScreen('img/player.png', confidence=0.9, region=Constants.MINIMAP)
        print('player encontrado')
        return False 
    except pg.ImageNotFoundException:
        return True

def run():
    try:
        event_th.is_set()
        with open(f'modules/{Constants.FOLDER_NAME}/infos.json', 'r') as file:
            data = json.loads(file.read())
        
        while not event_th.is_set():
            for item in data:
                try:
                    if event_th.is_set():
                        return
                    while actions.check_battle():
                        pg.press('4')
                        kill_box()
                        if event_th.is_set():
                            return
                        pg.sleep(1)
                        actions.get_loot()
                        if event_th.is_set():
                            return
                        AutoEquip.check_ring()
                        pg.sleep(1)
                        AutoEquip.check_amulet()
                        pg.sleep(1)
                    actions.next_box(item['path'], item['wait'])
                    pg.sleep(1)         
                    if actions.check_player():
                        pg.press('4')
                        kill_box()
                        if event_th.is_set():
                            return
                        pg.sleep(1)
                        actions.get_loot()
                        if event_th.is_set():
                            return
                        AutoEquip.check_ring()
                        pg.sleep(1)
                        AutoEquip.check_amulet()
                    actions.hole_down(item['down_hole'])
                    pg.sleep(1)
                    if event_th.is_set():
                        return
                    actions.hole_up(item['up_hole'],'modules/GT_alt/anchor_GT_alt_up.png',270,130)
                    pg.sleep(1)
                    if event_th.is_set():
                        return
                except Exception as e:
                    print(f"Erro durante a execução: {e}")
                    
    except Exception as e:
        print(f"Erro durante a execução geral: {e}")

def key_code(key,th_group):
    if key == keyboard.Key.esc:
        event_th.set()
        th_group.stop()
        return False
    if key == keyboard.Key.delete:
        th_group.start()
        th_run.start()

global event_th
event_th = threading.Event()
th_run = threading.Thread(target=run)

th_check_mana = my_thread.MyThread(lambda: CheckStatus.check_status('mana',2.1, *Constants.PIXEL_MANA, Constants.COR_MANA, '3'))
th_check_life = my_thread.MyThread(lambda : CheckStatus.check_status('life',1,*Constants.PIXEL_LIFE,Constants.COR_LIFE,'1'))
th_check_exura = my_thread.MyThread(lambda : CheckStatus.check_status('exura',1.9,*Constants.PIXEL_EXURA,Constants.COR_EXURA,'2'))

group_threads = my_thread.ThreadGroup([th_check_mana,th_check_life,th_check_exura])

with Listener(on_press=lambda key: key_code(key, group_threads)) as listener :
    listener.join()

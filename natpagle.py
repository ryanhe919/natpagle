import sys
import platform
import os
import time
import pyautogui
from packages import utils
from packages import image_process
from packages import audio
from packages import deep_learning

if 'Darwin' in platform.platform():
    PROCESS_NAME = 'World of Warcraft'
elif 'Windows' in platform.platform():
    PROCESS_NAME = 'Wow.exe'
else:
    PROCESS_NAME = 'Wow.exe'
    print("未知操作系统，程序可能无法正常运行!!!")

IMAGE_ADDR = './images'
FLOAT_NAME = 'float.png'
SESSION_NAME = 'session.png'
FLOAT_ADDR = os.path.join(IMAGE_ADDR, FLOAT_NAME)
SESSION_ADDR = os.path.join(IMAGE_ADDR, SESSION_NAME)

SOUND_DEV = 1
SOUND_THRESHOLD = 25000
IMAGE_THRESHOLD = 5


def main():
    if not utils.check_process_exist(PROCESS_NAME):
        sys.exit()
    screen_size = utils.check_screen_size()
    time.sleep(2)
    print('2s后开始钓鱼')
    while True:
        utils.start_fishing()
        time.sleep(2.5)
        start_x, start_y = image_process.make_screenshot(screen_size, 0.25)
        x, y, t_size = image_process.find_float(SESSION_ADDR, FLOAT_ADDR, start_x, start_y)

        # deep_learning.make_train_data(x - start_x, y - start_y)

        float_no = pyautogui.screenshot(region=(x, y, t_size[1], t_size[0]))
        float_no.save(os.path.join(IMAGE_ADDR, 'float_no.png'))

        if image_process.check_hooked(x, y, t_size, THRESHOLD=IMAGE_THRESHOLD):
            utils.move_to(x + t_size[1] // 2, y + t_size[0] // 2)
            utils.click()
        time.sleep(1)


if __name__ == '__main__':
    main()

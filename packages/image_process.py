import pyautogui
import cv2
import time
import os
import numpy as np
import tkinter as tk

IMAGE_ADDR = './images'


def make_screenshot(screen_size, ratio):
    bbox = (ratio * screen_size[0], ratio * screen_size[1],
            (1 - 2 * ratio) * screen_size[0], (1 - 2 * ratio) * screen_size[1])
    img = pyautogui.screenshot(region=bbox)
    img.save('./images/session.png')
    return bbox[0], bbox[1]


def find_float(src, target, start_x, start_y):
    image = cv2.imread(src)
    template = cv2.imread(target)
    t_h, t_w = template.shape[:2]
    result = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # return start_x + min_loc[0] + t_w // 2, start_y + min_loc[1] + t_h // 2, (t_h, t_w)
    return start_x + min_loc[0], start_y + min_loc[1], (t_h, t_w)


def check_hooked(x, y, t_size, text, THRESHOLD):
    theh = 0
    no = cv2.imread('./images/float_no.png').astype(np.int32)
    start_time = time.time()
    count = 0
    sum_var = 0
    while True:
        time.sleep(0.1)
        img = pyautogui.screenshot(region=(x, y, t_size[1], t_size[0]))
        img.save(os.path.join('./images', 'float_yes.png'))
        yes = cv2.imread('./images/float_yes.png').astype(np.int32)
        if count < 5:
            sum_var += np.sum((no.reshape(-1) - yes.reshape(-1)) ** 2)
            count += 1
            continue
        if count == 5:
            theh = sum_var / 5 * THRESHOLD
        if np.sum((no.reshape(-1) - yes.reshape(-1)) ** 2) > theh:
            text.insert(tk.END, '上钩...\n')
            return True
        if time.time() - start_time > 20:
            text.insert(tk.END, '超时未上钩...\n')
            return False

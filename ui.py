import tkinter as tk
from tkinter.filedialog import askopenfilename
import time
import threading as tr
import platform
from packages import utils, image_process
import sys
import pyautogui
import os

FLOAT_ADDR = "./images/float.png"
DEFAULT_THRESHOLD = 5
COUNT_NUM = -1


class Window(object):
    version_num = 1.0

    def __init__(self):
        self.flag = 0
        self.window = tk.Tk()

        self.window.title("钓鱼助手" + " " + "Version: " + str(self.version_num))
        self.window.geometry("500x350")

        self.label_1 = tk.Label(self.window, text="鱼漂路径：", width=20, height=2)
        self.label_2 = tk.Label(self.window, text="阈值：", width=20, height=2)
        self.label_3 = tk.Label(self.window, text="次数：", width=20, height=2)
        self.float_path = tk.StringVar()
        self.threshold = tk.StringVar()
        self.count_num = tk.StringVar()
        self.addr_1 = tk.Entry(self.window, width=50, textvariable=self.float_path)
        self.thresh = tk.Entry(self.window, width=10, textvariable=self.threshold)
        self.count = tk.Entry(self.window, width=10, textvariable=self.count_num)
        self.text = tk.Text(self.window, width=60, height=15)
        self.select = tk.Button(self.window, text="..", width=2, height=1, command=self.select_path)
        self.start = tk.Button(self.window, text="开始", width=10, height=1, command=self.start)
        self.stop = tk.Button(self.window, text="停止", width=10, height=1, command=self.stop)

    def show(self):
        self.label_1.place(x=10, y=10)
        self.label_2.place(x=10, y=50)
        self.label_3.place(x=250, y=50)
        self.float_path.set(value=FLOAT_ADDR)
        self.addr_1.place(x=120, y=18)
        self.threshold.set(value=str(DEFAULT_THRESHOLD))
        self.thresh.place(x=120, y=58)
        self.count_num.set(value=str(COUNT_NUM))
        self.count.place(x=360, y=58)
        self.text.place(x=40, y=90)
        self.select.place(x=430, y=14)
        self.start.place(x=40, y=300)
        self.stop.place(x=385, y=300)

    def select_path(self):
        self.float_path.set(askopenfilename())

    def start(self):
        self.flag = 0
        thread_1 = tr.Thread(target=self.fishing)
        thread_1.start()

    def fishing(self):
        self.text.insert(tk.END, "操作系统： " + platform.platform() + "\n")
        if 'Darwin' in platform.platform():
            process = 'World of Warcraft'
        elif 'Windows' in platform.platform():
            process = 'Wow.exe'
        else:
            process = 'Wow.exe'
            self.text.insert(tk.END, "未知操作系统")
            return

        if not utils.check_process_exist(process, self.text):
            sys.exit()
        screen_size = utils.check_screen_size(self.text)
        self.text.insert(tk.END, '2s后开始钓鱼\n')
        time.sleep(2)
        while int(self.count.get()) != 0:
            if self.flag == 1:
                break
            utils.start_fishing(self.text)
            time.sleep(2.5)
            start_x, start_y = image_process.make_screenshot(screen_size, 0.25)
            x, y, t_size = image_process.find_float("./images/session.png", self.addr_1.get(), start_x, start_y)

            float_no = pyautogui.screenshot(region=(x, y, t_size[1], t_size[0]))
            float_no.save(os.path.join("./images", 'float_no.png'))

            if image_process.check_hooked(x, y, t_size, self.text, THRESHOLD=int(self.thresh.get())):
                utils.move_to(x + t_size[1] // 2, y + t_size[0] // 2)
                utils.click()
            time.sleep(1)
            self.count_num.set(int(self.count.get()) - 1)

    def stop(self):
        self.flag = 1

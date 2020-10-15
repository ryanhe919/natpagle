import psutil
import pyautogui
import tkinter as tk


def check_process_exist(proc_name, text):
    text.insert(tk.END, '正在检查进程' + proc_name + '是否允许...' + "\n")
    for pid in psutil.pids():
        temp = psutil.Process(pid)
        if proc_name == temp.name():
            text.insert(tk.END, proc_name + '正在运行!!!' + "\n")
            return True
    text.insert(tk.END, proc_name + "未运行!!!" + '\n')
    return False


def check_screen_size(text):
    img = pyautogui.screenshot()
    text.insert(tk.END, "已获取屏幕大小：%dx%d\n" % img.size)
    return img.size


def start_fishing(text):
    pyautogui.press('f1')
    text.insert(tk.END, '开始钓鱼\n')


def move_to(x, y):
    pyautogui.moveTo(x, y)


def click():
    pyautogui.click(button='right')

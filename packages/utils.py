import psutil
import pyautogui


def check_process_exist(proc_name):
    print('正在检查进程' + proc_name + '是否允许...')
    for pid in psutil.pids():
        temp = psutil.Process(pid)
        if proc_name == temp.name():
            print(proc_name + '正在运行!!!')
            return True
    print(proc_name + "未运行!!!")
    return False


def check_screen_size():
    img = pyautogui.screenshot()
    print("已获取屏幕大小：%dx%d" % img.size)
    return img.size


def start_fishing():
    pyautogui.press('f1')
    print('开始钓鱼')

def move_to(x, y):
    pyautogui.moveTo(x, y)


def click():
    pyautogui.click(button='right')
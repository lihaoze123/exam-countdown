import datetime
import time

import cv2
import os
import numpy as np
import win32api
import win32con
import win32gui
from PIL import Image, ImageDraw, ImageFont


def setWallpaper(path):
    # 打开注册表
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)

    # 2：拉伸  0：居中  6：适应  10：填充
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 我们选择了拉伸
    # win32api.RegSetValueEx(reg_key,"Wallpaper")
    # SPIF_SENDWININICHANGE:立即生效
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_SENDWININICHANGE)


def get_the_remaining_time(year="2021", month="06", day="25"):
    now = datetime.datetime.now()
    end = datetime.datetime.strptime(
        '{year}-{mon}-{day} 00:00:00'.format(year=year, mon=month, day=day), '%Y-%m-%d %H:%M:%S')
    delta = end - now
    day = delta.days
    hour = int(delta.seconds / (60*60))
    seconds = delta.seconds - (hour * (60 ** 2))
    min = int(seconds / 60)
    seconds = seconds - (min * 60)
    return (day, hour, min, seconds)


def edit_wallpaper(year, month, day, text="中考"):
    bk_img = cv2.imread(os.path.realpath("./images/1.jpg"))
    fontpath = "./font/font.TTF"  # 设置字体
    font = ImageFont.truetype(fontpath, 80)  # 字体大小，当前90
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    # 绘制字体
    day, hour, min, sec = get_the_remaining_time(
        year=year, month=month, day=day)
    draw.text((350, 842), "距离{text}仅剩: {day}天{hour}小时{min}分{sec}秒".format(
        day=day, min=min, sec=sec, hour=hour, text=text), font=font, fill=(255, 255, 255))
    bk_img = np.array(img_pil)
    # 展示图象
    cv2.waitKey()
    cv2.imwrite("./images/result.jpg", bk_img)


def exit():
    print("请编辑config.txt")
    with open("./config.txt", "w", encoding="utf-8") as f:
        f.write('{"text": "", "year": "", "month": "", "day": ""}')
    input("输入q退出: \n")

if os.path.isfile("./config.txt"):
    while True:
        with open("./config.txt", "r", encoding="utf-8") as f:
            index = f.read()
            index = eval(index)
            text = index["text"]
            year = index["year"]
            month = index["month"]
            day = index["day"]
        if index["text"]:
                edit_wallpaper(text=text, year=year, month=month, day=day)
                setWallpaper(
                    os.path.realpath("./images/result.jpg"))
                time.sleep(1)
        else:
            exit()
else:
    exit()

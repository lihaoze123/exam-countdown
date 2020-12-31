'''
Date: 2020-10-03 01:20:37
LastEditors: lihaoze123
LastEditTime: 2020-10-03 10:11:42
'''

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


def get_the_remaining_time(year="2021", month="06", day="25", hour="00", min="00"):
    now = datetime.datetime.now()
    end = datetime.datetime.strptime(
        '{year}-{mon}-{day} {hour}:{min}:00'.format(year=year, mon=month, day=day, hour=hour, min=min), '%Y-%m-%d %H:%M:%S')
    delta = end - now
    day = delta.days
    hour = int(delta.seconds / (60*60))
    seconds = delta.seconds - (hour * (60 ** 2))
    min = int(seconds / 60)
    seconds = seconds - (min * 60)
    return (day, hour, min, seconds)


def edit_wallpaper(year, month, day, min, hour, text, sentence, x, y, file):
    bk_img = cv2.imread(os.path.realpath("./images/"+file))
    fontpath = "./font/font.TTF"  # 设置字体
    fontpath2 = "./font/SIMYOU.TTF"  # 设置字体
    
    font = ImageFont.truetype(fontpath, 50)
    font2 = ImageFont.truetype(fontpath2, 150)  # 字体大小
    
    color=(0, 0, 0)
    
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    # 绘制字体
    day, hour, min, sec = get_the_remaining_time(
        year=year, month=month, day=day, min=min, hour=hour)
    draw.text((100, 50), sentence, font=font2, fill=(0, 0, 0))
    draw.text((500, 50), "S H I F T\n\t康龙帅", font=ImageFont.truetype(fontpath2, 100), fill=(0, 0, 0))
    if day>=0:
        draw.text((x, y), "距离{text}仅剩:\n\t\t{day}天\n\t\t{hour}小时\n\t\t{min}分\n\t\t{sec}秒".format(
            day=day, min=min, sec=sec, hour=hour, text=text), font=font, fill=(0, 0, 0))
    else:draw.text((550, 600), text+"考试已结束", font=font, fill=(0, 0, 0))
    bk_img = np.array(img_pil)
    # 展示图象
    cv2.waitKey()
    cv2.imwrite("./images/result.jpg", bk_img)


def exit():
    print("请编辑config.txt")
    with open("./config.txt", "w", encoding="utf-8") as f:
        f.write('{"text": "", "year": "", "month": "", "day": ""}')
    input("输入q退出: \n")

def main(i, x=550, y=600, file='1.png'):
    text = i["text"]
    year = i["year"]
    month = i["month"]
    day = i["day"]
    min = i["min"]
    hour = i["hour"]
    sentence = i["sentence"]
    if i["text"]:
        edit_wallpaper(text=text, sentence=sentence,year=year, month=month, day=day, hour=hour, min=min, x=x, y=y, file=file)
    else:exit()


if os.path.isfile("./config.txt"):
    while True:
        index = eval(open("./config.txt", "r", encoding="utf-8").read())
        for i in index:
            for p in range(2):
                for a in range(3):
                    main(i)
                    if p:main({"text": "中考", "year": "2021", "month": "06", "day": "25", "hour": "00", "min": "00", "sentence": "态 努\n度 力\n决 造\n定 就\n高 实\n度 力"}, x=550, y=300, file='result.jpg')
                    else:main({"text": "一模", "year": "2021", "month": "01", "day": "25", "hour": "00", "min": "00", "sentence": "态 努\n度 力\n决 造\n定 就\n高 实\n度 力"}, x=550, y=300, file='result.jpg')
                    setWallpaper(os.path.realpath("./images/result.jpg"))
                    time.sleep(0.5)
else:
    exit()

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
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
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
    
    font = ImageFont.truetype(fontpath, 80)
    font2 = ImageFont.truetype(fontpath2, 150)  # 字体大小
    
    color=(204, 228, 248)
    
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    # 绘制字体
    day, hour, min, sec = get_the_remaining_time(
        year=year, month=month, day=day, min=min, hour=hour)
    draw.text((800, 100), sentence, font=font2, fill=color)
    if day>=0:
        draw.text((x, y), "距离{text}仅剩:\n\t\t{day}天\n\t\t{hour}小时\n\t\t{min}分\n\t\t{sec}秒".format(
            day=day, min=min, sec=sec, hour=hour, text=text), font=font, fill=color)
    else:draw.text((x, y), text+"考试已结束", font=font, fill=color)
    bk_img = np.array(img_pil)
    # 展示图象
    cv2.waitKey()
    cv2.imwrite("./images/result.jpg", bk_img)

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
        #main(i)
        main({"text": "高考", "year": "2024", "month": "06", "day": "7", "hour": "00", "min": "00", "sentence": "异想天开\n脚踏实地"}, x=800, y=500, file='1.png')
        setWallpaper(os.path.realpath("./images/result.jpg"))
        time.sleep(0.5)

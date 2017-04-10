# -*- encoding: utf-8 -*-
#
# 支持iOS10.0以上版本
# 支持iPhone5，5s,SE系列4寸 / iPhone6,6S,7系列4.7寸 / iPhone6Plus,6SPlus,7Plus系列5.5寸机型

import atx
import sys
import time
imagePathForScript = sys.argv[1]
storePath = sys.argv[2]
port = sys.argv[3]
from iOSMonkey.monkey.ios_monkey import *

#############设置程序是否是调试版本###############
isDebug = True

GT_NORMAL_OUTPUT = 'GT_NORMAL_OUTPUT'
GT_PICTURE_NOT_FOUND = 'GT_PICTURE_NOT_FOUND'

if isDebug:
    imagePathForScript = ""
    storePath = "/Users/casiillas/Desktop/screenshot/"
    port = "8100"


url = "http://127.0.0.1" + ":" + port
bundle_id = "com.netdragon.quicktest"
d = atx.connect(url)
s = d.start_app(bundle_id)


def log_debug(line, debug_state = True):
    if debug_state:
        print line

# 账号登陆
def login():
    delay_exist(1)
    # 检测客户更新
    if not d.exists("play@auto.png") and not d.exists("enter@auto.png"):
        log_debug(GT_NORMAL_OUTPUT + ':' + '更新中...', debug_state=isDebug)
        update = delay_exist(500,"play@auto.png")
        if update == False:
            print GT_PICTURE_NOT_FOUND,':','play@auto.png'
        else:
            log_debug(GT_NORMAL_OUTPUT + ':' + '更新完成', debug_state=isDebug)
    else:
        log_debug(GT_NORMAL_OUTPUT + ':' + '已是最新版', debug_state=isDebug)

    if d.exists("later_bind@auto.png"):
        d.cilck("later_bind@auto.png")
    # 如果用户未登录过
    if d.exists("play@auto.png"):
        d.click_image("play@auto.png")
        d.click_image("permit@auto.png")
        # 安装后第一次登录
        delay_exist(2)
        if d.exists("photo_confirm@auto.png"):
            d.click_image("photo_confirm@auto.png")
            d.click_image("later_bind@auto.png")
            d.click_image("user_confirm@auto.png")
            d.click_image("user_close@auto.png")
        if d.exists("user_confirm@auto.png"):
            d.click_image("user_confirm@auto.png")
        d.click_image("enter@auto.png")
        d.click_image("random@auto.png")
        d.click_image("createplayer@auto.png")
        d.click_image("confirm@auto.png")
        d.click_image("skip@auto.png")
        d.click_image("tip_confirm@auto.png")
    elif d.exists("enter@auto.png"):
        # 如果用户已经登录过
        d.click_image("enter@auto.png")
        if d.exists("random@auto.png"):
            d.click_image("random@auto.png")
            d.click_image("createplayer@auto.png")
            d.click_image("confirm@auto.png")
            delay_exist(2)
            d.click_image("skip@auto.png")
            d.click_image("tip_confirm@auto.png")
        else:
            print GT_PICTURE_NOT_FOUND,':','random@auto.png'
    else:
        print GT_PICTURE_NOT_FOUND,':','play@auto.png'
        print GT_PICTURE_NOT_FOUND,':','enter@auto.png'

#延时检测函数
def delay_exist(mytime,image = None):
    start_time = time.time()
    while time.time() - start_time < mytime:
        if image != None:
            if d.exists(image):
                return True
    return False
# Monkey测试
def monkey():
    mm = Monkey(session=d.session)
    mm.start_monkey(image_store_path= storePath, running_time=1,
                    check_close_wnd=checkwindow, check_close_seconds=5)
# 弹窗检测
def checkwindow():
    if d.exists("close@auto.png"):
        d.click_image("close@auto.png")
    if d.exists("auto_cancel@auto.png"):
        d.click_image("auto_cancel@auto.png")
def main():
    try:
        login()
        monkey()
        d.stop_app(bundle_id)
    except Exception as e:
        str_e = str(e)
main()
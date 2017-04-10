# -*- encoding: utf-8 -*-
#
# 支持iOS10.0以上版本
# 支持iPhone5，5s,SE系列4寸 / iPhone6,6S,7系列4.7寸 / iPhone6Plus,6SPlus,7Plus系列5.5寸机型

import atx
import sys

# imagePathForScript = sys.argv[1]
# storePath = sys.argv[2]
# port = sys.argv[3]
from iOSMonkey.monkey.ios_monkey import *

#############设置程序是否是调试版本###############
isDebug = True

# 定义参数
GT_NORMAL_OUTPUT = 'GT_NORMAL_OUTPUT'
GT_PICTURE_NOT_FOUND = 'GT_PICTURE_NOT_FOUND'
GT_TEST_CASE_FAILED = "GT_TEST_CASE_FAILED"
GT_SYSTEM_EXCEPTION = "GT_SYSTEM_EXCEPTION"
GT_OTHER_EXCEPTION = "GT_OTHER_EXCEPTION"

PLAY = 'play@auto.png'
ENTER = 'enter@auto.png'
LATER_BIND= 'later_bind@auto.png'
PERMIT = 'permit@auto.png'
PHOTO_CONFIRM = 'photo_confirm@auto.png'
USER_CONFIRM = 'user_confirm@auto.png'
USER_CLOSE = 'user_close@auto.png'
RANDOM = 'random@auto.png'
CREATEPLAYER = 'createplayer@auto.png'
CREATE_CONFIRM = 'confirm@auto.png'
SKIP = 'skip@auto.png'
TIP_CONFIRM = 'tip_confirm@auto.png'
CLOSE = 'close@auto.png'
AUTO_CANCEL = 'auto_cancel@auto.png'

if isDebug:
    imagePathForScript = "/Users/casiillas/Desktop/pic/"
    storePath = "/Users/casiillas/Desktop/screenshot/"
    port = "8100"

url = "http://127.0.0.1" + ":" + port
d = atx.connect(url)

def main():

    bundle_id = "com.netdragon.quicktest"
    d.start_app(bundle_id)
    try:
        login()
        monkey()
        d.stop_app(bundle_id)
    except Exception as e:
        print GT_OTHER_EXCEPTION + ":" + e


# Debug信息
def log_debug(line, debug_state = True):
    if debug_state:
        print line

# 账号登陆
def login():
    delay_exist(1)
    # 检测客户更新
    if not d.exists(imagePathForScript + PLAY) and not d.exists(imagePathForScript + ENTER):
        log_debug(GT_NORMAL_OUTPUT + ':' + '更新中...', debug_state=isDebug)
        update = delay_exist(500,imagePathForScript + PLAY)
        if update == False:
            print GT_PICTURE_NOT_FOUND,':',PLAY
        else:
            log_debug(GT_NORMAL_OUTPUT + ':' + '更新完成', debug_state=isDebug)
    else:
        log_debug(GT_NORMAL_OUTPUT + ':' + '已是最新版', debug_state=isDebug)

    if d.exists(imagePathForScript + LATER_BIND):
        d.cilck(imagePathForScript + LATER_BIND)
    # 如果用户未登录过
    if d.exists(imagePathForScript + PLAY):
        d.click_image(imagePathForScript + PLAY)
        d.click_image(imagePathForScript + PERMIT)
        # 安装后第一次登录
        delay_exist(2)
        if d.exists(imagePathForScript + PHOTO_CONFIRM):
            d.click_image(imagePathForScript + PHOTO_CONFIRM)
            d.click_image(imagePathForScript + LATER_BIND)
            d.click_image(imagePathForScript + USER_CONFIRM)
            d.click_image(imagePathForScript + USER_CLOSE)
        if d.exists(imagePathForScript + USER_CONFIRM):
            d.click_image(imagePathForScript + USER_CONFIRM)
        d.click_image(imagePathForScript + ENTER)
        d.click_image(imagePathForScript + RANDOM)
        d.click_image(imagePathForScript + CREATEPLAYER)
        d.click_image(imagePathForScript + CREATE_CONFIRM)
        d.click_image(imagePathForScript + SKIP)
        d.click_image(imagePathForScript + TIP_CONFIRM)
    elif d.exists(imagePathForScript + ENTER):
        # 如果用户已经登录过
        d.click_image(imagePathForScript + ENTER)
    else:
        print GT_PICTURE_NOT_FOUND,':',PLAY
        print GT_PICTURE_NOT_FOUND,':',ENTER

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
    if d.exists(imagePathForScript + CLOSE):
        d.click_image(imagePathForScript + CLOSE)
    if d.exists(imagePathForScript + AUTO_CANCEL):
        d.click_image(imagePathForScript + AUTO_CANCEL)

main()
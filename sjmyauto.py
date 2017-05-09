# -*- encoding: utf-8 -*-
#
# 支持iOS10.0以上版本
# 支持iPhone5，5s,SE系列4寸 / iPhone6,6S,7系列4.7寸 / iPhone6Plus,6SPlus,7Plus系列5.5寸机型
import random
from threading import Thread, Lock
import datetime
import time

from wda import *
import atx
import sys
import traceback



#############设置程序是否是调试版本###############

isDebug = True
# isDebug = False

# 定义参数
GT_NORMAL_OUTPUT = 'GT_NORMAL_OUTPUT'
GT_PICTURE_NOT_FOUND = 'GT_PICTURE_NOT_FOUND'
GT_TEST_CASE_FAILED = "GT_TEST_CASE_FAILED"
GT_SYSTEM_EXCEPTION = "GT_SYSTEM_EXCEPTION"
GT_OTHER_EXCEPTION = "GT_OTHER_EXCEPTION"

PLAY = 'play@auto.png'
ENTER = 'enter@auto.png'
USER_CLOSE = 'user_close@auto.png'
RANDOM = 'random@auto.png'
CREATEPLAYER = 'createplayer@auto.png'
CREATE_CONFIRM = 'confirm@auto.png'
SKIP = 'skip@auto.png'
CLOSE = 'close@auto.png'
TASK = 'task@auto.png'
MAP = 'map@auto.png'
MONSTER = 'findmonster@auto.png'
CHOOSE_MONSTER = 'level_5@auto.png'
AUTO = 'autofight@auto.png'
DIALOG = 'dialog@auto.png'
CLICK_DIALOG = 'click_dialog@auto.png'
SEND = 'send@auto.png'


if isDebug:
    imagePathForScript = "pic/"
    storePath = "/data/screenshot/"
    port = "8100"
else:
	imagePathForScript = sys.argv[1]
	storePath = sys.argv[2]
	port = sys.argv[3]

if imagePathForScript.endswith("/") is False:
    imagePathForScript = imagePathForScript + "/"

url = "http://127.0.0.1" + ":" + port
d = atx.connect(url)


class Test(object):
    def __init__(self):
        self.bundle_id = "com.netdragon.quicktest"
    # 打开App
    def openApp(self):
        d.start_app(self.bundle_id)
    # 关闭App
    def stopAPP(self):
        d.stop_app(self.bundle_id)

    # 用户登录
    def login(self):
        delay(2)
        # 如果第一次登录等待25s否则等待2s
        if d.exists(imagePathForScript + PLAY):
            pass
        else:
            delay(20)

        # 点击试玩
        click_event(PLAY)

        # 延时
        delay(8)

        # 第一次登录需要关闭窗口
        if d.exists(imagePathForScript + USER_CLOSE):
            d.click_image(imagePathForScript + USER_CLOSE)

        # 点击进入游戏
        click_event(ENTER)

        delay(17)
        # 第一次登录客户端需要创建角色
        if d.exists(imagePathForScript + RANDOM):
            self.registerPlayer()

    # 注册角色
    def registerPlayer(self):
        # 点击随机生成Name
        click_event(RANDOM)

        # 点击创建角色
        click_event(CREATEPLAYER)
        delay(2)

        # 点击确定创建
        click_event(CREATE_CONFIRM)
        delay(8)

        # 跳过
        click_event(SKIP)


    # 待机5分钟
    def standby(self):
        delay(10, checkwindow)

    # 野外杀怪5分钟
    def fight(self):

        # 如果是新注册账号第一次登录游戏
        if d.exists(imagePathForScript + TASK):
            # 点击任务
            click_event(TASK)
            d.click(100, 100)
            delay(10)
            d.click(100, 100)

        # 点击地图
        click_event(MAP)

        delay(5)
        # 点击出城打怪
        click_event(MONSTER)

        delay(5)
        # 选择怪物等级
        click_event(CHOOSE_MONSTER)

        delay(30)

        # 关闭地图
        click_event(CLOSE)

        # 自动战斗
        click_event(AUTO)

        # 延时5分钟
        delay(10)

        # 停止自动战斗
        click_event(AUTO)

    # 一直输入文本
    def inputText(self):
        # 点击对话框
        click_event(DIALOG)

        delay(2)

        # 输入数字
        def input_number():
            # 点击输入
            click_event(CLICK_DIALOG)

            delay(2)
            # 输入文本
            d.type("12345")

            # 点击发送
            click_event(SEND)

            delay(2)

        # 输入字母
        def input_letter():
            # 点击输入
            click_event(CLICK_DIALOG)

            delay(2)
            # 输入文本
            d.type("tqqtqq")

            # 点击发送
            click_event(SEND)

            delay(2)

        delay(150, input_number)
        delay(150, input_letter)

# 点击事件
def click_event(event):
    if d.exists(imagePathForScript + event):
        d.click_image(imagePathForScript + event)
    else:
        raise ImageException('GT_PICTURE_NOT_FOUND:%s' % event)


# 弹窗检测
def checkwindow():
    if d.exists(imagePathForScript + CLOSE):
        d.click_image(imagePathForScript + CLOSE)
    delay(5)

# 延时函数
def delay(mytime, myfun = None):
    start_time = time.time()
    while time.time() - start_time < mytime:
        if myfun != None:
            myfun()

# 图片异常捕获
class ImageException(Exception):
    pass


if __name__ == '__main__':
    sjmy = Test()
    sjmy.openApp()
    sjmy.login()
    sjmy.standby()
    sjmy.fight()
    sjmy.inputText()
    sjmy.stopAPP()
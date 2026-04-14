import time
import pyautogui
import random
import pyperclip
pyautogui.FAILSAFE=False
print('你有5s时间切到微信聊聊天框')
time.sleep(5)
news=['你好','现在比较忙，稍后联系哈','测试代码ing']
#a=random.random()#随机0-1小数

while True:

 a=random.choice(news)
 pyperclip.copy(a)
 pyautogui.hotkey('ctrl','v')
 pyautogui.press('enter')
 time.sleep(2)
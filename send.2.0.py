import pytesseract
import pyautogui
import pyperclip
import time
print("您有5s时间打开微信")
time.sleep(5)
key_word={
    '你好':'好好好，大家都好',
    '我要睡觉':'睡什么睡，起来继续干',
    '打瓦不':'gogogo，上号上分上青铜！',
    '打州不': '坝顶狙能不能滚一边去，别恶心人了',
    '打王者不': '唉，又是掉分的一天！',
    '我去吃饭了': '吃吃吃，少吃一顿会饿死你啊',
}
no_keyword='sorry,这几个字识别不了！'
pytesseract.pytesseract.tesseract_cmd = r'E:\pytesseract.2\tesseract.exe'
desigin=(1199,1087,375,52)
time.sleep(5)
def catch():
    try:
        img=pyautogui.screenshot(region=desigin)
        text=pytesseract.image_to_string(img,lang='chi_sim')
        return text.strip()
    except:
        return ""
def match(text):
  for d,w in key_word.items():
    if d in text:
        return w
  return no_keyword

def send(msg):
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl','v')
    time.sleep(0.2)
    pyautogui.press('enter')
last_text=""
while True:
    try:

     current_text = catch()
     if current_text and current_text!=last_text:
        print(f"\n识别到消息：{current_text[:30]}")
        last_text=current_text
        reply_text=match(current_text)
        print(f"\n自动回复消息：{reply_text}")
        send(reply_text)
     time.sleep(3)
    except KeyboardInterrupt:
     print("\n已停止自动回复")
     break
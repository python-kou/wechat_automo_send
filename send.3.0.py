import pyautogui
import pytesseract
import time
import pyperclip
import openai
import os

# ====================== 必改配置区 ======================
# 1. Tesseract OCR 安装路径（必须改成你自己的！）
pytesseract.pytesseract.tesseract_cmd = r'E:\pytesseract.2\tesseract.exe'

# 2. 聊天窗口截图区域 (左, 上, 宽, 高) —— 必须框住聊天消息区域
CHAT_REGION = (522, 1209, 545, 95)

# 3. AI API 配置（以 DeepSeek 为例，换其他服务商只需改下面三行）
AI_API_KEY = "yours_api_key"  # 替换成你的 API Key
AI_BASE_URL = "https://api.deepseek.com"  # API 地址
AI_MODEL = "deepseek-chat"  # 模型名称

# 4. 检测间隔秒数
CHECK_DELAY = 2.0

# 5. 未匹配到 AI 时的降级回复（防止 API 出错时冷场）
FALLBACK_REPLY = "收到消息啦，我稍后回复你~"

# 6. 系统提示词（定义机器人的说话风格）
SYSTEM_PROMPT = """你是一个微信/QQ自动回复助手，帮用户回复朋友的消息。
要求：
1. 回复要自然、口语化，像真人朋友聊天一样
2. 回复不要太长，控制在50字以内
3. 适当使用表情符号（😊😂👍等）
4. 如果不知道如何回复，就礼貌地表示稍后回复
5. 绝对不要透露你是AI或机器人
6.你的人设是三角洲高手，绝密航天随便清图，带朋友爽吃核心区"""
# ======================================================

# 初始化 OpenAI 客户端
client = openai.OpenAI(
    api_key=AI_API_KEY,
    base_url=AI_BASE_URL
)


def get_chat_text():
    """截图并 OCR 识别聊天文字"""
    try:
        img = pyautogui.screenshot(region=CHAT_REGION)
        text = pytesseract.image_to_string(img, lang='chi_sim')
        return text.strip()
    except Exception as e:
        print(f"[OCR 错误] {e}")
        return ""


def send_message(msg):
    """模拟键盘输入并发送消息"""
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')


def ai_reply(message, history=None):
    """调用 AI 生成回复"""
    if history is None:
        history = []

    messages = [
                   {"role": "system", "content": SYSTEM_PROMPT}
               ] + history + [
                   {"role": "user", "content": message}
               ]

    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[API 调用失败] {e}")
        return FALLBACK_REPLY


# ====================== 主程序 ======================
print("=" * 50)
print("AI 自动回复机器人已启动（微信/QQ通用）")
print("按 Ctrl + C 停止程序")
print("=" * 50)

last_text = ""
chat_history = []  # 保存多轮对话上下文
MAX_HISTORY = 6  # 最多保留最近 3 轮对话（一问一答算一轮）

while True:
    try:
        current_text = get_chat_text()

        # 有新消息才处理
        if current_text and current_text != last_text:
            print(f"\n[识别] {current_text[:50]}...")
            last_text = current_text

            # 调用 AI 生成回复
            reply = ai_reply(current_text, chat_history)
            print(f"[回复] {reply}")

            # 更新对话历史（保留最近几轮）
            chat_history.append({"role": "user", "content": current_text})
            chat_history.append({"role": "assistant", "content": reply})
            if len(chat_history) > MAX_HISTORY * 2:
                chat_history = chat_history[-(MAX_HISTORY * 2):]

            # 发送回复
            send_message(reply)

        time.sleep(CHECK_DELAY)

    except KeyboardInterrupt:
        print("\n[停止] 程序已退出")
        break
    except Exception as e:
        print(f"[运行错误] {e}")
        time.sleep(CHECK_DELAY)
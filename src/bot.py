import os
import re
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# โหลด environment variables
load_dotenv()

# สร้าง Slack App
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# =============== Message Handlers ===============

# ตอบกลับเมื่อมีคนพิมพ์ "hello" หรือ "hi"
@app.message(re.compile(r"(hello|hi|สวัสดี)", re.IGNORECASE))
def message_hello(message, say):
    user = message['user']
    say(f"สวัสดีครับคุณ <@{user}>! 👋 ผมคือ BL1NK Bot พร้อมช่วยเหลือคุณแล้ว")

# ตอบกลับเมื่อมีคนพิมพ์ "help"
@app.message(re.compile(r"help", re.IGNORECASE))
def message_help(say):
    help_text = """
🤖 *BL1NK Bot - คำสั่งที่ใช้ได้:*

• `hello` หรือ `hi` - ทักทาย
• `help` - แสดงคำสั่งทั้งหมด
• `ping` - ทดสอบการตอบสนอง
• `@BL1NK Bot` - เมนชั่นเพื่อคุยด้วย
• `info` - ข้อมูล bot

*ความสามารถพิเศษ:*
✅ รองรับ DM (ส่งข้อความส่วนตัวได้)
✅ ทำงานใน channel ทั้ง public และ private
✅ ตอบกลับแบบ real-time ด้วย Socket Mode
    """
    say(help_text)

# ตอบกลับเมื่อมีคนพิมพ์ "ping"
@app.message(re.compile(r"ping", re.IGNORECASE))
def message_ping(say):
    say("🏓 Pong! Bot ทำงานปกติครับ")

# ตอบกลับเมื่อมีคนพิมพ์ "info"
@app.message(re.compile(r"info", re.IGNORECASE))
def message_info(say):
    info_text = """
ℹ️ *BL1NK Bot Information*

📦 *Framework:* Slack Bolt for Python
🔌 *Mode:* Socket Mode (Real-time)
🏗️ *Project:* bl1nk-slack-mcp-server
💻 *Running on:* Termux (Android)

พัฒนาโดย: BL1NK Team
    """
    say(info_text)

# =============== Event Handlers ===============

# ตอบกลับเมื่อมีคนเมนชั่น bot
@app.event("app_mention")
def handle_app_mention(event, say):
    user = event['user']
    text = event.get('text', '')
    
    # ลบ mention ออกจากข้อความ
    clean_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    
    if not clean_text:
        say(f"สวัสดีครับ <@{user}>! มีอะไรให้ผมช่วยไหมครับ? พิมพ์ `help` เพื่อดูคำสั่งทั้งหมด")
    else:
        say(f"ได้รับข้อความจาก <@{user}> แล้วครับ: _{clean_text}_\n\nผมกำลังเรียนรู้ที่จะตอบคำถามได้ดีขึ้น! 🤖")

# =============== Reaction Handler ===============

# เพิ่ม reaction เมื่อมีคนพูดถึงคำว่า "good" หรือ "great"
@app.message(re.compile(r"(good|great|เยี่ยม|ดี)", re.IGNORECASE))
def add_reaction(message, client):
    try:
        client.reactions_add(
            channel=message['channel'],
            timestamp=message['ts'],
            name='tada'
        )
    except Exception as e:
        print(f"Error adding reaction: {e}")

# =============== Error Handler ===============

@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")

# =============== Start Bot ===============

if __name__ == "__main__":
    print("⚡️ BL1NK Slack Bot กำลังทำงาน (Socket Mode)...")
    print("📡 พร้อมรับข้อความจาก Slack แล้ว!")
    print("=" * 50)
    
    # ใช้ Socket Mode
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

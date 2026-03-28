import telebot
import threading
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== CONFIG =====
TOKEN = "8594033718:AAGjW0tWT3iFin7z8hegBlCkffdOR0yFM5U"
bot = telebot.TeleBot(TOKEN, threaded=True)

# ===== CHANNEL LINKS (4 SHOW) =====
ch1 = "https://t.me/+ws43qQ4tWZQwOGE1"
ch2 = "https://t.me/+XNLWdHJ7n9kzOGQ1"
ch3 = "https://t.me/+spxy0njzur9hNTI1"
ch4 = "https://t.me/+1_Yj8PXYUhc1MDE1"

# ===== CHANNEL IDS (ALL 4 CHECK) =====
channels = [
    -1003803906100,
    -1003838757488,
    -1003835376484,
    -100xxxxxxxxxx   # ⚠️ yaha 4th channel ka ID daal
]

# ===== JOIN CHECK =====
def check_join(user_id):
    try:
        for ch in channels:
            member = bot.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        return True
    except:
        return False

# ===== BUTTONS =====
def join_buttons():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton("📢 Join Channel 1", url=ch1),
        InlineKeyboardButton("📢 Join Channel 2", url=ch2),
        InlineKeyboardButton("📢 Join Channel 3", url=ch3),
        InlineKeyboardButton("📢 Join Channel 4", url=ch4),
        InlineKeyboardButton("✅ I Joined", callback_data="check")
    )
    return markup

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start(message):
    if not check_join(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "⚠️ पहले सभी चैनल join करो फिर Continue दबाओ",
            reply_markup=join_buttons()
        )
    else:
        bot.send_message(message.chat.id, "✅ Welcome Bro 🔥 Bot Working")

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "check":
        if check_join(call.from_user.id):
            bot.edit_message_text(
                "✅ Welcome Bro 🔥 Bot Working",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.answer_callback_query(call.id, "❌ सभी चैनल join करो")

# ===== KEEP ALIVE (RENDER) =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running 🔥"

def run():
    app.run(host='0.0.0.0', port=8080)

# ===== RUN =====
threading.Thread(target=run).start()

print("Bot Started 🔥")
bot.infinity_polling()

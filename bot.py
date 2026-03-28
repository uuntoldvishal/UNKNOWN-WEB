import telebot
import time
import os
import threading
import json
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# ---------------- CONFIG ----------------
TOKEN = "8594033718:AAGjW0tWT3iFin7z8hegBlCkffdOR0yFM5U"
ADMIN_ID = 8266427252
DATA_FILE = "data.json"

bot = telebot.TeleBot(TOKEN, threaded=True)

# ---------------- LOAD / SAVE ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

buttons_data = load_data()

# ---------------- CHANNEL CHECK ----------------
channels = [-1003803906100, -1003838757488, -1003835376484]

def check_join(user_id):
    try:
        for ch in channels:
            member = bot.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        return True
    except:
        return False

def join_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Join Channel", url="https://t.me"))
    markup.add(InlineKeyboardButton("Continue", callback_data="check"))
    return markup

# ---------------- MENU ----------------
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if not buttons_data:
        markup.add("No Data")
    else:
        for name in buttons_data.keys():
            markup.add(name)
    return markup

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Join channels first", reply_markup=join_buttons())

# ---------------- CHECK ----------------
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if check_join(call.from_user.id):
        bot.send_message(call.message.chat.id, "Select option 👇", reply_markup=main_menu())
    else:
        bot.answer_callback_query(call.id, "Join channels first ❌")

# ---------------- BUTTON CLICK ----------------
@bot.message_handler(func=lambda message: message.text in buttons_data)
def open_button(message):
    name = message.text
    items = buttons_data.get(name, [])

    if not items:
        bot.send_message(message.chat.id, "No items available")
        return

    markup = InlineKeyboardMarkup()
    for i in range(len(items)):
        markup.add(InlineKeyboardButton(f"Item {i+1}", callback_data=f"{name}|{i}"))

    bot.send_message(message.chat.id, name, reply_markup=markup)

# ---------------- SEND ITEM ----------------
@bot.callback_query_handler(func=lambda call: "|" in call.data)
def send_item(call):
    try:
        name, index = call.data.split("|")
        index = int(index)
        data = buttons_data[name][index]

        try:
            bot.send_document(call.message.chat.id, data)
        except:
            bot.send_message(call.message.chat.id, data)

    except:
        bot.send_message(call.message.chat.id, "Error ❌")

# ---------------- ADD BUTTON ----------------
@bot.message_handler(commands=['addbtn'])
def add_btn(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "Send button name:")
    bot.register_next_step_handler(msg, save_btn)

def save_btn(message):
    name = message.text.strip()

    if name in buttons_data:
        bot.send_message(message.chat.id, "Already exists ❌")
        return

    buttons_data[name] = []
    save_data(buttons_data)

    bot.send_message(message.chat.id, f"✅ Button '{name}' created")
    bot.send_message(message.chat.id, "Menu updated 👇", reply_markup=main_menu())

# ---------------- DELETE BUTTON ----------------
@bot.message_handler(commands=['delbtn'])
def delete_btn(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "Send button name to delete:")
    bot.register_next_step_handler(msg, confirm_delete_btn)

def confirm_delete_btn(message):
    name = message.text.strip()

    if name not in buttons_data:
        bot.send_message(message.chat.id, "Button not found ❌")
        return

    del buttons_data[name]
    save_data(buttons_data)

    bot.send_message(message.chat.id, f"✅ Button '{name}' deleted")
    bot.send_message(message.chat.id, "Updated Menu 👇", reply_markup=main_menu())

# ---------------- ADD ITEM ----------------
@bot.message_handler(commands=['additem'])
def add_item(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "Send button name:")
    bot.register_next_step_handler(msg, get_item_name)

def get_item_name(message):
    name = message.text.strip()

    if name not in buttons_data:
        bot.send_message(message.chat.id, "Button not found ❌")
        return

    msg = bot.send_message(message.chat.id, "Send file or text:")
    bot.register_next_step_handler(msg, save_item, name)

def save_item(message, name):
    try:
        if message.content_type == 'document':
            buttons_data[name].append(message.document.file_id)

        elif message.content_type == 'video':
            buttons_data[name].append(message.video.file_id)

        elif message.content_type == 'audio':
            buttons_data[name].append(message.audio.file_id)

        elif message.content_type == 'text':
            buttons_data[name].append(message.text)

        else:
            bot.send_message(message.chat.id, "Unsupported ❌")
            return

        save_data(buttons_data)
        bot.send_message(message.chat.id, "✅ Item added")

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# ---------------- ADMIN ----------------
@bot.message_handler(commands=['admin'])
def admin_view(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not buttons_data:
        bot.send_message(message.chat.id, "No data ❌")
        return

    text = "📊 DATA:\n\n"
    for k, v in buttons_data.items():
        text += f"{k} → {len(v)} items\n"

    bot.send_message(message.chat.id, text)

# ---------------- KEEP ALIVE ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot running 🚀"

def run_bot():
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)
            time.sleep(5)

threading.Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=10000)

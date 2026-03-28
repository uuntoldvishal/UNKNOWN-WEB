import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

🔑 TOKEN

TOKEN = "8594033718:AAGjW0tWT3iFin7z8hegBlCkffdOR0yFM5U"
bot = telebot.TeleBot(TOKEN, threaded=False)

👑 ADMIN

ADMIN_ID = 8266427252

📦 STORAGE

buttons_data = {}

📢 CHANNEL LINKS

ch1 = "https://t.me/+Ws43qQ4tWZQwOGE1"
ch2 = "https://t.me/+XNLWdHJ7n9kzOGQ1"
ch3 = "https://t.me/+spxy0njzur9hNTI1"
ch4 = "https://t.me/+l_Yj8PXYUhc1MDE1"

channels = [
-1003803906100,
-1003838757488,
-1003835376484
]

🔍 JOIN CHECK

def check_join(user_id):
try:
for ch in channels:
member = bot.get_chat_member(ch, user_id)
if member.status in ["left", "kicked"]:
return False
return True
except:
return False

🔘 JOIN BUTTONS

def join_buttons():
markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("📢 Channel 1", url=ch1))
markup.add(InlineKeyboardButton("📢 Channel 2", url=ch2))
markup.add(InlineKeyboardButton("📢 Channel 3", url=ch3))
markup.add(InlineKeyboardButton("📢 Channel 4", url=ch4))
markup.add(InlineKeyboardButton("✅ Continue", callback_data="check"))
return markup

🔘 MAIN MENU (BOTTOM BUTTONS)

def main_menu():
markup = ReplyKeyboardMarkup(resize_keyboard=True)
for name in buttons_data:
markup.add(name)
return markup

🚀 START

@bot.message_handler(commands=['start'])
def start(message):
bot.send_message(message.chat.id, "📢 Join all channels 👇", reply_markup=join_buttons())

🔁 CHECK JOIN

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
if check_join(call.from_user.id):
bot.send_message(call.message.chat.id, "👇 Select option", reply_markup=main_menu())
else:
bot.answer_callback_query(call.id, "❌ Pehle join karo")

🔘 BUTTON CLICK

@bot.message_handler(func=lambda message: message.text in buttons_data)
def open_button(message):
name = message.text
items = buttons_data.get(name, [])

if not items:  
    bot.send_message(message.chat.id, "❌ Isme abhi kuch add nahi hai")  
    return  

markup = InlineKeyboardMarkup()  
for i in range(len(items)):  
    markup.add(InlineKeyboardButton(f"📦 Item {i+1}", callback_data=f"item_{name}_{i}"))  

bot.send_message(message.chat.id, f"📂 {name}", reply_markup=markup)

📦 SEND ITEM

@bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
def send_item(call):
, name, index = call.data.split("")
index = int(index)
data = buttons_data[name][index]

try:  
    bot.send_document(call.message.chat.id, data)  
except:  
    bot.send_message(call.message.chat.id, data)

👑 ADD BUTTON

@bot.message_handler(commands=['addbtn'])
def add_btn(message):
if message.from_user.id == ADMIN_ID:
bot.send_message(message.chat.id, "📝 Button name bhejo:")
bot.register_next_step_handler(message, save_btn)

def save_btn(message):
name = message.text.strip()
buttons_data[name] = []
bot.send_message(message.chat.id, f"✅ Button '{name}' ban gaya")

➕ ADD ITEM (FIXED)

@bot.message_handler(commands=['additem'])
def add_item(message):
if message.from_user.id == ADMIN_ID:
bot.send_message(message.chat.id, "📝 Button name likho:")
bot.register_next_step_handler(message, get_item_name)

def get_item_name(message):
name = message.text.strip()

if name not in buttons_data:  
    bot.send_message(message.chat.id, "❌ Button nahi mila")  
    return  

msg = bot.send_message(message.chat.id, "📂 Ab file ya link bhejo:")  
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
        bot.send_message(message.chat.id, "❌ Unsupported type")  
        return  

    bot.send_message(message.chat.id, "✅ Item add ho gaya 🔥")  

except Exception as e:  
    bot.send_message(message.chat.id, f"Error: {e}")

❌ DELETE BUTTON

@bot.message_handler(commands=['delbtn'])
def del_btn(message):
if message.from_user.id == ADMIN_ID:
bot.send_message(message.chat.id, "❌ Button name?")
bot.register_next_step_handler(message, confirm_del_btn)

def confirm_del_btn(message):
name = message.text.strip()
if name in buttons_data:
del buttons_data[name]
bot.send_message(message.chat.id, "🗑️ Button delete ho gaya")
else:
bot.send_message(message.chat.id, "❌ Button nahi mila")

❌ DELETE ITEM

@bot.message_handler(commands=['delitem'])
def del_item(message):
if message.from_user.id == ADMIN_ID:
bot.send_message(message.chat.id, "📝 Button name?")
bot.register_next_step_handler(message, ask_index)

def ask_index(message):
name = message.text.strip()
if name not in buttons_data:
bot.send_message(message.chat.id, "❌ Button nahi mila")
return

bot.send_message(message.chat.id, "🔢 Item number?")  
bot.register_next_step_handler(message, delete_item, name)

def delete_item(message, name):
try:
index = int(message.text) - 1
if index < len(buttons_data[name]):
buttons_data[name].pop(index)
bot.send_message(message.chat.id, "🗑️ Item delete ho gaya")
else:
bot.send_message(message.chat.id, "❌ Invalid number")
except:
bot.send_message(message.chat.id, "❌ Number bhejo")

📊 ADMIN PANEL (FIXED)

@bot.message_handler(commands=['admin'])
def admin_view(message):
if message.from_user.id == ADMIN_ID:
if not buttons_data:
bot.send_message(message.chat.id, "❌ Koi data nahi hai")
return

text = "📊 DATA:\n\n"  
    for k, v in buttons_data.items():  
        text += f"🔘 {k} → {len(v)} items\n"  

    bot.send_message(message.chat.id, text)

🔄 RUN

print("🔥 BOT STARTED")

while True:
try:
bot.infinity_polling(timeout=60, long_polling_timeout=30)
except Exception as e:
print("Error:", e)
time.sleep(5)

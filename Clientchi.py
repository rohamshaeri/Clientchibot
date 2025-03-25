import telebot
from telebot.types import Message
import json
import os

API_TOKEN = '7535744536:AAEK54sJMgQ93A9fCfOyF8YcAM12L_hDFH8'
CHANNEL_USERNAME = 'Clientchi'  # without @

bot = telebot.TeleBot(API_TOKEN)

# Basic JSON DB
DB_FILE = 'referrals.json'
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

# Command: /start [referral_id]
@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    db = load_db()
    user_id = str(message.from_user.id)
    args = message.text.split()

    if user_id not in db:
        db[user_id] = {'referrals': [], 'invited_by': None, 'rewarded': False}

    # Handle referral logic
    if len(args) > 1:
        referrer_id = args[1]
        if referrer_id != user_id and referrer_id in db:
            if user_id not in db[referrer_id]['referrals']:
                db[referrer_id]['referrals'].append(user_id)
                db[user_id]['invited_by'] = referrer_id
                save_db(db)

                # Notify referrer if 5 reached
                if len(db[referrer_id]['referrals']) == 5 and not db[referrer_id]['rewarded']:
                    bot.send_message(referrer_id, 'تبریک! شما ۵ دعوت موفق داشتید. کلاینت رایگان شما آماده‌ست 🎉')
                    db[referrer_id]['rewarded'] = True
                    save_db(db)

    # Generate referral link
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    bot.send_message(message.chat.id, f" خوش اومدی!\n\nلینک دعوت اختصاصی شما:\n{ref_link}\n\nهر ۵ دعوت = ۱ کلاینت رایگان ")
    # Command: /stats
@bot.message_handler(commands=['stats'])
def handle_stats(message: Message):
    db = load_db()
    user_id = str(message.from_user.id)
    if user_id in db:
        count = len(db[user_id]['referrals'])
        bot.send_message(message.chat.id, f"شما تا الان {count} دعوت موفق داشتید.")
    else:
        bot.send_message(message.chat.id, "هنوز ثبت‌نام نکردی. با /start شروع کن.")

bot.polling()
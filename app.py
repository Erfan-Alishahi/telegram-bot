import telebot
import requests
import json
import os
from fuzzywuzzy import fuzz
from telebot import types

# Load the API token securely from an environment variable
API_TOKEN = "7055613975:AAFYOluPx0WUoAKhv_2Ft334fnsu9x9ei1A"
bot = telebot.TeleBot(API_TOKEN)

# Download the first JSON data
url_first = "https://raw.githubusercontent.com/Erfan-Alishahi/database/main/secondary-database.json"
response_first = requests.get(url_first)
if response_first.status_code == 200:
    primary_data = response_first.json()
else:
    raise Exception("Could not retrieve data from the primary URL")

# Load the secondary JSON data
jsn = open('data-bot.json', 'r', encoding='utf-8')
secondary_data = json.load(jsn)

# Function to find similar names
def find_similar_names_1(name):
    matches = []
    name_parts = name.split(" ")
    for department_data in primary_data.values():
        for person in department_data:
            for na in name_parts:
                if na.lower() in person['Name'].lower():
                    matches.append((person['Name'], person["Department"]))
    return list(set(matches))

def find_similar_names_2(name):
    matches = []
    for department_data in primary_data.values():
        for person in department_data:
            similarity_ratio = fuzz.ratio(name, person['Name'])
            if similarity_ratio >= 51:
                matches.append((person['Name'], person['Department']))
    return matches

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        """
سلام دوست عزیز، به بات ما خوش آمدید!
برای پیدا کردن اطلاعات استاد مورد نظر، کافیست نام وی را به فارسی وارد کنید.
در صورتی که نام را به درستی ندانید، می‌توانید تقریبا مشابه نام را وارد کنید و بات تلاش خواهد کرد تا نام متناظر را پیدا کند.
"""
    )

# Handle searching for people by name
@bot.message_handler(content_types=['text'])
def people(message):
    found = False
    name = message.text.strip()

    # First, attempt to find an exact match
    for department, department_data in primary_data.items():
        for person in department_data:
            if name == person['Name']:
                found = True
                person_id = person['ID']
                department_secondary_data = secondary_data.get(department, [])
                for secondary_person in department_secondary_data:
                    if secondary_person.get('ID') == person_id:
                        info_str = "\n".join([f"*{key}*: `{value}`" for key, value in secondary_person.items() if key != 'pic' and key != 'ID' and key != 'web'])
                        if 'web' in secondary_person:
                            info_str += '\n*personal page*: ' + f"[link]({secondary_person['web']})"
                        info_str += "\n*Department*: "
                        info_str += person['Department']
                        bot.send_photo(message.chat.id, secondary_person.get('pic'), info_str, parse_mode="markdown")
                        break
                break

    # If no exact match is found, try to find similar names
    if not found:
        similar_names = find_similar_names_1(name)
        if similar_names:
            # Create an inline keyboard
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for f in similar_names:
                button_text = f"{f[0]} - دانشکده: {f[1]}"
                button = types.InlineKeyboardButton(button_text, callback_data=f[0])
                keyboard.add(button)
            bot.send_message(message.chat.id, "استاد مورد نظر یافت نشد. لطفاً از لیست پیشنهادی زیر انتخاب کنید:", reply_markup=keyboard)
            return
        else:
            similar_names = find_similar_names_2(name)
            if similar_names:
                # Create an inline keyboard
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                for f in similar_names:
                    button_text = f"{f[0]} - دانشکده: {f[1]}"
                    button = types.InlineKeyboardButton(button_text, callback_data=f[0])
                    keyboard.add(button)
                bot.send_message(message.chat.id, "استاد مورد نظر یافت نشد. لطفاً از لیست پیشنهادی زیر انتخاب کنید:", reply_markup=keyboard)
                return

    if not found:
        bot.send_message(message.chat.id, "متاسفانه اطلاعاتی در مورد این استاد یافت نشد.")

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    name = call.data
    for department, department_data in primary_data.items():
        for person in department_data:
            if name == person['Name']:
                person_id = person['ID']
                department_secondary_data = secondary_data.get(department, [])
                for secondary_person in department_secondary_data:
                    if secondary_person.get('ID') == person_id:
                        info_str = "\n".join([f"*{key}*: `{value}`" for key, value in secondary_person.items() if key != 'pic' and key != 'ID' and key != 'web'])
                        if 'web' in secondary_person:
                            info_str += '\n*personal page*: ' + f"[link]({secondary_person['web']})"
                        info_str += "\n*Department*: "
                        info_str += person['Department']
                        bot.send_photo(call.message.chat.id, secondary_person.get('pic'), info_str, parse_mode="markdown")
                        break

bot.infinity_polling()

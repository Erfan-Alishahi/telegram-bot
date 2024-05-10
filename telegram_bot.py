import telebot
import requests
import json
import os

# Load the API token securely from an environment variable
API_TOKEN = "6614220572:AAGIObyk0jZbZjAforJCysqdkhNLlbpZHzg"
bot = telebot.TeleBot(API_TOKEN)

# Download the first JSON data
url_first = "https://raw.githubusercontent.com/Erfan-Alishahi/database/main/secondary-database.json"
response_first = requests.get(url_first)
if response_first.status_code == 200:
    primary_data = response_first.json()
else:
    raise Exception("Could not retrieve data from the primary URL")

jsn = open('data-bot.json', 'r', encoding='utf-8')
secondary_data = json.load(jsn)

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "سلام دوست عزیز، برای پیدا کردن اطلاعات استاد مورد نظر، کافیست نام وی را به انگلیسی وارد کنید."
    )

# Handle searching for people by name
@bot.message_handler(content_types=['text'])
def people(message):
    found = False
    for department, department_data in primary_data.items():
        for person in department_data:
            if message.text == person['Name']:
                found = True
                person_id = person['ID']
                department_secondary_data = secondary_data.get(department, [])
                for secondary_person in department_secondary_data:
                    if secondary_person.get('ID') == person_id:
                        info_str = "\n".join([f"{key}: {value}" for key, value in secondary_person.items()])
                        bot.send_photo(message.chat.id,secondary_person.get('pic'),info_str)
                        break
                break

    if not found:
        bot.send_message(message.chat.id, "متاسفانه اطلاعاتی در مورد این استاد یافت نشد.")

bot.infinity_polling()

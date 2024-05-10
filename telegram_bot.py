import telebot
import requests
import json
import os

# Load the API token securely from an environment variable
API_TOKEN = "6614220572:AAGIObyk0jZbZjAforJCysqdkhNLlbpZHzg"
bot = telebot.TeleBot(API_TOKEN)
jsn = open('data-bot.json', 'r', encoding='utf-8')
databot = json.load(jsn)
# Download the JSON data
url = "https://raw.githubusercontent.com/Erfan-Alishahi/database/main/secondary-database.json"
response = requests.get(url)
if response.status_code == 200:
    nested_data = response.json()
else:
    raise Exception("Could not retrieve data from the provided URL")

# Flatten the nested JSON structure into a list of dictionaries
data = []
for key, value in nested_data.items():
    data.extend(value)

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
    for person in data:
        if message.text == person['Name']:
            found = True
            for i in range(len(databot)):
                if message.text == databot[i]['NameFa']:
                    string = str()
                    for x,y in databot[i].items():
                        if x != "pic":
                            string += f"{x}: {y}\n"
                    bot.send_photo(message.chat.id,databot[i]["pic"], string)
                    break
            break

    if not found:
        bot.send_message(message.chat.id, "متاسفانه اطلاعاتی در مورد این استاد یافت نشد.")

bot.infinity_polling()

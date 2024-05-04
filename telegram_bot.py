import telebot
import json

API_TOKEN = "6614220572:AAGIObyk0jZbZjAforJCysqdkhNLlbpZHzg"
bot = telebot.TeleBot(API_TOKEN) # bot object
jsn = open(r"C:\\Users\\Lenovo\\Desktop\data-bot.json")
data = json.load(jsn)


#Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام دوست عزیز، برای پیدا کردن اطلاعات استاد مورد نظر، کافیست نام وی را به انگلیسی وارد کنید.")
    
#Handle search people
@bot.message_handler(content_types=['text'])
def people(message):
    for i in range(len(data)):
        if message.text == data[i]['Name']:
            string = str()
            for x,y in data[i].items():
                if x != "pic":
                    string += f"{x}: {y}\n"
            bot.send_photo(message.chat.id,data[i]["pic"], string)
            break

bot.infinity_polling()

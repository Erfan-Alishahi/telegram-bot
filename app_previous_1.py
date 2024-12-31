import telebot
import requests
import json
from fuzzywuzzy import fuzz
from github import Github
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# bot API token
API_TOKEN = "7055613975:AAFYOluPx0WUoAKhv_2Ft334fnsu9x9ei1A"
bot = telebot.TeleBot(API_TOKEN)

# Load the primary JSON data
"""PRIMARY_DATA_URL = "https://raw.githubusercontent.com/Erfan-Alishahi/database/main/secondary-database.json"
response_primary = requests.get(PRIMARY_DATA_URL)
if response_primary.status_code == 200:
    primary_data = response_primary.json()
else:
    raise Exception("Could not retrieve data from the primary URL")

# Load the secondary JSON data
with open('data-bot.json', 'r', encoding='utf-8') as jsn2:
    secondary_data = json.load(jsn2)"""
#-----------------------------------------------------------------
# download both datas from github to read anad write
GITHUB_TOKEN = "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"
REPO_NAME = "Erfan-Alishahi/telegram-bot"
BIG_JSON_FILE_PATH = "data-bot.json"
LITLE_JSON_FILE_PATH = "data.json"
# connect to github
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# download both json file's 
big_data_content = repo.get_contents(BIG_JSON_FILE_PATH)
litle_data_content = repo.get_contents(LITLE_JSON_FILE_PATH)

json_big_data = json.loads(big_data_content.decoded_content.decode('utf-8'))
json_litle_data = json.loads(litle_data_content.decoded_content.decode('utf-8'))


#-----------------------------------------------------------------

# Function to find similar names (partial match)
def find_similar_names_partial(name):        # find_similar_names_1
    matches = []
    name_parts = name.split(" ")
    for department_data in json_litle_data.values():
        for person in department_data:
            for na in name_parts:
                if na.lower() in person['Name'].lower():
                    matches.append((person['Name'], person["Department"]))
    return list(set(matches))

# Function to find similar names (fuzzy match)
def find_similar_names_fuzzy(name):          # find_similar_names_2
    matches = []
    for department_data in json_litle_data.values():
        for person in department_data:
            similarity_ratio = fuzz.ratio(name, person['Name'])
            if similarity_ratio >= 51:
                matches.append((person['Name'], person['Department']))
    return matches

# people states
user_states = {}

# admin tools
selected_prof = str()

# states
STATE_MAIN_MENU = "main_menu"
STATE_CONTACT_ADMIN = "contact_admin"
STATE_SEARCH_PROFESSOR = "search_professor"
STATE_ADMIN_MAIN_PANEL = "admin_panel"
STATE_ADMIN_SECOND_PANEL = "admin_second_panel"
STATE_ADMIN_THIRD_PANEL = "admin_third_panel"
STATE_ADMIN_EDIT_PROF_PANEL = "admin_edit_prof_panel"
STATE_ADMIN_NEW_PROF_PANEL = "admin_new_prof_panel"
# for new prof
STATE_ADMIN_NEW_PROF_PANEL_NAME = "admin_new_prof_panel_name"
STATE_ADMIN_NEW_PROF_PANEL_ROOM = "admin_new_prof_panel_room"
STATE_ADMIN_NEW_PROF_PANEL_EMAIL = "admin_new_prof_panel_email"
STATE_ADMIN_NEW_PROF_PANEL_PHONE = "admin_new_prof_panel_phone"
STATE_ADMIN_NEW_PROF_PANEL_FAX = "admin_new_prof_panel_fax"
STATE_ADMIN_NEW_PROF_PANEL_WEB = "admin_new_prof_panel_web"
STATE_ADMIN_NEW_PROF_PANEL_PIC = "admin_new_prof_panel_pic"
STATE_ADMIN_NEW_PROF_PANEL_DEPARTMENT = "admin_new_prof_panel_department"
STATE_ADMIN_NEW_PROF_PANEL_POSITION = "admin_new_prof_panel_position"
# for edit prof
STATE_ADMIN_EDIT_PROF_PANEL_EMAIL = "admin_edit-prof_panel_email"
STATE_ADMIN_EDIT_PROF_PANEL_PHONE = "admin_edit-prof_panel_phone"
STATE_ADMIN_EDIT_PROF_PANEL_ROOM = "admin_edit-prof_panel_room"
#------------------
ADMIN_CHAT_ID = "6919820799"
ADMIN_SECRET_KEY = "itsmeimback"
#------------------
def send_to_admin(message, user_id):
    bot.send_message(ADMIN_CHAT_ID, f'New message from `{user_id}`:\n\n*{message}*', parse_mode='markdown')

# main buttons
def main_menu_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("جستجوی استاد"), KeyboardButton("ارتباط با ادمین"))
    return markup

# back button
def back_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("بازگشت"))
    return markup

# main admin buttons
def admin_main_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = "انتخاب استاد"
    button_2 = "خروج از پنل ادمین"
    markup.add(button_1, button_2)
    return markup

# second admin butthons
def admin_second_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = "اضافه کردن استاد جدید"
    button_2 = "بازگشت"
    markup.add(button_2, button_1)
    return markup

# third admin buttons
def admin_third_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = "بازگشت"
    button_2 = "حذف"
    button_3 = "ویرایش"
    markup.add(button_1, button_2, button_3)
    return markup

# add new prof buttons 
def admin_new_prof_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = "Name"
    button_2 = "Room"
    button_3 = "E-Mail"
    button_4 = "Phone"
    button_5 = "Fax"
    button_6 = "web"
    button_7 = "pic"
    button_8 = "Department"
    button_9 = "Position"
    button_10 = "بازگشت"
    button_11 = "تمام"
    markup.add(button_1,button_2,button_3,button_4,button_5,button_6,button_7,button_8,button_9,button_10,button_11)
    return markup

# edit prof buttons
def admin_edit_prof_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = "Room"
    button_2 = "E-Mail"
    button_3 = "Phone"
    button_4 = "بازگشت"
    button_5 = "تمام"
    markup.add(button_1,button_2,button_3,button_4,button_5)
    return markup

# new prof dictionary
new_prof = dict()

# edit prof dictionary
edit_prof = dict()

# هندلر برای دستور /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_states[message.chat.id] = STATE_MAIN_MENU
    bot.send_message(
        message.chat.id,
        "به ربات خوش آمدید! یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu_buttons()
    )

# هندلر برای دریافت پیام
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    state = user_states.get(user_id, STATE_MAIN_MENU)
    
    global new_prof
    global selected_prof
    global edit_prof

    if state == STATE_MAIN_MENU:
        if message.text == "جستجوی استاد":
            user_states[user_id] = STATE_SEARCH_PROFESSOR
            bot.send_message(
                user_id,
                "لطفاً نام استاد را وارد کنید:",
                reply_markup=back_button()
            )
        elif message.text == "ارتباط با ادمین":
            user_states[user_id] = STATE_CONTACT_ADMIN
            bot.send_message(
                user_id,
                "پیام خود را برای ادمین ارسال کنید:",
                reply_markup=back_button()
            )
        elif message.text == ADMIN_SECRET_KEY and message.chat.id == int(ADMIN_CHAT_ID):
            user_states[user_id] = STATE_ADMIN_MAIN_PANEL
            bot.send_message(
                user_id,
                "به پنل ادمین خوش آمدید!",
                reply_markup=admin_main_buttons()
            )
        else:
            bot.send_message(
                user_id,
                "لطفاً یکی از گزینه‌ها را انتخاب کنید.",
                reply_markup=main_menu_buttons()
            )

    elif state == STATE_CONTACT_ADMIN:
        if message.text == "بازگشت":
            user_states[user_id] = STATE_MAIN_MENU
            bot.send_message(
                user_id,
                "به منوی اصلی برگشتید.",
                reply_markup=main_menu_buttons()
            )
        else:
            send_to_admin(message.text, user_id)
            bot.send_message(
                user_id,
                "پیام شما برای ادمین ارسال شد.",
                reply_markup=back_button()
            )

    elif state == STATE_SEARCH_PROFESSOR:
        if message.text == "بازگشت":
            user_states[user_id] = STATE_MAIN_MENU
            bot.send_message(
                user_id,
                "به منوی اصلی برگشتید.",
                reply_markup=main_menu_buttons()
            )
        else:
#------------------------------------------------------------------------------------
            found = False
            name = message.text.strip()
        
            # First, attempt to find an exact match
            for department, department_data in json_litle_data.items():
                for person in department_data:
                    if name == person['Name']:
                        found = True
                        person_id = person['ID']
                        department_secondary_data = json_big_data.get(department, [])
                        for secondary_person in department_secondary_data:
                            if secondary_person.get('ID') == person_id:
                                info_str = "\n".join([f"*{key}*: `{value}`" for key, value in secondary_person.items() if key != 'pic' and key != 'ID' and key != 'web'])
                                if 'web' in secondary_person:
                                    info_str += '\n*personal page*: ' + f"[link]({secondary_person['web']})"
                                info_str += "\n*Department*: "
                                info_str += person['Department']
                                if secondary_person.get('pic') != None:
                                    bot.send_photo(message.chat.id, secondary_person.get('pic'), info_str, parse_mode="markdown")
                                else:
                                    bot.send_message(message.chat.id, info_str, parse_mode="markdown")
                                break
                        break
                    
            # If no exact match is found, try to find similar names
            if not found:
                similar_names = find_similar_names_partial(name)
                if similar_names:
                    # Create an inline keyboard
                    keyboard = InlineKeyboardMarkup(row_width=1)
                    for f in similar_names:
                        button_text = f"{f[0]} - دانشکده: {f[1]}"
                        button = InlineKeyboardButton(button_text, callback_data=f[0])
                        keyboard.add(button)
                    bot.send_message(message.chat.id, "استاد مورد نظر یافت نشد. لطفاً از لیست پیشنهادی زیر انتخاب کنید:", reply_markup=keyboard)
                    return
                else:
                    similar_names = find_similar_names_fuzzy(name)
                    if similar_names:
                        # Create an inline keyboard
                        keyboard = InlineKeyboardMarkup(row_width=1)
                        for f in similar_names:
                            button_text = f"{f[0]} - دانشکده: {f[1]}"
                            button = InlineKeyboardButton(button_text, callback_data=f[0])
                            keyboard.add(button)
                        bot.send_message(message.chat.id, "استاد مورد نظر یافت نشد. لطفاً از لیست پیشنهادی زیر انتخاب کنید:", reply_markup=keyboard)
                        return
        
            if not found:
                bot.send_message(message.chat.id, "متاسفانه اطلاعاتی در مورد این استاد یافت نشد.")
        


#------------------------------------------------------------------------------------
    elif state == STATE_ADMIN_MAIN_PANEL:
        if message.text == "خروج از پنل ادمین":
            user_states[user_id] = STATE_MAIN_MENU
            bot.send_message(
                user_id,
                "از پنل ادمین خارج شدید.",
                reply_markup=main_menu_buttons()
            )
        elif message.text == "انتخاب استاد":
            user_states[user_id] = STATE_ADMIN_SECOND_PANEL
            bot.send_message(
                user_id,
                "میتوانید برای تغییر اطلاعات استاد موجود در دیتابیس، آیدی ایشان را وارد نمایید و یا یکی از گزینه های زیر را انتخاب:",
                reply_markup=admin_second_buttons()
            )

    elif state == STATE_ADMIN_SECOND_PANEL:
        if message.text == "بازگشت":
            user_states[user_id] = STATE_ADMIN_MAIN_PANEL
            bot.send_message(
                user_id,
                "به منوی اصلی ادمین بازگشتید.",
                reply_markup=admin_main_buttons()
                )
        elif message.text == "اضافه کردن استاد جدید":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        elif message.text.isdigit():# اینجا بعد از وارد کردن آیدی استاد، باید کلید و مقدار استاد رو از دیکشنری بیاره واسمون
            Found = False
            global prof_id
            prof_id = int(message.text)
            for dep in json_big_data: # dep --> 11000, 12000, 13000 and ..., type --> str
                for people in json_big_data[dep]: # dicts, type --> dict
                    if people["ID"] == prof_id:
                        Found = True
                        user_states[user_id] = STATE_ADMIN_THIRD_PANEL
                        selected_prof = (dep, prof_id)
                        bot.send_message(
                            user_id,
                            f"استاد یافت شد:\n *{people['Name']}*\n شماره دانشکده: *{dep}*",
                            reply_markup=admin_third_buttons(),
                            parse_mode='markdown'
                        )
                        break
            if not Found:
                bot.send_message(
                user_id,
                "استاد یافت نشد، مجددا تلاش کنید."
            )

    elif state == STATE_ADMIN_THIRD_PANEL:
        if message.text == "بازگشت":
            user_states[user_id] = STATE_ADMIN_SECOND_PANEL
            bot.send_message(
                user_id,
                "میتوانید برای تغییر اطلاعات استاد موجود در دیتابیس، آیدی ایشان را وارد نمایید و یا یکی از گزینه های زیر را انتخاب:",
                reply_markup=admin_second_buttons()
            )
        elif message.text == "حذف":
            bot.send_message(
                user_id,
                "برای تایید حذف اطلاعات این استاد، کلمه `CONFIRM-DELETE` را بنویسید.",
                parse_mode="markdown"
                )
        elif message.text == "ویرایش":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            bot.send_message(
                user_id,
                "برای ویرایش اطلاعات، یکی از گزینه های زیر را انتخاب کنید:",
                reply_markup=admin_edit_prof_buttons()
            )
        elif message.text == "CONFIRM-DELETE":
            # delete from big json
            for dep in json_big_data:
                for people in json_big_data[dep]:
                    if people['ID'] == selected_prof[1]:
                        json_big_data[dep].remove(people)
            # delete from little json
            for dep in json_litle_data:
                for people in json_litle_data[dep]:
                    if people['ID'] == selected_prof[1]:
                        json_litle_data[dep].remove(people)
            # update big-json file
            updated_json = json.dumps(json_big_data, indent=4)
            repo.update_file(
                path=BIG_JSON_FILE_PATH,
                message="Updated json file from sharif-hub",
                content=updated_json,
                sha=big_data_content.sha
            )
            # update little-json file
            updated_json = json.dumps(json_litle_data, indent=4)
            repo.update_file(
                path=LITLE_JSON_FILE_PATH,
                message="Updated json file from sharif-hub",
                content=updated_json,
                sha=litle_data_content.sha
            )
            user_states[user_id] = STATE_ADMIN_SECOND_PANEL
            # send message
            bot.send_message(
                user_id,
                f"اطلاعات استاد مورد نظر با آیدی *{prof_id}* با موفقیت حذف شد.",
                parse_mode='markdown',
                reply_markup=admin_second_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_EDIT_PROF_PANEL:
        if message.text == "بازگشت":
            user_states[user_id] = STATE_ADMIN_THIRD_PANEL
            bot.send_message(
                user_id,
                "بازگشتید، یک گزینه را انتخاب کنید",
                reply_markup=admin_third_buttons()
            )
            edit_prof = dict()
        elif message.text == "تمام":
            for people in json_big_data[selected_prof[0]]:
                if people["ID"] == selected_prof[1]:
                    if edit_prof.get("Room") != None:
                        people["Room"] = edit_prof["Room"]
                    if edit_prof.get("Phone") != None:
                        people["Phone"] = edit_prof["Phone"]
                    if edit_prof.get("E-Mail") != None:   
                        people["E-Mail"] = edit_prof["E-Mail"]
                    ########################
                    # update big-json file
                    updated_json = json.dumps(json_big_data, indent=4)
                    repo.update_file(
                        path=BIG_JSON_FILE_PATH,
                        message="Updated json file from sharif-hub",
                        content=updated_json,
                        sha=big_data_content.sha
                    )
                    # update little-json file
                    updated_json = json.dumps(json_litle_data, indent=4)
                    repo.update_file(
                        path=LITLE_JSON_FILE_PATH,
                        message="Updated json file from sharif-hub",
                        content=updated_json,
                        sha=litle_data_content.sha
                    )
                    ########################
                    user_states[user_id] = STATE_ADMIN_THIRD_PANEL
                    bot.send_message(
                        user_id,
                        f"اطلاعات استاد مورد نظر با آیدی: *{selected_prof[1]}* با موفقیت تغییر پیدا کرد",
                        parse_mode="markdown",
                        reply_markup=admin_third_buttons()
                    )
                    edit_prof = dict()

        elif message.text == "Room":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL_ROOM
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "E-Mail":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL_EMAIL
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "Phone":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL_PHONE
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
    
    elif user_states[user_id] == STATE_ADMIN_EDIT_PROF_PANEL_ROOM:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_edit_prof_buttons()
            )
        else:
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            edit_prof["Room"] = message.text
            bot.send_message(
                user_id,
                "شماره اتاق استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_edit_prof_buttons()
            )

    elif user_states[user_id] == STATE_ADMIN_EDIT_PROF_PANEL_EMAIL:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_edit_prof_buttons()
            )
        else:
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            edit_prof["E-Mail"] = message.text
            bot.send_message(
                user_id,
                "ایمیل استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_edit_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_EDIT_PROF_PANEL_PHONE:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_edit_prof_buttons()
            )
        else:
            user_states[user_id] = STATE_ADMIN_EDIT_PROF_PANEL
            edit_prof["Phone"] = message.text
            bot.send_message(
                user_id,
                "شماره تلفن استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_edit_prof_buttons()
            )

    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL:
        if message.text == "بازگشت":
            user_states[user_id] = STATE_ADMIN_SECOND_PANEL
            bot.send_message(
                user_id,
                "میتوانید برای تغییر اطلاعات استاد موجود در دیتابیس، آیدی ایشان را وارد نمایید و یا یکی از گزینه های زیر را انتخاب:",
                reply_markup=admin_second_buttons()
            )
        elif message.text == "Name":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_NAME
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "Room":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_ROOM
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "E-Mail":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_EMAIL    
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "Phone":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_PHONE
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "Fax":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_FAX
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "web":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_WEB
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "pic":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_PIC
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "Department":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_DEPARTMENT
            bot.send_message(
                user_id,
                """نام دانشکده استاد مورد نظر را به درستی از لیست زیر کپی کرده و بفرستید:\n`فیزیک`\n\
`علوم ریاضی`\n`شیمی`\n`مرکز زبان‌ها و زبان‌شناسی`\n`مرکز معارف اسلامی و علوم انسانی`\n\
`مهندسی برق`\n`مهندسی مکانیک`\n`گروه فلسفه علم`\n`مهندسی انرژی`\n`مهندسی صنایع`\n\
`مدیریت و اقتصاد`\n`مهندسی کامپیوتر`\n`مهندسی هوافضا`\n`مهندسی و علم مواد`\n\
`مهندسی عمران`\n`مهندسی شیمی و نفت`\n`مرکز آموزش مهارت‌های مهندسی`""",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر"),
                parse_mode="markdown"
            )
        elif message.text == "Position":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL_POSITION
            bot.send_message(
                user_id,
                "اطلاعات مورد نظر را وارد کنید:",
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("بازگشت بدون تغییر")
            )
        elif message.text == "تمام":
            Found_now = False
            for dep in json_litle_data:
                if json_litle_data[dep][-1]["Department"] == new_prof["Department"]:
                    constant_dep = dep
                    new_prof["ID"] = json_litle_data[dep][-1]["ID"] + 1
                    litle_data_new_prof = {"ID":new_prof["ID"],"Department":new_prof["Department"],"Name":new_prof["Name"]}
                    # add prof to little json data
                    json_litle_data[dep].append(litle_data_new_prof)
                    Found_now = True
                    break
            # add prof to big json data
            del new_prof["Department"]
            json_big_data[constant_dep].append(new_prof)
            if Found_now:
                user_states[user_id] = STATE_ADMIN_SECOND_PANEL
                bot.send_message(
                    user_id,
                    f"استاد مورد نظر با موفقیت لیست اساتید دانشکده {new_prof['Department']} اضافه شد.\nبه پنل قبلی برگشتید.",
                    reply_markup=admin_second_buttons(),
                    parse_mode="markdown"
                )
                ########################
                # update big-json file
                updated_json = json.dumps(json_big_data, indent=4)
                repo.update_file(
                    path=BIG_JSON_FILE_PATH,
                    message="Updated json file from sharif-hub",
                    content=updated_json,
                    sha=big_data_content.sha
                )
                # update little-json file
                updated_json = json.dumps(json_litle_data, indent=4)
                repo.update_file(
                    path=LITLE_JSON_FILE_PATH,
                    message="Updated json file from sharif-hub",
                    content=updated_json,
                    sha=litle_data_content.sha
                )
                ########################
                new_prof = dict()
            else:
                user_states[user_id] = STATE_ADMIN_SECOND_PANEL
                bot.send_message(
                    user_id,
                    "دانشکده و مرکزی با این نام پیدا نشد.\nبه پنل قبلی برگشتید.\nمیتوانید برای تغییر اطلاعات استاد موجود در دیتابیس، آیدی ایشان را وارد نمایید و یا یکی از گزینه های زیر را انتخاب:",
                    reply_markup=admin_second_buttons()
                )
                new_prof = dict()

    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_NAME:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["Name"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "نام استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )

    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_ROOM:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["Room"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "شماره اتاق استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )

    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_EMAIL:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["E-Mail"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "آدرس ایمیل استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_PHONE:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["Phone"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "شماره تلفن استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_FAX:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["Fax"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "فکس استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_WEB:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["web"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "آدرس صفحه شخصی استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_PIC:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["pic"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "آدرس عکس استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_DEPARTMENT:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["Department"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "نام دانشکده استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
    elif user_states[user_id] == STATE_ADMIN_NEW_PROF_PANEL_POSITION:
        if message.text == "بازگشت بدون تغییر":
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "با استفاده از دکمه های زیر، اطلاعات استاد مورد نظر را وارد کنید.",
                reply_markup=admin_new_prof_buttons()
            )
        else:
            new_prof["Position"] = message.text
            user_states[user_id] = STATE_ADMIN_NEW_PROF_PANEL
            bot.send_message(
                user_id,
                "سمت استاد در حافظه ذخیره شد، اطلاعات دیگر را وارد نمایید و یا روی دکمه تمام بزنید",
                reply_markup=admin_new_prof_buttons()
            )
        

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    name = call.data
    for department, department_data in json_litle_data.items():
        for person in department_data:
            if name == person['Name']:
                person_id = person['ID']
                department_secondary_data = json_big_data.get(department, [])
                for secondary_person in department_secondary_data:
                    if secondary_person.get('ID') == person_id:
                        info_str = "\n".join([f"*{key}*: `{value}`" for key, value in secondary_person.items() if key != 'pic' and key != 'ID' and key != 'web'])
                        if 'web' in secondary_person:
                            info_str += '\n*personal page*: ' + f"[link]({secondary_person['web']})"
                        info_str += "\n*Department*: "
                        info_str += person['Department']
                        if secondary_person.get('pic') != None:
                            bot.send_photo(call.message.chat.id, secondary_person.get('pic'), info_str, parse_mode="markdown")
                        else:
                            bot.send_message(call.message.chat.id, info_str, parse_mode="markdown")
                        break

bot.infinity_polling()

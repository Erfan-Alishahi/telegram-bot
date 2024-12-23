
import os
import telebot
import requests
import json
from fuzzywuzzy import fuzz
from telebot import types
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()
# Load the API token securely from an environment variable
API_TOKEN = "7055613975:AAFYOluPx0WUoAKhv_2Ft334fnsu9x9ei1A"
bot = telebot.TeleBot(API_TOKEN)
# Securely load the API token and admin credentials from environment variables
ADMIN_CHAT_ID = ""  # Should be a string
ADMIN_USERNAME = "test"
ADMIN_PASSWORD = "1234"

if not all([API_TOKEN, ADMIN_CHAT_ID, ADMIN_USERNAME, ADMIN_PASSWORD]):
    raise Exception("Please set TELEGRAM_API_TOKEN, ADMIN_CHAT_ID, ADMIN_USERNAME, and ADMIN_PASSWORD environment variables.")

bot = telebot.TeleBot(API_TOKEN)

# Load the primary JSON data
PRIMARY_DATA_URL = "https://raw.githubusercontent.com/Erfan-Alishahi/database/main/secondary-database.json"
response_primary = requests.get(PRIMARY_DATA_URL)
if response_primary.status_code == 200:
    primary_data = response_primary.json()
else:
    raise Exception("Could not retrieve data from the primary URL")

# Load the secondary JSON data
with open('data-bot.json', 'r', encoding='utf-8') as jsn:
    secondary_data = json.load(jsn)

# State management for users
user_states = {}

# Admin authentication state
admin_authenticated = False

# Admin session state
admin_session = {}

# Function to find similar names (partial match)
def find_similar_names_partial(name):
    matches = []
    name_parts = name.split(" ")
    for department_data in primary_data.values():
        for person in department_data:
            for na in name_parts:
                if na.lower() in person['Name'].lower():
                    matches.append((person['Name'], person["Department"]))
    return list(set(matches))

# Function to find similar names (fuzzy match)
def find_similar_names_fuzzy(name):
    matches = []
    for department_data in primary_data.values():
        for person in department_data:
            similarity_ratio = fuzz.ratio(name, person['Name'])
            if similarity_ratio >= 51:
                matches.append((person['Name'], person['Department']))
    return matches

# Function to send admin a message
def send_to_admin(message):
    bot.send_message(ADMIN_CHAT_ID, message)

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
سلام دوست عزیز، به بات ما خوش آمدید!
برای پیدا کردن اطلاعات استاد مورد نظر، کافیست نام وی را به فارسی وارد کنید.
در صورتی که نام را به درستی ندانید، می‌توانید تقریبا مشابه نام را وارد کنید و بات تلاش خواهد کرد تا نام متناظر را پیدا کند.
"""
    bot.send_message(message.chat.id, welcome_text)

# Handle text messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    global admin_authenticated

    user_id = message.from_user.id
    text = message.text.strip()

    # Check if the message is the hidden admin keyword
    if text.lower() == "itsmeimback" and str(user_id) == ADMIN_CHAT_ID:
        # Initiate admin login
        user_states[user_id] = {'state': 'admin_login_username'}
        bot.send_message(user_id, "لطفاً نام کاربری خود را وارد کنید:")
        return

    # Check if user is in a specific state
    if user_id in user_states:
        state = user_states[user_id].get('state')

        if state == 'contact_admin':
            # Forward the message to admin
            send_to_admin(f"پیام از کاربر @{message.from_user.username} (ID: {user_id}):\n{text}")
            bot.send_message(user_id, "پیام شما به مدیر ارسال شد. متشکریم!")
            del user_states[user_id]
            return

        elif state == 'revision_id':
            # Save the ID and ask for revision message
            try:
                prof_id = int(text)
                user_states[user_id]['prof_id'] = prof_id
                user_states[user_id]['state'] = 'revision_message'
                bot.send_message(user_id, "لطفاً متن بازنگری مورد نظر خود را ارسال کنید:")
            except ValueError:
                bot.send_message(user_id, "لطفاً یک شماره ID معتبر وارد کنید:")
            return

        elif state == 'revision_message':
            # Save the revision message and forward to admin
            prof_id = user_states[user_id].get('prof_id')
            revision_text = text
            send_to_admin(f"درخواست بازنگری:\nID استاد: {prof_id}\nپیام: {revision_text}\nاز طرف کاربر @{message.from_user.username} (ID: {user_id})")
            bot.send_message(user_id, "درخواست بازنگری شما به مدیر ارسال شد. متشکریم!")
            del user_states[user_id]
            return

        elif state == 'admin_login_username':
            # Save the username and ask for password
            entered_username = text
            user_states[user_id]['entered_username'] = entered_username
            user_states[user_id]['state'] = 'admin_login_password'
            bot.send_message(user_id, "لطفاً رمز عبور خود را وارد کنید:")
            return

        elif state == 'admin_login_password':
            # Verify password
            entered_password = text
            entered_username = user_states[user_id].get('entered_username')

            if entered_username == ADMIN_USERNAME and entered_password == ADMIN_PASSWORD:
                admin_authenticated = True
                admin_session[user_id] = True
                bot.send_message(user_id, "ورود موفقیت‌آمیز! به پنل مدیریت خوش آمدید.", reply_markup=admin_panel_keyboard())
                del user_states[user_id]
            else:
                bot.send_message(user_id, "نام کاربری یا رمز عبور اشتباه است. دوباره تلاش کنید.")
                del user_states[user_id]
            return

        elif state == 'admin_edit_id':
            # Admin is providing the ID to edit
            try:
                prof_id = int(text)
                user_states[user_id]['edit_prof_id'] = prof_id
                user_states[user_id]['state'] = 'admin_edit_field'
                bot.send_message(user_id, "لطفاً نام فیلدی که می‌خواهید ویرایش کنید را وارد کنید (مثلاً Name, Room, Phone, etc.):")
            except ValueError:
                bot.send_message(user_id, "لطفاً یک شماره ID معتبر وارد کنید:")
            return

        elif state == 'admin_edit_field':
            # Admin is providing the field to edit
            field = text
            user_states[user_id]['edit_field'] = field
            user_states[user_id]['state'] = 'admin_edit_value'
            bot.send_message(user_id, "لطفاً مقدار جدید را وارد کنید:")
            return

        elif state == 'admin_edit_value':
            # Admin is providing the new value
            new_value = text
            prof_id = user_states[user_id].get('edit_prof_id')
            field = user_states[user_id].get('edit_field')

            # Find and update the professor in secondary_data
            updated = False
            for department, dept_data in secondary_data.items():
                for person in dept_data:
                    if person.get('ID') == prof_id:
                        if field in person:
                            person[field] = new_value
                            updated = True
                            break
                if updated:
                    break

            if updated:
                # Save the updated secondary_data to the JSON file
                with open('data-bot.json', 'w', encoding='utf-8') as jsn:
                    json.dump(secondary_data, jsn, ensure_ascii=False, indent=4)
                bot.send_message(user_id, f"فیلد `{field}` برای استاد با ID {prof_id} به `{new_value}` تغییر یافت.")
            else:
                bot.send_message(user_id, f"استادی با ID {prof_id} یافت نشد یا فیلد `{field}` نامعتبر است.")
            
            # Return to admin panel
            bot.send_message(user_id, "برای ادامه از پنل مدیریت استفاده کنید.", reply_markup=admin_panel_keyboard())
            del user_states[user_id]
            return

    # If not in any specific state, proceed with normal message handling
    name = text

    found = False
    for department, department_data in primary_data.items():
        for person in department_data:
            if name == person['Name']:
                found = True
                person_id = person['ID']
                department_secondary_data = secondary_data.get(department, [])
                for secondary_person in department_secondary_data:
                    if secondary_person.get('ID') == person_id:
                        info_lines = [
                            f"*Name*: `{secondary_person.get('Name', '')}`",
                            f"*Room*: `{secondary_person.get('Room', '')}`",
                            f"*P.O.Box*: `{secondary_person.get('P.O.Box', '')}`",
                            f"*Phone*: `{secondary_person.get('Phone', '')}`",
                            f"*Fax*: `{secondary_person.get('Fax', '')}`",
                            f"*E-Mail*: `{secondary_person.get('E-Mail', '')}`",
                            f"*Position*: `{secondary_person.get('Position', '')}`",
                            f"*ID*: `{secondary_person.get('ID', '')}`"
                        ]
                        if 'web' in secondary_person:
                            info_lines.append(f"*Personal Page*: [Link]({secondary_person['web']})")
                        info_lines.append(f"*Department*: {person['Department']}")
                        info_str = "\n".join(info_lines)
                        
                        # Create inline keyboard
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        contact_button = types.InlineKeyboardButton("Contact Admin", callback_data="contact_admin")
                        revision_button = types.InlineKeyboardButton("Revision", callback_data="revision")
                        keyboard.add(contact_button, revision_button)
                        
                        bot.send_photo(
                            message.chat.id,
                            secondary_person.get('pic'),
                            info_str,
                            parse_mode="markdown",
                            reply_markup=keyboard
                        )
                        break
                break
        if found:
            break

    if not found:
        # Attempt to find similar names
        similar_names = find_similar_names_partial(name)
        if similar_names:
            # Create an inline keyboard with similar names
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for f in similar_names:
                button_text = f"{f[0]} - دانشکده: {f[1]}"
                button = types.InlineKeyboardButton(button_text, callback_data=f[0])
                keyboard.add(button)
            bot.send_message(message.chat.id, "استاد مورد نظر یافت نشد. لطفاً از لیست پیشنهادی زیر انتخاب کنید:", reply_markup=keyboard)
            return
        else:
            similar_names = find_similar_names_fuzzy(name)
            if similar_names:
                # Create an inline keyboard with similar names
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                for f in similar_names:
                    button_text = f"{f[0]} - دانشکده: {f[1]}"
                    button = types.InlineKeyboardButton(button_text, callback_data=f[0])
                    keyboard.add(button)
                bot.send_message(message.chat.id, "استاد مورد نظر یافت نشد. لطفاً از لیست پیشنهادی زیر انتخاب کنید:", reply_markup=keyboard)
                return

        # If still not found
        bot.send_message(message.chat.id, "متاسفانه اطلاعاتی در مورد این استاد یافت نشد.")

# Handle callback queries from inline buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    user_id = call.from_user.id

    if data == "contact_admin":
        # Set state to contact_admin
        user_states[user_id] = {'state': 'contact_admin'}
        bot.send_message(user_id, "لطفاً پیام خود را برای مدیر ارسال کنید:")
    
    elif data == "revision":
        # Set state to revision_id
        user_states[user_id] = {'state': 'revision_id'}
        bot.send_message(user_id, "لطفاً ID استاد مورد نظر را وارد کنید:")
    
    else:
        # Assume data is a professor's name from similar names
        name = data
        found = False
        for department, department_data in primary_data.items():
            for person in department_data:
                if name == person['Name']:
                    found = True
                    person_id = person['ID']
                    department_secondary_data = secondary_data.get(department, [])
                    for secondary_person in department_secondary_data:
                        if secondary_person.get('ID') == person_id:
                            info_lines = [
                                f"*Name*: `{secondary_person.get('Name', '')}`",
                                f"*Room*: `{secondary_person.get('Room', '')}`",
                                f"*P.O.Box*: `{secondary_person.get('P.O.Box', '')}`",
                                f"*Phone*: `{secondary_person.get('Phone', '')}`",
                                f"*Fax*: `{secondary_person.get('Fax', '')}`",
                                f"*E-Mail*: `{secondary_person.get('E-Mail', '')}`",
                                f"*Position*: `{secondary_person.get('Position', '')}`",
                                f"*ID*: `{secondary_person.get('ID', '')}`"
                            ]
                            if 'web' in secondary_person:
                                info_lines.append(f"*Personal Page*: [Link]({secondary_person['web']})")
                            info_lines.append(f"*Department*: {person['Department']}")
                            info_str = "\n".join(info_lines)
                            
                            # Create inline keyboard
                            keyboard = types.InlineKeyboardMarkup(row_width=2)
                            contact_button = types.InlineKeyboardButton("Contact Admin", callback_data="contact_admin")
                            revision_button = types.InlineKeyboardButton("Revision", callback_data="revision")
                            keyboard.add(contact_button, revision_button)
                            
                            bot.send_photo(
                                call.message.chat.id,
                                secondary_person.get('pic'),
                                info_str,
                                parse_mode="markdown",
                                reply_markup=keyboard
                            )
                            break
                    break
            if found:
                break
        if not found:
            bot.send_message(call.message.chat.id, "اطلاعات مربوط به این استاد یافت نشد.")

    bot.answer_callback_query(call.id)

# Admin panel inline keyboard
def admin_panel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    edit_button = types.KeyboardButton("ویرایش اطلاعات استاد")
    logout_button = types.KeyboardButton("خروج از پنل مدیریت")
    keyboard.add(edit_button, logout_button)
    return keyboard

# Handle admin panel actions
@bot.message_handler(func=lambda message: message.text in ["ویرایش اطلاعات استاد", "خروج از پنل مدیریت"])
def admin_panel_actions(message):
    global admin_authenticated
    user_id = message.from_user.id

    if user_id not in admin_session or not admin_session.get(user_id):
        bot.send_message(user_id, "شما وارد پنل مدیریت نشده‌اید.")
        return

    if message.text == "ویرایش اطلاعات استاد":
        user_states[user_id] = {'state': 'admin_edit_id'}
        bot.send_message(user_id, "لطفاً ID استاد مورد نظر برای ویرایش را وارد کنید:")
    
    elif message.text == "خروج از پنل مدیریت":
        admin_session[user_id] = False
        bot.send_message(user_id, "از پنل مدیریت خارج شدید.", reply_markup=types.ReplyKeyboardRemove())

# Handle admin editing steps
@bot.message_handler(func=lambda message: True, content_types=['text'])
def admin_edit_handler(message):
    global admin_authenticated
    user_id = message.from_user.id
    text = message.text.strip()

    # This handler is redundant as admin_panel_actions handles specific texts
    pass  # Placeholder in case additional admin actions are needed

# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

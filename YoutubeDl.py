
import telebot
from telebot.types import LinkPreviewOptions

import requests 
import sqlite3
import time



with sqlite3.connect('user_Db.db') as connection:
    curser = connection.cursor()
    create_table = """
    CREATE TABLE IF NOT EXISTS users(
        Chat_id integer primary key,
        first_name text,
        last_name text,
        phone_number text,
        Download integer
    );
"""

    curser.execute(create_table)


KeyBoard_Markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True , row_width=2) # منو ربات 
contact = telebot.types.KeyboardButton("تایید شماره تماس📞" , request_contact=True)
KeyBoard_Markup.add("ارسال لینک ویدیو❤️:","آموزش های ما📖:",contact) #لیست منو های ربات


Ads = "🛑🛑\nبرای استفاده با بالاترین کیفیت موجود باید صدا و فیلم به صورت جدا دانلود شود و سپس در اندروید نرم افزار MxPalyer یا در کامپیوتر با نرمافزار KMPlayer صدا به تصویر اضافه شود🛑🛑"
Learn = "برای دریافت آموزش تصویری روی دکمه آموزش کلیک کنید."


Download_Video_Ads = telebot.types.InlineKeyboardButton("درحال ارسال مدیا... 🚀",callback_data="Paycheck")
Download_Video_Ads_Markup = telebot.types.InlineKeyboardMarkup()
Download_Video_Ads_Markup.add(Download_Video_Ads)


Select_Type_File = telebot.types.InlineKeyboardButton("ویدیو",callback_data="Video")
Select_Type_File1 = telebot.types.InlineKeyboardButton("صدا",callback_data="Sound")
Select_Type_File_Markup = telebot.types.InlineKeyboardMarkup()
Select_Type_File_Markup.add(Select_Type_File,Select_Type_File1)


Select_Type_video = telebot.types.InlineKeyboardButton("1080px",callback_data="1080")
Select_Type_video1= telebot.types.InlineKeyboardButton("720px",callback_data="720")
Select_Type_video2 = telebot.types.InlineKeyboardButton("480px",callback_data="480")

Select_Type_video_Markup = telebot.types.InlineKeyboardMarkup()
Select_Type_video_Markup.add(Select_Type_video,Select_Type_video1,Select_Type_video2)


Select_Type_learn1= telebot.types.InlineKeyboardButton("اندروید📱",callback_data="Android")
Select_Type_learn2 = telebot.types.InlineKeyboardButton("Pc🖥",callback_data="Pc")

Select_Type_learn_Markup = telebot.types.InlineKeyboardMarkup()
Select_Type_learn_Markup.add(Select_Type_learn1,Select_Type_learn2)


Token = "YOUR BOT TOKEN" #توکن ربات بزن
OneApiToken = "OneApiToken"  #برو تو سایت one-api.ir
Bot = telebot.TeleBot(Token)

@Bot.message_handler(commands=['start'])
def start(message):
        
        
          Bot.send_message(message.chat.id , "خوش اومدین به ربات دانلودر یوتوب روشاک 🚀" , reply_markup=KeyBoard_Markup)
          Bot.send_message(message.chat.id , "برای ادامه کار لطفا شماره موبایل و اطلاعات خود را تایید کنید" , reply_markup=KeyBoard_Markup)
        
@Bot.message_handler(content_types=['contact'])
def Keyboard(message):
   Bot.send_message(message.chat.id,"اطلاعات شما تایید شد.")
   
   
   with sqlite3.connect('user_Db.db') as connection:
        curser = connection.cursor()
        insert_data_query = """
        INSERT INTO users (Chat_id , first_name, last_name , phone_number , Download)
        VALUES (?, ?, ?, ?, ?)
"""

        data = (
             message.contact.user_id,
             f'{message.contact.first_name}',
             f'{message.contact.last_name}',
             f'{message.contact.phone_number}',
             0
        )
        curser.execute(insert_data_query,data)
@Bot.message_handler()
def send_link(message):
    if message.text == "ارسال لینک ویدیو❤️:":
        Bot.send_message(message.chat.id,"لطفا لینک ویدیو یوتوب را ارسال کنید: " )
        Bot.register_next_step_handler(message,recive_video_link)
    elif message.text == "آموزش های ما📖:":
        Bot.send_message(message.chat.id,"در کدام پلتفرم ویدیو را نگاه میکنید؟ ", reply_markup=Select_Type_learn_Markup)
        
             

def recive_video_link(message):
     name = message.text
     Bot.send_message(message.chat.id,"لطفا کیفیت مدیا را انتخاب کنید❤️: " , reply_markup=Select_Type_video_Markup)
#      Bot.send_chat_action(message.chat.id,"upload_video")
#      Bot.send_message(message.chat.id,Ads,reply_markup=Download_Video_Ads_Markup)
     global link
     link = name
@Bot.callback_query_handler(func=lambda call:True)
def callback(call):
     if call.data == "Video":
          Bot.send_message(call.message.chat.id,"لطفا کیفیت فیلم را انتخاب کنید❤️: ",reply_markup=Select_Type_video_Markup)
     
     elif call.data == "1080":
          Bot.send_message(call.message.chat.id,Ads,reply_markup=Download_Video_Ads_Markup)
          Url = f"https://one-api.ir/youtube/?token={OneApiToken}&action=getvideoid&link={link}"
          respons = requests.get(Url)
          Video_Id = respons.json()['result']
          Url = f"https://youtube.one-api.ir/?token={OneApiToken}&action=fullvideo&id={Video_Id}"
          respons = requests.get(Url)
          Data =respons.json()['result']['formats']
          Video = []
          resu = []
          Sound = []
          title = respons.json()['result']['title']
          Description = respons.json()['result']['description']
          Channel_Url = respons.json()['result']['channel_url']
          Tumbnail = respons.json()['result']['thumbnail']
          for Video1 in Data:
               if Video1['resolution'] == "1920x1080" :
                    if Video1['video_ext'] == "mp4":
                         Video.append(Video1['id'])
                         resu.append(Video1['resolution'])
          for Sound1 in Data:
               if Sound1['format_note'] == "medium" :
                    if Sound1['audio_ext'] == "m4a":
                         Sound.append(Sound1['id'])
          Url_Video = f"https://youtube.one-api.ir/?token={OneApiToken}&action=download&id={Video[0]}"
          respons_Video = requests.get(Url_Video)
          Video_Url = respons_Video.json()['result']['link']
          Url_Sound = f"https://youtube.one-api.ir/?token={OneApiToken}&action=download&id={Sound[0]}"
          respons_Sound = requests.get(Url_Sound)
          Sound_Url = respons_Sound.json()['result']['link']
          respons_Tumbnail = requests.get(Tumbnail , allow_redirects=True)
          open(f'{Video_Id}'+'.webp', 'wb').write(respons_Tumbnail.content)
          Bot.send_photo(call.message.chat.id , open(f'{Video_Id}'+'.webp' , "rb") , f"Title: {title}\nChannel_Url: {Channel_Url}\n\n\nلینک دانلود فیلم📹: {Video_Url}\nلینک دانلود صدا🎧: {Sound_Url}\n\n\n{Ads}")
     elif call.data == "720":
          Bot.send_message(call.message.chat.id,Ads,reply_markup=Download_Video_Ads_Markup)
          Url = f"https://one-api.ir/youtube/?token={OneApiToken}&action=getvideoid&link={link}"
          respons = requests.get(Url)
          Video_Id = respons.json()['result']
          Url = f"https://youtube.one-api.ir/?token={OneApiToken}&action=fullvideo&id={Video_Id}"
          respons = requests.get(Url)
          Data =respons.json()['result']['formats']
          Video = []
          resu = []
          Sound = []
          title = respons.json()['result']['title']
          Description = respons.json()['result']['description']
          Channel_Url = respons.json()['result']['channel_url']
          Tumbnail = respons.json()['result']['thumbnail']
          for Video1 in Data:
               if Video1['resolution'] == "1280x720" :
                    if Video1['video_ext'] == "mp4":
                         Video.append(Video1['id'])
                         resu.append(Video1['resolution'])
          for Sound1 in Data:
               if Sound1['format_note'] == "medium" :
                    if Sound1['audio_ext'] == "m4a":
                         Sound.append(Sound1['id'])
          Url_Video = f"https://youtube.one-api.ir/?token={OneApiToken}&action=download&id={Video[0]}"
          respons_Video = requests.get(Url_Video)
          Video_Url = respons_Video.json()['result']['link']
          Url_Sound = f"https://youtube.one-api.ir/?token={OneApiToken}&action=download&id={Sound[0]}"
          respons_Sound = requests.get(Url_Sound)
          Sound_Url = respons_Sound.json()['result']['link']
          respons_Tumbnail = requests.get(Tumbnail , allow_redirects=True)
          open(f'{Video_Id}'+'.webp', 'wb').write(respons_Tumbnail.content)    
          Bot.send_photo(call.message.chat.id , open(f'{Video_Id}'+'.webp' , "rb") , f"Title: {title}\nChannel_Url: {Channel_Url}\n\n\nلینک دانلود فیلم📹: {Video_Url}\nلینک دانلود صدا🎧: {Sound_Url}\n\n\n{Ads}")
     elif call.data == "480":
          Bot.send_message(call.message.chat.id,Ads,reply_markup=Download_Video_Ads_Markup)
          Url = f"https://one-api.ir/youtube/?token={OneApiToken}&action=getvideoid&link={link}"
          respons = requests.get(Url)
          Video_Id = respons.json()['result']
          Url = f"https://youtube.one-api.ir/?token={OneApiToken}&action=fullvideo&id={Video_Id}"
          respons = requests.get(Url)
          Data =respons.json()['result']['formats']
          Video = []
          resu = []
          Sound = []
          title = respons.json()['result']['title']
          Description = respons.json()['result']['description']
          Channel_Url = respons.json()['result']['channel_url']
          Tumbnail = respons.json()['result']['thumbnail']
          for Video1 in Data:
               if Video1['resolution'] == "1280x720" :
                    if Video1['video_ext'] == "mp4":
                         Video.append(Video1['id'])
                         resu.append(Video1['resolution'])
          for Sound1 in Data:
               if Sound1['format_note'] == "medium" :
                    if Sound1['audio_ext'] == "m4a":
                         Sound.append(Sound1['id'])
          Url_Video = f"https://youtube.one-api.ir/?token={OneApiToken}&action=download&id={Video[0]}"
          respons_Video = requests.get(Url_Video)
          Video_Url = respons_Video.json()['result']['link']
          Url_Sound = f"https://youtube.one-api.ir/?token={OneApiToken}&action=download&id={Sound[0]}"
          respons_Sound = requests.get(Url_Sound)
          Sound_Url = respons_Sound.json()['result']['link']
          respons_Tumbnail = requests.get(Tumbnail , allow_redirects=True)
          open(f'{Video_Id}'+'.webp', 'wb').write(respons_Tumbnail.content)    
          Bot.send_photo(call.message.chat.id , open(f'{Video_Id}'+'.webp' , "rb") , f"Title: {title}\nChannel_Url: {Channel_Url}\n\n\nلینک دانلود فیلم📹: {Video_Url}\nلینک دانلود صدا🎧: {Sound_Url}\n\n\n{Ads}")
          # Bot.send_message(call.message.chat.id,"sjfbapwf",link_preview_options=LinkPreviewOptions(True,f'{Video_Url}'))
     elif call.data == "Android":
          Bot.send_photo(call.message.chat.id , open("learn_file/step-1-mobile.jpg" , "rb"),"درصورت بروز هرگونه مشکل لطفا به ایدی:\n@Roshakadmin\nمراجعه کنید")
          Bot.send_photo(call.message.chat.id , open("learn_file/step-2-mobile.jpg" , "rb"),"درصورت بروز هرگونه مشکل لطفا به ایدی:\n@Roshakadmin\nمراجعه کنید")
     elif call.data == "Pc":
          Bot.send_photo(call.message.chat.id , open("learn_file/step-1-pc.jpg" , "rb"),"درصورت بروز هرگونه مشکل لطفا به ایدی:\n@Roshakadmin\nمراجعه کنید")
          Bot.send_photo(call.message.chat.id , open("learn_file/step-2-pc.jpg" , "rb"),"درصورت بروز هرگونه مشکل لطفا به ایدی:\n@Roshakadmin\nمراجعه کنید")
Bot.infinity_polling()






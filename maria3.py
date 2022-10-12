# -*- coding: utf-8 -*-

import logging
import re
import telebot
from telebot import types
import sqlite3
import datetime
import time
import gspread
import json

bot = telebot.TeleBot('5512294752:AAG9Dbz2tjp9faIQikdkx6s_PMJwCw_jVKE')
googlesheet_id = '19LfiHjqaegmV47wqqgpuQbYaoIaMzFEekNwNSeuw5VQ'
gc = gspread.service_account(filename='maria-359514-cb22a8d7b592.json')

nameRedFoto = ''

@bot.message_handler(commands=['start'])
def start(message):
	conn = sqlite3.connect('db.db')
	cur = conn.cursor()
	cur.execute(f"""SELECT * FROM user WHERE idTeleg = '{message.from_user.id}' """)
	rows = cur.fetchall()
	if len(rows) < 1:
		now = datetime.datetime.now()
		dataOform = now.strftime("%d-%m-%Y")
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute("""INSERT INTO user(idTeleg, dataDob) VALUES ( ?, ?)""", (message.from_user.id, dataOform ))
		conn.commit()
		# bot.send_message(message.from_user.id, f'Привет! Я Мария, виртуальный помощник Babysmile Photography. \nЯ очень рада, что ты теперь с нами :)\n\nНажми кнопку Старт', parse_mode= 'HTML')
		keyboards = telebot.types.ReplyKeyboardMarkup(True)
		keyboards.row('Кто может помочь', 'Ответы на частые вопросы')
		keyboards.row('Связаться со мной')
		vakansii = types.InlineKeyboardMarkup()
		foto = types.InlineKeyboardButton(text='Фотограф', callback_data='foto')
		redFoto = types.InlineKeyboardButton(text='Редактор фотографий', callback_data='redFoto')
		# vakansii.add(foto)
		vakansii.add(redFoto)
		bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}", reply_markup=keyboards, parse_mode= 'HTML')
		bot.send_message(message.chat.id, text=f"Чтобы я могла более точно тебе помогать, выбери название своей должности из списка:", reply_markup=vakansii, parse_mode= 'HTML')
	else:
		keyboards = telebot.types.ReplyKeyboardMarkup(True)
		keyboards.row('Кто может помочь', 'Ответы на частые вопросы')
		keyboards.row('Связаться со мной')
		vakansii = types.InlineKeyboardMarkup()
		foto = types.InlineKeyboardButton(text='Фотограф', callback_data='foto')
		redFoto = types.InlineKeyboardButton(text='Редактор фотографий', callback_data='redFoto')
		# vakansii.add(foto)
		vakansii.add(redFoto)
		bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}", reply_markup=keyboards, parse_mode= 'HTML')
		bot.send_message(message.chat.id, text=f"Чтобы я могла более точно тебе помогать, выбери название своей должности из списка:", reply_markup=vakansii, parse_mode= 'HTML')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text.lower() == 'связаться со мной':
		bot.forward_message(-631332560, message.chat.id, message.message_id)
		bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} хочет чтобы с ним связались.')
		bot.send_message(message.chat.id, text=f"Я передала нашим специалистам, что с вами необходимо связаться, ожидайте", parse_mode= 'HTML')
	if message.text.lower() == 'кто может помочь':
		bot.send_message(message.chat.id, text=f"Наставник Анастасия +7 (908) 6271838 \nРуководитель службы редакторов Яна +7 (981) 4051287\nКоллеги из отдела персонала hrm@bsmile.ru", parse_mode= 'HTML')
		# bot.forward_message(-631332560, message.chat.id, message.message_id)
		# bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} нажал на кнопку "кто может помочь".')


	elif message.text.lower() == 'ответы на частые вопросы':
		bot.send_message(message.chat.id, text=f"&#8226;&#8194;<a href='https://docs.google.com/document/d/1UJLMSkxyy7MslbSwtqFpHGg8kVu5GCjUVkFlJVJN3n4/edit?usp=sharing'><b>Как заполнить договор?</b></a>\n&#8226;&#8194;<a href='https://docs.google.com/document/d/1-Yc_1PLryGD_Qd-WjlaxnOIhTqotuiH0ZwNQbUQ6Qtw/edit?usp=sharing'><b>Куда, как и когда отправить договор?</b></a>\n&#8226;&#8194;<a href='https://docs.google.com/document/d/1O9la64gMrtTU7M5N8jQRgiLlDT4KJSBsaJvlLCCPhAM/edit?usp=sharing'><b>Где найти шаблон договора?</b></a>\n&#8226;&#8194;<a href='https://docs.google.com/document/d/1KnIw5BbF2kyWJSaDRbPVexaJWVt1XO7ekEB1dC1BwM4/edit?usp=sharing'><b>Где посмотреть стоимость работ?</b></a>\n&#8226;&#8194;<a href='https://docs.google.com/document/d/1KnIw5BbF2kyWJSaDRbPVexaJWVt1XO7ekEB1dC1BwM4/edit?usp=sharing'><b>Где посмотреть начисленную оплату?</b></a>\n&#8226;&#8194;<a href='https://docs.google.com/document/d/1-GNasmb8RoMKaE1w1bzKCvDxjAChQpP_3Wzf3sFuuBg/edit?usp=sharing'><b>В какие даты проводятся выплаты?</b></a>\n&#8226;&#8194;<a href='https://docs.google.com/document/d/1jbXM4jQ9m7fewtQmAD-wOnDA8tVbT29wE933OJj533A/edit?usp=sharing'><b>Зачем подключать сервис “Свое дело” в Сбербанк онлайн?</b></a>\n&#8226;&#8194;<a href='https://disk.yandex.ru/i/AvYjaVflCxuGpw'><b>С чего начать работу редактору?</b></a>", disable_web_page_preview = True, parse_mode= 'HTML')

	# elif message.text.lower() == 'привет':
	# 	bot.send_message(message.chat.id, text=f"", parse_mode= 'HTML')

	if 'привет!' in message.text.lower():
		bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}! Хорошего дня.", parse_mode= 'HTML')

	elif 'привет' in message.text.lower():
		bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}! Хорошего дня.", parse_mode= 'HTML')

	if 'помощь' in message.text.lower():
		bot.forward_message(-631332560, message.chat.id, message.message_id)
		bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} нужна помощь')
		bot.send_message(message.chat.id, text=f"Скорее жми внизу кнопку “Кто может помочь” или кнопку “Связаться со мной”", parse_mode= 'HTML')

	if 'помощ' in message.text.lower():
		bot.forward_message(-631332560, message.chat.id, message.message_id)
		bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} нужна помощь')
		bot.send_message(message.chat.id, text=f"Скорее жми внизу кнопку “Кто может помочь” или кнопку “Связаться со мной”", parse_mode= 'HTML')

	if 'помочь' in message.text.lower():
		bot.forward_message(-631332560, message.chat.id, message.message_id)
		bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} нужна помощь')
		bot.send_message(message.chat.id, text=f"Скорее жми внизу кнопку “Кто может помочь” или кнопку “Связаться со мной”", parse_mode= 'HTML')

	if 'помогите' in message.text.lower():
		bot.forward_message(-631332560, message.chat.id, message.message_id)
		bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} нужна помощь')
		bot.send_message(message.chat.id, text=f"Скорее жми внизу кнопку “Кто может помочь” или кнопку “Связаться со мной”", parse_mode= 'HTML')

	if 'как дела?' in message.text.lower():
		bot.send_message(message.chat.id, text=f"Замечательно!  Очень надеюсь, у тебя такой же классный день😉", parse_mode= 'HTML')
	elif 'как дела' in message.text.lower():
		bot.send_message(message.chat.id, text=f"Замечательно!  Очень надеюсь, у тебя такой же классный день😉", parse_mode= 'HTML')
	elif '?' in message.text.lower():
		bot.forward_message(-631332560, message.chat.id, message.message_id)
		bot.send_message(-631332560, f'{message.from_user.first_name} {message.from_user.last_name} задал вопрос в боте')
		bot.send_message(message.chat.id, text=f"Хороший вопрос 👍 Я передала его коллегам, которые свяжутся с тобой и обязательно помогут 😀", parse_mode= 'HTML')
	if 'привет' not in message.text.lower() and 'привет!' not in message.text.lower() and 'помощь' not in message.text.lower() and 'как дела?' not in message.text.lower() and 'как дела' not in message.text.lower() and '?' not in message.text.lower() and 'ответы на частые вопросы' not in message.text.lower() and 'кто может помочь' not in message.text.lower() and 'помощ' not in message.text.lower() and 'помогите' not in message.text.lower() and 'связаться со мной' not in message.text.lower()  and 'помочь' not in message.text.lower():
		bot.send_message(message.chat.id, text=f"Похоже у тебя отличное воображение 😉 Мы ценим творческих людей и рады, что и ты с нами!😁 ", parse_mode= 'HTML')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
# ========================================РЕДАКТОРЫ ФОТОГРАФИЙ==========================================
	if call.data == 'redFoto':
		# bot.delete_message(call.message.chat.id, call.message.message_id)
		onlineOfflineRedfoto = types.InlineKeyboardMarkup()
		onlineRedFoto = types.InlineKeyboardButton(text='🎓ЗАПИСАТЬСЯ НА ОНЛАЙН ЗАНЯТИЯ', callback_data='onlineRedFoto')
		offlineRedFoto = types.InlineKeyboardButton(text='🎓ТЕМЫ ДЛЯ САМОСТОЯТЕЛЬНОГО ИЗУЧЕНИЯ:', callback_data='offlineRedFoto')
		onlineOfflineRedfoto.add(onlineRedFoto)

		bot.send_message(call.message.chat.id, text=f"👌Отлично, приглашаю тебя на небольшое обучение, которое позволит максимально быстро войти в работу и познакомиться с нашими стандартами.\nТебя ждут 3 онлайн занятия и 4 темы для самостоятельного изучения.\nТакже я добавлю тебя в чат с наставником и другими учениками.\n\nЖелаю успехов! 😄", reply_markup=onlineOfflineRedfoto, parse_mode= 'HTML')

	if call.data == 'onlineRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1StandartRabotyPSRedFoto = sh.sheet1.get('B3')
		week2StandartRabotyPSRedFoto = sh.sheet1.get('C3')
		dataStandartRabotyPSRedFoto = types.InlineKeyboardMarkup()
		dataWeek1StandartRabotyPSRedFoto = types.InlineKeyboardButton(text=week1StandartRabotyPSRedFoto[0][0], callback_data='dataWeek1StandartRabotyPSRedFoto')
		dataWeek2StandartRabotyPSRedFoto = types.InlineKeyboardButton(text=week2StandartRabotyPSRedFoto[0][0], callback_data='dataWeek2StandartRabotyPSRedFoto')
		dataStandartRabotyPSRedFoto.add(dataWeek1StandartRabotyPSRedFoto)
		dataStandartRabotyPSRedFoto.add( dataWeek2StandartRabotyPSRedFoto)
		bot.send_message(call.message.chat.id, text=f"Выбери удобную дату и время, чтобы пройти урок “Стандарты работы в PS (ретушь)”", reply_markup=dataStandartRabotyPSRedFoto, parse_mode= 'HTML')


	if call.data == 'dataWeek1StandartRabotyPSRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1StandartRabotyPSRedFoto = sh.sheet1.get('B3')
		dataStandartRabotyPSRedFoto = week1StandartRabotyPSRedFoto[0][0]
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET urok1 = '{dataStandartRabotyPSRedFoto}' WHERE idTeleg = '{call.from_user.id}'""")
		# cur.execute("""UPDATE user SET urok1 = ? WHERE idTeleg = ?""", (dataStandartRabotyPSRedFoto, call.message.from_user.id))
		conn.commit()

		week1SborkaKomplektaPremiumRedFoto = sh.sheet1.get('B2')
		week2SborkaKomplektaPremiumRedFoto = sh.sheet1.get('C2')
		dataSborkaKomplektaPremiumRedFoto = types.InlineKeyboardMarkup()
		dataWeek1SborkaKomplektaPremiumRedFoto = types.InlineKeyboardButton(text=week1SborkaKomplektaPremiumRedFoto[0][0], callback_data='dataWeek1SborkaKomplektaPremiumRedFoto')
		dataWeek2SborkaKomplektaPremiumRedFoto = types.InlineKeyboardButton(text=week2SborkaKomplektaPremiumRedFoto[0][0], callback_data='dataWeek2SborkaKomplektaPremiumRedFoto')
		dataSborkaKomplektaPremiumRedFoto.add(dataWeek1SborkaKomplektaPremiumRedFoto)
		dataSborkaKomplektaPremiumRedFoto.add(dataWeek2SborkaKomplektaPremiumRedFoto)
		bot.send_message(call.message.chat.id, text=f'Выбери удобную дату и время, чтобы пройти урок “PS: сборка комплекта Премиум”', reply_markup=dataSborkaKomplektaPremiumRedFoto, parse_mode= 'HTML')
	if call.data == 'dataWeek2StandartRabotyPSRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1StandartRabotyPSRedFoto = sh.sheet1.get('C3')
		dataStandartRabotyPSRedFoto = week1StandartRabotyPSRedFoto[0][0]
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET urok1 = '{dataStandartRabotyPSRedFoto}' WHERE idTeleg = '{call.from_user.id}'""")
		# cur.execute("""UPDATE user SET urok1 = ? WHERE idTeleg = ?""", (dataStandartRabotyPSRedFoto, call.message.from_user.id))
		conn.commit()
		week1SborkaKomplektaPremiumRedFoto = sh.sheet1.get('B2')
		week2SborkaKomplektaPremiumRedFoto = sh.sheet1.get('C2')
		dataSborkaKomplektaPremiumRedFoto = types.InlineKeyboardMarkup()
		dataWeek1SborkaKomplektaPremiumRedFoto = types.InlineKeyboardButton(text=week1SborkaKomplektaPremiumRedFoto[0][0], callback_data='dataWeek1SborkaKomplektaPremiumRedFoto')
		dataWeek2SborkaKomplektaPremiumRedFoto = types.InlineKeyboardButton(text=week2SborkaKomplektaPremiumRedFoto[0][0], callback_data='dataWeek2SborkaKomplektaPremiumRedFoto')
		dataSborkaKomplektaPremiumRedFoto.add(dataWeek1SborkaKomplektaPremiumRedFoto)
		dataSborkaKomplektaPremiumRedFoto.add(dataWeek2SborkaKomplektaPremiumRedFoto)
		bot.send_message(call.message.chat.id, text=f'Выбери удобную дату и время, чтобы пройти урок “PS: сборка комплекта Премиум”', reply_markup=dataSborkaKomplektaPremiumRedFoto, parse_mode= 'HTML')
# =====================================================

	if call.data == 'dataWeek1SborkaKomplektaPremiumRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1SborkaKomplektaPremiumRedFoto = sh.sheet1.get('B2')
		dataSborkaKomplektaPremiumRedFoto = week1SborkaKomplektaPremiumRedFoto[0][0]
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET urok2 = '{dataSborkaKomplektaPremiumRedFoto}' WHERE idTeleg = '{call.from_user.id}'""")
		# cur.execute("""UPDATE user SET urok1 = ? WHERE idTeleg = ?""", (dataStandartRabotyPSRedFoto, call.message.from_user.id))
		conn.commit()
		week1RabotaNadOshcibkamiObrabotkiRedFoto = sh.sheet1.get('B4')
		week2RabotaNadOshcibkamiObrabotkiRedFoto = sh.sheet1.get('C4')
		dataRabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardMarkup()
		dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardButton(text=week1RabotaNadOshcibkamiObrabotkiRedFoto[0][0], callback_data='dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto')
		dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardButton(text=week2RabotaNadOshcibkamiObrabotkiRedFoto[0][0], callback_data='dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto')
		dataRabotaNadOshcibkamiObrabotkiRedFoto.add(dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto)
		dataRabotaNadOshcibkamiObrabotkiRedFoto.add(dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto)
		bot.send_message(call.message.chat.id, text=f'Выбери удобную дату и время, чтобы пройти урок “Работа над ошибками обработки”', reply_markup=dataRabotaNadOshcibkamiObrabotkiRedFoto, parse_mode= 'HTML')
	if call.data == 'dataWeek2SborkaKomplektaPremiumRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1SborkaKomplektaPremiumRedFoto = sh.sheet1.get('C2')
		dataSborkaKomplektaPremiumRedFoto = week1SborkaKomplektaPremiumRedFoto[0][0]
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET urok2 = '{dataSborkaKomplektaPremiumRedFoto}' WHERE idTeleg = '{call.from_user.id}'""")
		# cur.execute("""UPDATE user SET urok1 = ? WHERE idTeleg = ?""", (dataStandartRabotyPSRedFoto, call.message.from_user.id))
		conn.commit()
		week1RabotaNadOshcibkamiObrabotkiRedFoto = sh.sheet1.get('B4')
		week2RabotaNadOshcibkamiObrabotkiRedFoto = sh.sheet1.get('C4')
		dataRabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardMarkup()
		dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardButton(text=week1RabotaNadOshcibkamiObrabotkiRedFoto[0][0], callback_data='dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto')
		dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardButton(text=week2RabotaNadOshcibkamiObrabotkiRedFoto[0][0], callback_data='dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto')
		dataRabotaNadOshcibkamiObrabotkiRedFoto.add(dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto)
		dataRabotaNadOshcibkamiObrabotkiRedFoto.add(dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto)
		bot.send_message(call.message.chat.id, text=f'Выбери удобную дату и время, чтобы пройти урок “Работа над ошибками обработки”', reply_markup=dataRabotaNadOshcibkamiObrabotkiRedFoto, parse_mode= 'HTML')
# ============================================================
	if call.data == 'dataWeek1RabotaNadOshcibkamiObrabotkiRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1RabotaNadOshcibkamiObrabotkiRedFoto = sh.sheet1.get('B4')
		dataRabotaNadOshcibkamiObrabotkiRedFoto = week1RabotaNadOshcibkamiObrabotkiRedFoto[0][0]
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET urok3 = '{dataRabotaNadOshcibkamiObrabotkiRedFoto}' WHERE idTeleg = '{call.from_user.id}'""")
		# cur.execute("""UPDATE user SET urok1 = ? WHERE idTeleg = ?""", (dataStandartRabotyPSRedFoto, call.message.from_user.id))
		conn.commit()
		bot.send_message(call.message.chat.id, text=f'Теперь напиши свои Фамилию Имя Отчество (постарайся сделать это без ошибок)', parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, get_sendGoogle);

	if call.data == 'dataWeek2RabotaNadOshcibkamiObrabotkiRedFoto':
		sh = gc.open_by_key(googlesheet_id)
		week1RabotaNadOshcibkamiObrabotkiRedFoto = sh.sheet1.get('C4')
		dataRabotaNadOshcibkamiObrabotkiRedFoto = week1RabotaNadOshcibkamiObrabotkiRedFoto[0][0]
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET urok3 = '{dataRabotaNadOshcibkamiObrabotkiRedFoto}' WHERE idTeleg = '{call.from_user.id}'""")
		# cur.execute("""UPDATE user SET urok1 = ? WHERE idTeleg = ?""", (dataStandartRabotyPSRedFoto, call.message.from_user.id))
		conn.commit()
		bot.send_message(call.message.chat.id, text=f'Теперь напиши свои Фамилию Имя Отчество (постарайся сделать это без ошибок)', parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, get_sendGoogle);

# ===============================================================================
	if call.data == 'offlineRedFoto':
		kalibrovkaRedFoto = types.InlineKeyboardMarkup()
		buttonKalibrovkaRedFoto = types.InlineKeyboardButton(text='Открыть урок', url='https://disk.yandex.ru/d/tA2VsO6-LBkoHw/%D0%9A%D0%B0%D0%BB%D0%B8%D0%B1%D1%80%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B0')
		kalibrovkaRedFoto.add(buttonKalibrovkaRedFoto)
		bot.send_message(call.message.chat.id, text=f"✔️Калибровка монитора 🔻", reply_markup=kalibrovkaRedFoto, parse_mode= 'HTML')

		lightroomRedFoto = types.InlineKeyboardMarkup()
		buttonLightroomRedFotoRedFoto = types.InlineKeyboardButton(text='Открыть урок', url='https://disk.yandex.ru/d/tA2VsO6-LBkoHw/%D0%A1%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D1%8B %D1%86%D0%B2%D0%B5%D1%82%D0%BE%D0%BA%D0%BE%D1%80%D1%80%D0%B5%D0%BA%D1%86%D0%B8%D0%B8 %D0%B2 LR')
		testLightroomRedFotoRedFoto = types.InlineKeyboardButton(text='Тест по теме', url='https://onlinetestpad.com/svx6oam4tq3vk')
		lightroomRedFoto.add(buttonLightroomRedFotoRedFoto, testLightroomRedFotoRedFoto)
		# lightroomRedFoto.add(testLightroomRedFotoRedFoto)
		bot.send_message(call.message.chat.id, text=f"✔️Стандарты работы в Lr (цветокоррекция) 🔻", reply_markup=lightroomRedFoto, parse_mode= 'HTML')

		komplektStandartRedFoto = types.InlineKeyboardMarkup()
		buttonKomplektStandartRedFoto = types.InlineKeyboardButton(text='Открыть урок', url='https://disk.yandex.ru/d/tA2VsO6-LBkoHw/%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0 %D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%82%D0%B0 %D0%A1%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82')
		testKomplektStandartRedFoto = types.InlineKeyboardButton(text='Тест по теме', url='https://onlinetestpad.com/kw3i3wgzt3ubw')
		komplektStandartRedFoto.add(buttonKomplektStandartRedFoto, testKomplektStandartRedFoto)
		# komplektStandartRedFoto.add(testKomplektStandartRedFoto)
		bot.send_message(call.message.chat.id, text=f"✔️Сборка комплекта Стандарт 🔻", reply_markup=komplektStandartRedFoto, parse_mode= 'HTML')

		jobCrmRedFoto = types.InlineKeyboardMarkup()
		buttonJobCrmRedFoto = types.InlineKeyboardButton(text='Открыть урок', url='https://disk.yandex.ru/d/HFuSK9pSlvLmAQ')
		testJobCrmRedFoto = types.InlineKeyboardButton(text='Тест по теме', url='https://onlinetestpad.com/3x2uj3d6aafn2')
		jobCrmRedFoto.add(buttonJobCrmRedFoto, testJobCrmRedFoto)
		# jobCrmRedFoto.add(testJobCrmRedFoto)
		bot.send_message(call.message.chat.id, text=f"✔️Работа в CRM 🔻", reply_markup=jobCrmRedFoto, parse_mode= 'Markdown')

		oformlenie = types.InlineKeyboardMarkup()
		infoOformlenie = types.InlineKeyboardButton(text='Получить информацию по оформлению', callback_data='infoOformlenie')
		oformlenie.add(infoOformlenie)
		bot.send_message(call.message.chat.id, text=f"После обучения мы предлагаем оформить наше сотрудничество.", reply_markup=oformlenie, parse_mode= 'HTML')

	if call.data == 'infoOformlenie':
		bot.send_message(call.message.chat.id, text=f"1. Если ты хочешь первое время работать в формате фриланс (не более 1 месяца), то необходимо:\n👉 скачать и заполнить в электронном виде соглашение https://docs.google.com/document/d/1XQrV1nHpqFeHU-15mRNqhHlaIUpRITF68FkfWpIvk6k/edit?usp=sharing\n👉 прислать на Hrm@bsmile.ru заполненное соглашение и фото страниц паспорта с ФИО, датой рождения и адресом регистрации, номер ЮMoney кошелька для выплат за проведенные работы, контактный номер телефона.\n\n2. Также можно в любой момент <a href='https://docs.google.com/document/d/1O9la64gMrtTU7M5N8jQRgiLlDT4KJSBsaJvlLCCPhAM/edit?usp=sharing'>подписать постоянный договор</a>  по <a href='https://docs.google.com/document/d/1UJLMSkxyy7MslbSwtqFpHGg8kVu5GCjUVkFlJVJN3n4/edit?usp=sharing'>образцу</a>\n👉 Заполненный в электронном виде договор с приложениями, копию паспорта (первый разворот и страницу с действующей регистрацией), копию банковских реквизитов и справку о регистрации как самозанятого направить на почту hrm@bsmile.ru\n👉 Для удобного подписания документов нужно зарегистрироваться в системе электронного документооборота «КонтурСайн» по ссылке  https://cabinet.kontur.ru/pages/registration/sign?utm_source=kontur-sign.ru&utm_medium=referral&p=1210&utm_referer=yandex.ru&utm_startpage=kontur-sign.ru&utm_orderpage=kontur-sign.ru\n👉 Подписать договор посредством неквалифицированной электронной подписи по ссылке, которая придет на твою почту.\n\nПосле получения документов на твой телефон придет сообщение с логином и паролем для входа в CRM (адрес CRM bphoto.pro).", disable_web_page_preview = True, parse_mode= 'HTML')
		bot.send_message(call.message.chat.id, text=f"Нажав кнопку “Ответы на частые вопросы”, ты сможешь найти подсказку на самые частые вопросы. \nПо всем остальным мы на связи по почте hrm@bsmile.ru\nТакже я добавлю тебя в чат с наставником и другими учениками.\n\nЖелаю успехов!😃", parse_mode= 'HTML')






def get_sendGoogle(message):
	global nameRedFoto
	nameRedFoto = message.text;
	conn = sqlite3.connect('db.db')
	cur = conn.cursor()
	cur.execute(f"""UPDATE user SET name = '{nameRedFoto}' WHERE idTeleg = '{message.from_user.id}'""")
	conn.commit()
	conn = sqlite3.connect('db.db')
	cur = conn.cursor()
	cur.execute(f"""SELECT * FROM user WHERE idTeleg = '{message.from_user.id}' """)
	rows = cur.fetchall()
	for row in rows:
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()
		cur.execute(f"""UPDATE user SET name = '{nameRedFoto}' WHERE idTeleg = '{message.from_user.id}'""")
		sh = gc.open_by_key(googlesheet_id)
		sh = gc.open_by_key(googlesheet_id)
		sh.sheet1.append_row([row[3], row[5], row[4], row[6]])
		testPoOnline = types.InlineKeyboardMarkup()
		testStandartRabotyPSRedFoto = types.InlineKeyboardButton(text='Пройти тест по теме Стандарты работы в PS (ретушь)', url='https://onlinetestpad.com/6jwyuhuzq56na')
		testSborkaKomplektaPremiumRedFoto = types.InlineKeyboardButton(text='Пройти тест по теме PS: сборка комплекта Премиум', url='https://onlinetestpad.com/iqzaqbmwcfn34')
		testRabotaNadOshcibkamiObrabotkiRedFoto = types.InlineKeyboardButton(text='Пройти тест по теме Работа над ошибками обработки', url='https://onlinetestpad.com/whthpi2c6l2ik')
		testPoOnline.add(testStandartRabotyPSRedFoto)
		testPoOnline.add(testSborkaKomplektaPremiumRedFoto)
		testPoOnline.add(testRabotaNadOshcibkamiObrabotkiRedFoto)

		bot.send_message(message.chat.id, text=f'👍Отлично! Я записала тебя на онлайн занятия: \nСтандарты работы в PS (ретушь) - {row[4]}\nPS: сборка комплекта Премиум - {row[5]}\nРабота над ошибками обработки - {row[6]}\n\nВсе они пройдут с демонстрацией экрана по этой ссылке https://join.skype.com/CehFxXbXRt9L\nВключать видео участникам не нужно ;)\n\nПосле посещения уроков не забудь пройти тесты для проверки своих знаний 😁', reply_markup=testPoOnline, parse_mode= 'HTML')

		offlineRedFoto = types.InlineKeyboardMarkup()
		offline = types.InlineKeyboardButton(text='🎓ТЕМЫ ДЛЯ САМОСТОЯТЕЛЬНОГО ИЗУЧЕНИЯ:', callback_data='offlineRedFoto')
		offlineRedFoto.add(offline)
		bot.send_message(message.chat.id, text=f'Идем дальше 😉 Чтобы стать лучшим редактором нужно самостоятельно изучить еще 4 темы 👇', reply_markup=offlineRedFoto, parse_mode= 'HTML')















def main(use_logging, level_name):
	if use_logging:
		telebot.logger.setLevel(logging.getLevelName(level_name))
	bot.polling(none_stop=True, interval=.5)
if __name__ == '__main__':
    main(True, 'DEBUG')

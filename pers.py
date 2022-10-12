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

bot = telebot.TeleBot('5742914126:AAHGBHVsUsfeAYzSkhVAL02GU2-Xi9JbcSI')
googlesheet_id = '1BeLdVhUHOaz6SKcyUhv3JkHTI5w94ZMsPXyr1_q_Jr4'
gc = gspread.service_account(filename='maria-359514-cb22a8d7b592.json')

tel = ''
zapros = ''
name = ''


@bot.message_handler(commands=['start'])
def start(message):
	conn = sqlite3.connect('db2.db')
	cur = conn.cursor()
	cur.execute(f"""SELECT * FROM users WHERE idTeleg = '{message.from_user.id}' """)
	rows = cur.fetchall()
	if len(rows) < 1:
		now = datetime.datetime.now()
		dataOform = now.strftime("%d-%m-%Y")
		conn = sqlite3.connect('db2.db')
		cur = conn.cursor()
		cur.execute("""INSERT INTO users(idTeleg, data) VALUES ( ?, ?)""", (message.from_user.id, dataOform ))
		conn.commit()
		keyboards = telebot.types.ReplyKeyboardMarkup(True)
		keyboards.row('ПОДАТЬ ЗАПРОС')
		bot.send_message(message.chat.id, text=f"Здравствуй коллега! Я виртуальный помощник Babysmile Group. Здесь ты можешь написать свой персональный вопрос или просьбу, c которой мы постараемся помочь. Или напиши на demidovich@bsmile.ru есть ", reply_markup=keyboards, parse_mode= 'HTML')
	else:
		keyboards = telebot.types.ReplyKeyboardMarkup(True)
		keyboards.row('ПОДАТЬ ЗАПРОС')
		bot.send_message(message.chat.id, text=f"Здравствуй коллега! Я виртуальный помощник Babysmile Group. Здесь ты можешь написать свой персональный вопрос или просьбу, c которой мы постараемся помочь. Или напиши на demidovich@bsmile.ru нет ", reply_markup=keyboards, parse_mode= 'HTML')
	# conn = sqlite3.connect('db2.db')
	# cur = conn.cursor()
	# cur.execute("""INSERT INTO person(id, name, zapros, nomer) VALUES ( ?, ?, ?, ?)""", (message.from_user.id, dataOform ))
	# conn.commit()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text.lower() == 'подать запрос':
		bot.send_message(message.chat.id, text=f"Напиши и отправь мне тект своего обращения", parse_mode= 'HTML')
		bot.register_next_step_handler(message, get_name);

def get_name(message):
	global zapros
	zapros = message.text
	bot.send_message(message.from_user.id, 'Теперь введи своё имя')
	bot.register_next_step_handler(message, get_tel)
def get_tel(message):
	global name
	name = message.text
	bot.send_message(message.from_user.id, 'Теперь отправь мне свой номер телефона для связи')
	bot.register_next_step_handler(message, get_result)
def get_result(message):
	global tel
	tel = message.text
	conn = sqlite3.connect('db2.db')
	cur = conn.cursor()
	cur.execute("""INSERT INTO person(name, zapros, nomer, idTeleg) VALUES ( ?, ?, ?, ?)""", (name, zapros, tel, message.from_user.id))
	conn.commit()
	sh = gc.open_by_key(googlesheet_id)
	sh.sheet1.append_row([name, zapros, tel, message.from_user.id])
	bot.send_message(message.from_user.id, 'Я отправил ваш запрос, ожидайте с вами свяжется наш специалистn')




def main(use_logging, level_name):
	if use_logging:
		telebot.logger.setLevel(logging.getLevelName(level_name))
	bot.polling(none_stop=True, interval=.5)
if __name__ == '__main__':
    main(True, 'DEBUG')
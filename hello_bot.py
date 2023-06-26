from config import *
import telebot
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO) # Outputs debug messages to console.

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

bot.polling()

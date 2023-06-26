import logging
import traceback

from config import *
from util import *

import telebot
from flask import Flask, request, jsonify

app = Flask(__name__)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='MarkdownV2')


def send_action(tx):
    message = handle_transaction(tx)
    try:
        bot.send_message(MAIN_CHANNEL, message, disable_web_page_preview=True)
    except Exception as e:
        print(traceback.format_exc(e))

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/push', methods = ['POST'])
def push_event():
    data = request.form['data']
    tx = json.loads(data)
    send_action(tx)
    return tx


if __name__ == '__main__':
    app.run()

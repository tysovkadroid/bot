from flask import Flask, request
from telegram import Update

from bot import bot, update_queue
from bot.config import TOKEN, HOST, PORT, URL

app = Flask(__name__)


@app.route('/' + TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        update_queue.put(update)
    return '', 200


@app.route('/setWebhook')
def process_webhook():
    bot.delete_webhook()
    bot.set_webhook(URL + TOKEN)
    return '', 200


@app.route('/')
def index():
    return '', 200


if __name__ == '__main__':
    app.run(HOST, PORT, debug=False, use_evalex=False)

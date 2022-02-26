import flask
from telebot import types

from main import bot
import os

from config import Config

conf = Config("data/config.csv")
server = flask.Flask(__name__)


@server.route('/' + conf.get("token"), methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(
        flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
async def index():
    await bot.remove_webhook()
    await bot.set_webhook(url="https://{}.herokuapp.com/{}".format(conf.get("name"), conf.get("token")))
    return "Hello from Heroku!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

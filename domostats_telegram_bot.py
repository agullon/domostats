import json, requests, time, urllib, configparser
from urllib.parse import quote_plus
import temperature

BASE_URL = ''

def set_base_url():
    global BASE_URL
    config = configparser.RawConfigParser()
    config.read('../keys/connection_tokens.ini')
    bot_token = config.get('telegram', 'domostats.bot')
    BASE_URL = 'https://api.telegram.org/bot{}/'.format(bot_token)  

def get_base_url():
    global BASE_URL
    return BASE_URL

def get_url(url): 
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_updates(offset=None):
    url = get_base_url() + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    content = get_url(url)
    return json.loads(content)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def inline_keyboard():
    reply_markup = {
        "inline_keyboard": [
        [{"text":temperature.HALL,"callback_data":temperature.HALL},
         {"text":temperature.MAIN_ROOM,"callback_data":temperature.MAIN_ROOM}]
       ]
    }
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = quote_plus(text)
    url = get_base_url() + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def get_text_and_chat_id(update):
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
    elif "callback_query" in update:
        text = update["callback_query"]["data"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
    return text, chat_id


def handle_updates(updates):
    for update in updates["result"]:
        text, chat_id = get_text_and_chat_id(update)
        if text == temperature.HALL or text == temperature.MAIN_ROOM:
            send_message(temperature.temperature_status(text), chat_id)
        send_message("Elige un lugar", chat_id, inline_keyboard())


def main():
    set_base_url()
    temperature.start()
    last_update_id = None
    updates = get_updates()
    if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        get_updates(last_update_id)
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
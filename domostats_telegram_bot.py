import json, requests, time, urllib, configparser
from urllib.parse import quote_plus
import temperature, hue_requests, stats, domostats

BASE_URL = ''

def set_base_url():
    global BASE_URL
    config = configparser.RawConfigParser()
    config.read('../keys/connection_tokens.ini')
    bot_token = config.get('telegram', 'domostats.bot')
    BASE_URL = 'https://api.telegram.org/bot{}/'.format(bot_token)  

def get_url(url): 
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    content = get_url(url)
    return json.loads(content)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def rooms_keyboard():
    reply_markup = {
        "inline_keyboard": [
        [
         #{'text':domostats.spanish_name[domostats.INDOOR],'callback_data':domostats.INDOOR},
         #{'text':domostats.spanish_name[domostats.OUTDOOR],'callback_data':domostats.OUTDOOR},
         {'text':'ahora mismo','callback_data':'ahora mismo'},
         {'text':'evolución','callback_data':'evolución'}]
       ]
    }
    return json.dumps(reply_markup)

def single_button_keyboard():
    reply_markup = {
        "inline_keyboard": [
        [{"text":"Toda la info","callback_data":"toda la info"}]
       ]
    }
    return json.dumps(reply_markup)

def send_message(text, chat_id, reply_markup=None):
    url = BASE_URL + 'sendMessage'
    url += '?text={}'.format(quote_plus(text))
    url += '&chat_id={}'.format(chat_id)
    url += '&parse_mode=Markdown'
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    r = requests.get(url)

def send_image(photo, chat_id):
    url = BASE_URL + 'sendPhoto'
    files = {'photo':photo}
    data = {'chat_id':chat_id}
    r = requests.post(url, files=files, data=data)

def get_text_and_chat_id(update):
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
    elif "callback_query" in update:
        text = update["callback_query"]["data"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
    return text, chat_id

def handle_updates(updates):
    for update in updates['result']:
        text, chat_id = get_text_and_chat_id(update)
        if text == domostats.INDOOR or text == domostats.OUTDOOR:
            send_message(temperature.room_status(text), chat_id)
        elif text == 'ahora mismo':
            send_message(temperature.all_rooms(), chat_id)
        elif text == 'evolución':
            send_image(stats.get_plot_png(), chat_id)
        send_message('Elige:', chat_id, rooms_keyboard())

def main():
    set_base_url()
    hue_requests.set_endpoint()
    last_update_id = None
    updates = get_updates()
    if len(updates['result']) > 0:
        last_update_id = get_last_update_id(updates) + 1
        get_updates(last_update_id)
    while True:
        updates = get_updates(last_update_id)
        if len(updates['result']) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
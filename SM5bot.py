import config
import telebot
import requests
from io import BytesIO
from PIL import Image
from pyowm import OWM
from urllib import parse

bot = telebot.TeleBot(config.token, parse_mode=None)

owm = OWM(config.APIkey, config.config_dict)
mgr = owm.weather_manager()

@bot.message_handler(commands=['start']) # /start Стартовое сообщение с подсказкой по началу работы
def send_start(message):
	bot.reply_to(message, """Привет!
Это универсальный бот, список команд:
/city - погода 
/map - дорожная ситуация по адресу
/help - справочная информация.""")

@bot.message_handler(commands=['help']) # /help Подсказка по списку команд и функционалу бота
def send_help(message):
	bot.reply_to(message, "Список команд бота пока ограничивается:\n/city - запрос погоды в указанном городе,\n/map - запрос пробок по указанному адресу.\nСкоро он будет дополнен!")

@bot.message_handler(content_types=['text', 'photo' , 'document']) # Ответ на запрос погоды в указанном городе
def cityreader(message):
    if message.text == '/city':
        bot.send_message(message.chat.id, "Укажите название города")
        bot.register_next_step_handler(message, send_weather_answer)
    elif message.text == '/map':
        bot.send_message(message.chat.id, "Введите адрес")
        bot.register_next_step_handler(message, searcher )
    else:
        bot.send_message(message.chat.id, "Укажите верную команду - /command")
def send_weather_answer(message):
    city = message.text
    observation = mgr.weather_at_place(city)
    w = observation.weather
    deg = u'\u2103'
    # bot.reply_to(message, message.text)
    answer = "В городе " + city + " сейчас " + str(w.detailed_status) + ", температура воздуха составляет " + str(w.temperature('celsius')['temp']) + str(deg) + " , ощущается как " + str(w.temperature('celsius')['feels_like']) + str(deg) + "." + "\n" + "Время измерений: " + str(w.reference_time(timeformat='iso'))
    bot.send_message(message.chat.id, answer)
def searcher(message):
    adress = message.text
    url = "https://nominatim.openstreetmap.org/search.php?"
    value = {'q' : adress}
    valuedata = parse.urlencode(value)
    OSMapi = url + valuedata
    response = requests.get(OSMapi + '&polygon_geojson=1&format=json&limit=1')
    coord = response.json()
    datadict = list(coord[0]['boundingbox'])
    #datadict = dict((coord[0]['geojson']))
    #coordlist = list(datadict['coordinates'])
    #print(coordlist)
    latitude = datadict[2]
    longitude = datadict[1]
    latlon = str(latitude) + ',' + str(longitude)
    mstyle = "l=map,trf,skl"
    size = "size=650,450&z=13"
    YANDEXapi = "https://static-maps.yandex.ru/1.x/?ll="
    i1 = requests.get(YANDEXapi + latlon + "&" + size + "&" + mstyle)
    i2 = i1.content
    img = Image.open(BytesIO(i2))
    bot.send_photo(message.chat.id, img)

if __name__ == '__main__':
    bot.infinity_polling()
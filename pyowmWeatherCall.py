from pyowm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('a675eb29624b81306b830ee74a258203', config_dict)
mgr = owm.weather_manager()

place = input("Введите интересующий город: ")

observation = mgr.weather_at_place(place)
w = observation.weather
deg = u'\u2103'
print("В городе " + place + " сейчас " + str(w.detailed_status) + ", температура воздуха составляет " + str(w.temperature('celsius')['temp']) + str(deg) + " , ощущается как " + str(w.temperature('celsius')['feels_like']) + str(deg) + "\n" +
"Время измерений: " + str(w.reference_time(timeformat='iso')))
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']

city = os.environ['CITY']
# city1 = os.environ['CITY1']
# city2 = os.environ['CITY2']

birthday = os.environ['BIRTHDAY']
# birthday1 = os.environ['BIRTHDAY1']
# birthday2 = os.environ['BIRTHDAY2']
# birthday3 = os.environ['BIRTHDAY3']
# birthday4 = os.environ['BIRTHDAY4']
# birthday5 = os.environ['BIRTHDAY5']
# birthday6 = os.environ['BIRTHDAY6']


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   url1 = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
#   url2 = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city2
  res = requests.get(url).json()
#   res1 = requests.get(url1).json()
#   res2 = requests.get(url2).json()
  weather = res['data']['list'][0]
#   weather1 = res1['data']['list'][0]
#   weather2 = res2['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])
# ,weather1['weather'], math.floor(weather1['temp']),weather2['weather'], math.floor(weather2['temp'])

def get_weather1():
  url1 = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
#   res = requests.get(url).json()
  res1 = requests.get(url1).json()
#   res2 = requests.get(url2).json()
#   weather = res['data']['list'][0]
  weather1 = res1['data']['list'][0]
#   weather2 = res2['data']['list'][0]
  return weather1['weather'], math.floor(weather1['temp'])
# ,weather1['weather'], math.floor(weather1['temp']),weather2['weather'], math.floor(weather2['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# def get_birthday1():
#   next1 = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
#   if next1 < datetime.now():
#     next1 = next1.replace(year=next1.year + 1)
#   return (next1 - today).days

# def get_birthday2():
#   next2 = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
#   if next2 < datetime.now():
#     next2 = next2.replace(year=next2.year + 1)
#   return (next2 - today).days

# def get_birthday3():
#   next3 = datetime.strptime(str(date.today().year) + "-" + birthday3, "%Y-%m-%d")
#   if next3 < datetime.now():
#     next3 = next3.replace(year=next3.year + 1)
#   return (next3 - today).days

# def get_birthday4():
#   next4 = datetime.strptime(str(date.today().year) + "-" + birthday4, "%Y-%m-%d")
#   if next4 < datetime.now():
#     next4 = next4.replace(year=next4.year + 1)
#   return (next4 - today).days

# def get_birthday5():
#   next5 = datetime.strptime(str(date.today().year) + "-" + birthday5, "%Y-%m-%d")
#   if next5 < datetime.now():
#     next5 = next5.replace(year=next5.year + 1)
#   return (next5 - today).days

# def get_birthday6():
#   next6 = datetime.strptime(str(date.today().year) + "-" + birthday6, "%Y-%m-%d")
#   if next6 < datetime.now():
#     next6 = next6.replace(year=next6.year + 1)
#   return (next6 - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

# wea, temperature,wea1, temperature1,wea2, temperature2 = get_weather()
wea, temperature= get_weather()
wea1, temperature1= get_weather1()

data = {"weather":{"value":wea},"temperature":{"value":temperature},
        "weather1":{"value":wea1},"temperature1":{"value":temperature1},
#         "weather2":{"value":wea2},"temperature2":{"value":temperature2},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday()},
#         "birthday_left1":{"value":get_birthday1()},
#         "birthday_left2":{"value":get_birthday2()},
#         "birthday_left3":{"value":get_birthday3()},
#         "birthday_left4":{"value":get_birthday4()},
#         "birthday_left5":{"value":get_birthday5()},
#         "birthday_left6":{"value":get_birthday6()},
        "words":{"value":get_words(), "color":get_random_color()}
        }
res = wm.send_template(user_id, template_id, data)
print(res)


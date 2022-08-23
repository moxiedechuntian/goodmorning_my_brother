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
city1 = "西安"
city2 = "北京"
birthday = os.environ['BIRTHDAY']
birthday1 = "06-01"
birthday2 = '11-12'
birthday3 = '09-18'
birthday4 = '10-09'
birthday5 = '01-24'
birthday6 = '02-03'
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
# user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather(a):
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + a
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low']), weather['date']

wea, temperature,high,low,date= get_weather(city)
wea1, temperature1,high1,low1= get_weather(city1)
wea2, temperature2,high2,low2= get_weather(city2)


def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(d):
  next = datetime.strptime(str(date.today().year) + "-" + d, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

birthday = get_birthday(birthday)
birthday1 = get_birthday(birthday1)
birthday2 = get_birthday(birthday2)
birthday3 = get_birthday(birthday3)
birthday4 = get_birthday(birthday4)
birthday5 = get_birthday(birthday5)
birthday6 = get_birthday(birthday6)

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

data = {"date":{"value":date},
        "weather":{"value":wea},"temperature":{"value":temperature},"high":{"value":high},"low":{"value":low},
        "weather1":{"value":wea1},"temperature1":{"value":temperature1},"high1":{"value":high1},"low1":{"value":low1},
        "weather2":{"value":wea2},"temperature2":{"value":temperature2},"high2":{"value":high2},"low":{"value":low2},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":birthday},
        "birthday_left1":{"value":birthday1},
        "birthday_left2":{"value":birthday2},
        "birthday_left3":{"value":birthday3},
        "birthday_left4":{"value":birthday4},
        "birthday_left5":{"value":birthday5},
        "birthday_left6":{"value":birthday6},
        "words":{"value":get_words(), "color":get_random_color()}
        }
res = wm.send_template(user_id, template_id, data)
print(res)


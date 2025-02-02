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
city1 = "成都"
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

# user_id = os.environ["USER_ID"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather(a):
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + a
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

wea, temperature,high,low = get_weather(city)
wea1, temperature1,high1,low1 = get_weather(city1)
wea2, temperature2,high2,low2 = get_weather(city2)

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
  words = requests.get("https://api.shadiao.pro/du")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

data = {
        "date":{"value":today.strftime('%Y年%m月%d日'), "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"high":{"value":high, "color":get_random_color()},"low":{"value":low, "color":get_random_color()},
        "weather1":{"value":wea1, "color":get_random_color()},"temperature1":{"value":temperature1, "color":get_random_color()},"high1":{"value":high1, "color":get_random_color()},"low1":{"value":low1, "color":get_random_color()},
        "weather2":{"value":wea2, "color":get_random_color()},"temperature2":{"value":temperature2, "color":get_random_color()},"high2":{"value":high2, "color":get_random_color()},"low2":{"value":low2, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "birthday_left":{"value":birthday, "color":get_random_color()},
        "birthday_left1":{"value":birthday1, "color":get_random_color()},
        "birthday_left2":{"value":birthday2, "color":get_random_color()},
        "birthday_left3":{"value":birthday3, "color":get_random_color()},
        "birthday_left4":{"value":birthday4, "color":get_random_color()},
        "birthday_left5":{"value":birthday5, "color":get_random_color()},
        "birthday_left6":{"value":birthday6, "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}
        }

count=0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1
# print(res)
print("发送了"+str(count)+"条消息")

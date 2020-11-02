#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         : imooc
# @Email          : imooc@foxmail.com
# @Created at     : 2018/11/21
# @Filename       : juhe.py
# @Desc           :


import json
import requests
from utils import proxy


def weather(city):
    """
    :param city: 城市名字
    :return: 返回实况天气
    """
    key = '13d7317bb5c82bd56fe3dccd3e0e2aee'
    api = 'http://apis.juhe.cn/simpleWeather/query'
    params = 'city=%s&key=%s' % (city, key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url)
    json_data = json.loads(response.text)
    print(json_data)
    result = json_data.get('result')
    realtime = result.get('realtime')
    response = dict()
    response['temperature'] = realtime.get('temperature')
    response['info'] = realtime.get('info')
    response['direct'] = realtime.get('direct')
    response['power'] = realtime.get('power')
    response['humidity'] = realtime.get('humidity')  # 湿度
    response['aqi'] = realtime.get('aqi') #空气指数
    return response

def constellation(cons_name):
    key = 'fed29157ba4d3fb9aec2f0625d07838d'
    api = 'http://web.juhe.cn:8080/constellation/getAll'
    type = 'today'
    params = '?consName=%s&type=%s&key=%s' %(cons_name, type, key)
    url = api + params
    print(url)
    response = requests.get(url, proxies=proxy.proxy())
    data = json.loads(response.text)
    return {
        "name": cons_name,
        "text": data['summary']
    }

if __name__ == '__main__':
    data = weather('深圳')

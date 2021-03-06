#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
Copyright (c) 2013 Qimin Huang <qiminis0801@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import requests
import json
import time


class Weather:
    def __init__(self):
        pass

    def weather(self, cityid):
        flag = 1
        while flag:
            try:
                r = requests.get('http://www.weather.com.cn/data/cityinfo/' + cityid + '.html')
                weatherinfo = json.loads(r.text)[u'weatherinfo']
                flag = 0
            except:
                 pass
        return weatherinfo[u'city'] + u', ' + weatherinfo[u'weather'] + u', ' + weatherinfo[u'temp1'] + u' ~ ' + weatherinfo[u'temp2']


if __name__ == '__main__':
    weather = Weather()
    print weather.weather('101010100')
    print weather.weather('101231001')

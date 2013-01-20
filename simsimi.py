#-*-coding:utf-8-*-

"""
Copyright (c) 2012 wong2 <wonderfuly@gmail.com>

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
import cookielib


class SimSimi:

    def __init__(self):
        self.session = requests.Session()
        self.session.get('http://www.simsimi.com/talk.htm')

        self.headers = {
            'Referer': 'http://www.simsimi.com/talk.htm'
        }
        self.url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'

    def chat(self, message=''):
        if message.strip():
            r = self.session.get(self.url % message.strip(), headers=self.headers)
            try:
                return r.json()['response']
            except:
                return u'法海你不懂爱，雷峰塔会倒下来'
        else:
            return u'叫我干嘛'


if __name__ == '__main__':
    simi = SimSimi()
    print simi.chat('最后一个问题')

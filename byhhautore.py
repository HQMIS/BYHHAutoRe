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


# note:
# 1、This Python Script use Library urlllib2、urllib、cookielib:
#    see http://docs.python.org/2/library/urllib2.html
#    see http://docs.python.org/2/library/urllib.html
#    see http://docs.python.org/2/library/cookielib.html
# 2、This Python Script use SimSimi:
#     see https://github.com/wong2/xiaohuangji
#     see http://www.simsimi.com/talk.htm?lc=ch
#     see http://developer.simsimi.com/
# 3、 This Python Script can also use xiaoi:
#     see http://i.xiaoi.com

# Questions && Solutions
# 1、 GB2312对一些复杂汉字不支持：
#     see https://gist.github.com/4468718
# 2、 At times, response is not succeed:
#     Swallow post, to find the reason, and solve it...
#     Change character encoding GB18030...
#     Add retry for each class...
# 3、 执行一次log.i()往log.txt里面写入多次：
#      see http://bbs.csdn.net/topics/390205890


import time
import random
import cPickle as pickle
import os

from byhh import BYHH, NEWS, NEWSURL, REPLY, BBSSND
from ai import magic
from wr import getweather
from log import LOG

import requests


log = LOG()
#cwd = os.path.dirname(__file__) + os.path.sep
cwd = './'


def sleepTime():
    # BYHH会检测，是否为机器登录
    # 看到的是如果sleeptime时间为一个数，则被判为机器登录
    # 所以这里生成随机数来处理
    sleeptime = 15 + random.randint(0, 15)
    time.sleep(sleeptime)


def hanzi(hz):
    return hz.decode('utf8').encode('GB18030')


def unicode2GB18030(hz):
    return hz.encode('GB18030')


def specialWords(swList, _reply):
    for sw in swList:
        if sw in _reply:
            return True, sw
    return False, 'sw'


def analyseResponse(msg, first):
    return msg.split(first.decode('utf8'))[1].split('<br><font'.decode('utf8'))[0].encode('utf8')


def keyword_getResponse(kwid, appid):
    url = 'http://www.unidust.cn/search.do?type=web&appid='
    msg = requests.post(url + appid).text
    try:
        return analyseResponse(msg, '</font><br>')
    except:
        if 1 == kwid:
            return analyseResponse(msg, '可看笑话分类<br>')
        if 3 == kwid:
            return analyseResponse(msg, '<br></font>')


if __name__ == '__main__':
    username = raw_input('UserName: ')
    password = raw_input('PassWord: ')

    # 登录白云黄鹤
    byhh = BYHH(username, password)
    cookie = byhh.login()
    log.i(cookie)

    # 加载城市名称和城市id
    cityidDict = pickle.load(file(cwd + 'cityid', 'r'))
    # 加载SpecialWords列表
    specialWordsList = open(cwd + 'SpecialWords', 'r').readline().split(';')
    specialWordsDict = {}
    for sw in specialWordsList:
        specialWordsDict[sw.split(':')[0]] = sw.split(':')[1]

    # 加载sensitiveWords列表
    sensitiveWordsList = open(cwd + 'SensitiveWords', 'r').readline().split(';')

    while True:
        # 获取新鲜事列表页面，返回首个新鲜事Url
        news = NEWS()
        news_url = news.news(cookie)
        if 0 == news_url:
            log.i(hanzi('亲爱的') + username + hanzi(',  您暂时还没有新鲜事\n我先休息一会，等会再看看\n'))
            print hanzi('亲爱的') + username + hanzi(',  您暂时还没有新鲜事\n我先休息一会，等会再看看\n')
        else:
            log.i(hanzi('首新鲜事Url： ') + news_url)
            print hanzi('首新鲜事Url： '), news_url

            # 获取新鲜事页面，返回标题、内容、以及回文章的Url
            newsurl = NEWSURL()
            title, content, _reply, re_url = newsurl.newsurl('http://byhh.net/cgi-bin/' + news_url, cookie)
            log.i(hanzi('原帖标题： ') + title)
            print hanzi('原帖标题： '), title
            log.i(hanzi('引用文本： ') + ' '.join(content))
            print hanzi('引用文本： '), content
            log.i(hanzi('回帖内容： ') + _reply)
            print hanzi('回帖内容： '), _reply
            log.i(hanzi('回帖页面Url： ') + re_url)
            print hanzi('回帖页面Url： '), re_url

            # 获取回帖页面，返回回帖接口，源码action后的Url
            reply = REPLY()
            bbssnd_url = reply.reply('http://byhh.net/cgi-bin/' + re_url, cookie)
            log.i(hanzi('回帖接口： ') + bbssnd_url)
            print hanzi('回帖接口： '), bbssnd_url

            # 生成回复内容
            # 对于special words，会直接读取预设的内容进行回复
            tf, sw = specialWords(specialWordsDict.keys(), _reply)
            if  tf:
                re_info = "".join(open(cwd + specialWordsDict[sw]).readlines())
            elif hanzi('天气') in _reply:
                cityFlag = False
                for city in cityidDict.keys():
                    if unicode2GB18030(city) in _reply:
                        re_info = hanzi(getweather(city.encode('utf8')))
                        cityFlag = True
                        break
                if  not cityFlag:
                    re_info = hanzi(getweather('武汉'))
                else:
                    pass
            elif hanzi('笑话') in _reply or hanzi('讲笑话') in _reply or hanzi('讲个笑话') in _reply:
                re_info = hanzi(keyword_getResponse(1, '61'))
            elif hanzi('故事') in _reply or hanzi('讲故事') in _reply or hanzi('讲个故事') in _reply:
                re_info = hanzi(keyword_getResponse(2, '381'))
            else:  # SimSimi获取
                re_info = hanzi(magic(_reply.decode('GB18030')))
            log.i(re_info)
            print re_info

            # 判断是否有敏感词
            tf, sw = specialWords(sensitiveWordsList, re_info)
            if tf:
                log.i(hanzi('敏感词： ') + sw)
                print hanzi('敏感词： '), sw
                re_info = hanzi('昔人已乘黄鹤去，此地空余黄鹤楼。黄鹤一去不复返，白云千载空悠悠')
            else:
                pass

            # 回帖
            bbssnd = BBSSND('Re:' + title, re_info + os.linesep + os.linesep.join(content))
            bbssnd.bbssnd('http://byhh.net/cgi-bin/' + bbssnd_url, cookie)
        sleepTime()

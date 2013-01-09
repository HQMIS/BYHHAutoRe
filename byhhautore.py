#-*-coding:utf-8-*-

# script: byhhautore.py
# author: huangqimin@baidu.com

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
# 3、

import time
import random
import cPickle as pickle

from byhh import BYHH, NEWS, NEWSURL, REPLY, BBSSND
from ai import magic
from wr import getweather

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

if __name__ == '__main__':
    username = raw_input('UserName: ')
    password = raw_input('PassWord: ')

    # 登录白云黄鹤
    byhh = BYHH(username, password)
    cookie = byhh.login()
    print cookie

    # 加载城市名称和城市id
    cityidDict = pickle.load(file('./cityid', 'r'))
    # 加载SpecialWords列表
    specialWordsList = open('./SpecialWords', 'r').readline().split(';')
    specialWordsDict = {}
    for sw in specialWordsList:
        specialWordsDict[sw.split(':')[0]] = sw.split(':')[1]
    
    # 加载SpecialWords列表
    sensitiveWordsList = open('./SensitiveWords', 'r').readline().split(';')

    while True:
        # 获取新鲜事列表页面，返回首个新鲜事Url
        news = NEWS()
        news_url = news.news(cookie)
        print news_url
        if 0 == news_url:
            print hanzi('亲爱的')+username+hanzi(',  您暂时还没有新鲜事\n我先休息一会，等会再看看\n')
        else:
            print hanzi('首新鲜事Url： '), news_url

            # 获取新鲜事页面，返回标题、内容、以及回文章的Url
            newsurl = NEWSURL()
            title, content, _reply, re_url = newsurl.newsurl('http://byhh.net/cgi-bin/'+news_url, cookie)
            print hanzi('原帖标题： '), title
            print hanzi('引用文本： '), content
            print hanzi('回帖内容： '), _reply
            print hanzi('回帖页面Url： '), re_url

            # 获取回帖页面，返回回帖接口，源码action后的Url
            reply = REPLY()
            bbssnd_url = reply.reply('http://byhh.net/cgi-bin/'+re_url, cookie)
            print hanzi('回帖接口： '), bbssnd_url

            # 生成回复内容
            # 对于special words，会直接读取预设的内容进行回复
            tf, sw = specialWords(specialWordsDict.keys(), _reply)
            if  tf:
                re_info = "".join(open('./'+specialWordsDict[sw]).readlines())
            elif hanzi('天气') in _reply:
                cityFlag = False
                for city in cityidDict.keys():
                    if unicode2GB18030(city) in _reply:
                        re_info = hanzi(getweather(city.encode('utf8')))
                        cityFlag = True
                        break
                if  not cityFlag:
                    re_info = hanzi(getweather('武汉'))
            else: # SimSimi获取
                re_info = hanzi(magic(_reply.decode('GB18030')))
            print re_info
            
            # 判断是否有敏感词
            tf, sw = specialWords(sensitiveWordsList, re_info)
            if tf:
                print hanzi('敏感词： '), sw
                re_info = hanzi('昔人已乘黄鹤去，此地空余黄鹤楼。黄鹤一去不复返，白云千载空悠悠')
            else:
                pass
            
            # 回帖
            bbssnd = BBSSND('Re:'+title, re_info+'\n'+'\n'.join(content))
            bbssnd.bbssnd('http://byhh.net/cgi-bin/'+bbssnd_url, cookie)
        sleepTime()


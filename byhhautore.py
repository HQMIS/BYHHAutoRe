#-*-coding:utf-8-*-

# script: byhhautore.py
# author: huangqimin@baidu.com

# note: 
# 1、This Python Script use Library urlllib2、urllib、cookielib:
#    see http://docs.python.org/2/library/urllib2.html
#    see http://docs.python.org/2/library/urllib.html
#    see http://docs.python.org/2/library/cookielib.html
# 2、This Python Script use SimSimi:
#     see https://github.com/wong2/renren-bot
#     see http://www.simsimi.com/talk.htm?lc=ch
#     see http://developer.simsimi.com/
# 3、 This Python Script can also use xiaoi:
#     see http://i.xiaoi.com

import urllib
import urllib2
import cookielib
import random
import time
import cPickle as pickle

from ai import magic
from wr import getweather

class BYHH:
    def __init__(self, username, password):
        self.id = username
        self.pw = password
 
    def login(self):
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        params = {'id': self.id, 'pw': self.pw}
        req = urllib2.Request('http://bbs.whnet.edu.cn/cgi-bin/bbslogin', urllib.urlencode(params))
        source = opener.open(req).read()

        msg = []
        for i in range(0, 10):
            first = source.find("'")
            source = source.replace("'", '"', 1)
            second = source.find("\'")
            source = source.replace("\'", '"', 1)
            msg.append(source[first+1:second])   

        cookie = ""
        for i in range(3, 10):
            cookie = cookie + msg[i] + ";"

        return cookie

class NEWS:
    def __init__(self):
        pass
    
    def news(self, cookies):
        req = urllib2.Request("http://byhh.net/cgi-bin/bbsnewsfeed")
        req.add_header("Cookie", cookie)
        source = urllib2.urlopen(req).read()
        #print source
        return source.split('<td width=76><a href="')[1].split('"')[0]

class NEWSURL:
    def __init__(self):
        pass
    
    def newsurl(self, url, cookies):
        req = urllib2.Request(url)
        req.add_header("Cookie", cookie)
        source = urllib2.urlopen(req).read()
        #print source
        _title = source.split("<textarea")[1].split("\n")[2].split(":")[-1]
        _id = source.split("<textarea")[1].split("\n")[1].split(":")[1].split(",")[0]
        _content = source.split("<textarea")[1].split("--")[0].split("\n")[4:]
        for i in _content:
            if "" == i or "\r" == i or i.startswith(":") or i.startswith(hanzi("【")):
                pass
            else:
                _reply = i
        ### 引用内容太多时， 保留7行
        _content = _content[:7] if len(_content)>7 else _content
        _content = [": "+line.strip() for line in _content]
        re_url = source.split("[<a href=")[3].split("id")[0][1:-2]
        return _title, [hanzi("【 在 ")+_id+ hanzi("的大作中提到: 】"),]+_content, _reply.strip(), re_url

class REPLY:
    def __init__(self):
        pass
    
    def reply(self, url, cookies):
        req = urllib2.Request(url)
        req.add_header("Cookie", cookie)
        source = urllib2.urlopen(req).read()
        #print source
        return source.split("action")[1].split(">")[0][2:-1]
        
class BBSSND:
    def __init__(self, title, text, signature=1, start=7762):
        self.title = title
        self.text = text
        self.signature = signature
        self.start = start
 
    def bbssnd(self, url, cookies):
        params = {'title': self.title, 'signature':self.signature, 'start':self.start, 'text': self.text}
        req = urllib2.Request(url, urllib.urlencode(params))
        req.add_header("Cookie", cookie)
        print urllib2.urlopen(req).read()

def sleepTime():
    # BYHH会检测，是否为机器登录
    # 看到的是如果sleeptime时间为一个数，则被判为机器登录
    # 所以这里生成随机数来处理
    sleeptime = 15 + random.randint(0, 15)
    time.sleep(sleeptime)

def hanzi(hz):
    # 将汉字转为gb2312编码格式
    return hz.decode("utf8").encode("gb2312")

def utf82gb2312(hz):
    # 将unicode编码格式转换为gb2312编码格式
    return hz.encode("gb2312")

def utf82GBK(hz):
    # 将unicode编码格式转换为GBK编码格式
    return hz.encode("GBK")

if __name__ == '__main__':
    username = raw_input("UserName: ")
    password = raw_input("PassWord: ")

    ### 登录白云黄鹤
    byhh = BYHH(username, password)
    cookie = byhh.login()

    ### 加载城市名称和城市id
    cityidDict = pickle.load(file('./cityid', 'r'))

    while True:
        try:
            ### 获取新鲜事列表页面，返回首个新鲜事Url
            news = NEWS()
            news_url = news.news(cookie)
            print hanzi("首新鲜事Url： "), news_url

            ### 获取新鲜事页面，返回标题、内容、以及回文章的Url
            newsurl = NEWSURL()
            title, content, _reply, re_url = newsurl.newsurl("http://byhh.net/cgi-bin/"+news_url, cookie)
            print hanzi("原帖标题： "), title
            print hanzi("引用文本： "), content
            print hanzi("回帖内容： "), _reply
            print hanzi("回帖页面Url： "), re_url

            ### 获取回帖页面，返回回帖接口，源码action后的Url
            reply = REPLY()
            bbssnd_url = reply.reply("http://byhh.net/cgi-bin/"+re_url, cookie)
            print hanzi("回帖接口： "), bbssnd_url

            ### 生成回复内容，对于special words，会直接读取预设的内容进行回复，下面只是一个Demo(“男哥”)，其他的则去SimSimi获取
            if  hanzi("男哥") in _reply:
                re_info = "".join(open("./SolarChimeny").readlines())
            elif hanzi("天气") in _reply:
                cityFlag = False
                for city in cityidDict.keys():
                    if utf82GBK(city) in _reply:
                        re_info = hanzi(getweather(city.encode("utf8")))
                        cityFlag = True
                        break
                if  not cityFlag:
                    re_info = hanzi(getweather("武汉"))
            else:
                re_info = hanzi(magic(_reply.decode("gb2312")))
            print re_info
            
            ### 判断是否有敏感词
            if hanzi("呵呵") in re_info:
                print hanzi("敏感词： 微信")
                re_info = hanzi("昔人已乘黄鹤去，此地空余黄鹤楼。黄鹤一去不复返，白云千载空悠悠")
            else:
                pass
            
            ### 回帖
            bbssnd = BBSSND("Re:"+title, re_info+"\n"+"\n".join(content))
            bbssnd.bbssnd("http://byhh.net/cgi-bin/"+bbssnd_url, cookie)
        except:
            print hanzi("亲爱的")+username+hanzi(",  您暂时还没有新鲜事\n我先休息一会，等会再看看\n")
        sleepTime()


#-*-coding:utf-8-*-

# script: autoreply.py
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
from ai import magic

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
        return source.split("<td width=36>")[-1].split("<a href=")[4].split("target")[0][1:-2]  

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
            if "" == i or "\r" == i or i.startswith(":") or i.startswith("【".decode("utf8").encode("gb2312")):
                pass
            else:
                _reply = i 
        _content = [": "+line for line in _content]
        re_url = source.split("[<a href=")[3].split("id")[0][1:-2]
        return _title, ["【 在 ".decode("utf8").encode("gb2312")+_id+ "的大作中提到: 】".decode("utf8").encode("gb2312"),]+_content, _reply, re_url

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
 
if __name__ == '__main__':
    #username = raw_input("UserName:")
    #password = raw_input("PassWord:")
    username = "HQM"
    password = "4385663"

    ### 登录白云黄鹤
    byhh = BYHH(username, password)
    cookie = byhh.login()

    while True:
        try:
            ### 获取新鲜事列表页面，返回最后一个新鲜事Url
            news = NEWS()
            news_url = news.news(cookie)
            print news_url

            ### 获取新鲜事页面，返回标题、内容、以及回文章的Url
            newsurl = NEWSURL()
            title, content, _reply, re_url = newsurl.newsurl("http://byhh.net/cgi-bin/"+news_url, cookie)
            print title
            print content
            print _reply
            print re_url

            ### 获取回帖页面，返回回帖接口，源码action后的Url
            reply = REPLY()
            bbssnd_url = reply.reply("http://byhh.net/cgi-bin/"+re_url, cookie)
            print bbssnd_url
            
            ### 回帖，找的接口不对还是使用不对？回帖编程了发帖，好吧，把“Re”写成了“RE”
            ### 像@wong2的小黄鸡一样，这里自动添加一些回复，"\n".join(content)
            bbssnd = BBSSND("Re:"+title, magic(_reply.decode("gb2312")).decode("utf8").encode("gb2312")+"\n"+"\n".join(content))
            bbssnd.bbssnd("http://byhh.net/cgi-bin/"+bbssnd_url, cookie)
        except:
            print "亲爱的".decode("utf8").encode("gb2312")+username+",  您暂时还没有新鲜事\n我先休息一会，等会再看看".decode("utf8").encode("gb2312")
        sleepTime()


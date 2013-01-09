#-*-coding:utf-8-*-

# script: byhh.py
# author: huangqimin@baidu.com

# note: 
# 1、This Python Script is  Function for www.byhh.net

import urllib
import urllib2
import cookielib

class BYHH:
    def __init__(self, username, password):
        self.url = 'http://bbs.whnet.edu.cn/cgi-bin/bbslogin'
        self.id = username
        self.pw = password
 
    def login(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        urllib2.install_opener(opener)
        source = opener.open(urllib2.Request(self.url, urllib.urlencode({'id': self.id, 'pw': self.pw}))).read()
        # 不同帐号的cookie貌似不同，不知道啥情况
        return ';'.join([value for i, value in enumerate(source.split("'")[1:-2]) if 0==i%2][3:-1])

class NEWS:
    def __init__(self):
        self.url = 'http://byhh.net/cgi-bin/bbsnewsfeed'
    
    def _news(self, cookie):
        req = urllib2.Request(self.url)
        req.add_header('Cookie', cookie)
        return urllib2.urlopen(req).read().split('<td width=76><a href="')[1].split('"')[0]
    
    def news(self, cookie):
        try:
            return self._news(cookie)
        except:
            return 0
    
class NEWSURL:
    def __init__(self):
        pass
    
    def _newsurl(self, url, cookie):
        req = urllib2.Request(url)
        req.add_header('Cookie', cookie)
        source = urllib2.urlopen(req).read()
        _title = source.split('<textarea')[1].split('\n')[2].split(':')[-1]
        _id = source.split('<textarea')[1].split('\n')[1].split(':')[1].split(',')[0]
        _content = source.split('<textarea')[1].split('--')[0].split('\n')[4:]
        for i in _content:
            if "" == i or '\r' == i or i.startswith(':') or i.startswith(hanzi('【')):
                pass
            else:
                _reply = i
        # 引用内容太多时，保留7行
        _content = [': '+line.strip() for i, line in enumerate(_content) if i<7]
        re_url = source.split('[<a href=')[3].split('id')[0][1:-2]
        return _title, [hanzi('【 在 ')+_id+ hanzi('的大作中提到: 】'),]+_content, _reply.strip(), re_url

    def newsurl(self, url, cookie):
        try:
            return self._newsurl(url, cookie)
        except:
            return self.newsurl(url, cookie)
        
class REPLY:
    def __init__(self):
        pass
    
    def _reply(self, url, cookie):
        req = urllib2.Request(url)
        req.add_header('Cookie', cookie)
        return urllib2.urlopen(req).read().split('action')[1].split('>')[0][2:-1]

    def reply(self, url, cookie):
        try:
            return self._reply(url, cookie)
        except:
            return self.reply(url, cookie)        
        
class BBSSND:
    def __init__(self, title, text, signature=1, start=7762):
        self.title = title
        self.text = text
        self.signature = signature
        self.start = start
 
    def _bbssnd(self, url, cookie):
        req = urllib2.Request(url, urllib.urlencode({'title': self.title, 'signature':self.signature, 'start':self.start, 'text': self.text}))
        req.add_header('Cookie', cookie)
        print urllib2.urlopen(req).read()

    def bbssnd(self, url, cookie):
        try:
            return self._bbssnd(url, cookie)
        except:
            return self.bbssnd(url, cookie)

def hanzi(hz):
    return hz.decode('utf8').encode('GB18030')

if __name__ == '__main__':
    username = raw_input('UserName: ')
    password = raw_input('PassWord: ')

    # 登录白云黄鹤
    byhh = BYHH(username, password)
    cookie = byhh.login()
    print cookie

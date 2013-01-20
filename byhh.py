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
# 1、This Python Script is  Function for www.byhh.net


import urllib
import urllib2
import cookielib
import os
import time
import logging


from log import LOG


log = LOG()


class BYHH:
    def __init__(self, username, password):
        self.url = 'http://bbs.whnet.edu.cn/cgi-bin/bbslogin'
        self.id = username
        self.pw = password

    def login(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        urllib2.install_opener(opener)
        source = opener.open(urllib2.Request(self.url, urllib.urlencode({'id': self.id, 'pw': self.pw}))).read()
        log.i(source)
        """
        For HQM:
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <script type="text/javascript">document.cookie='utmpnum=1008'</script>
        <script type="text/javascript">document.cookie='utmpuserid=guest'</script>
        <script type="text/javascript">document.cookie='utmpkey=52169662'</script>
        <script type="text/javascript">document.cookie='utmpnum=401'</script>
        <script type="text/javascript">document.cookie='utmpkey=88906202'</script>
        <script type="text/javascript">document.cookie='utmpuserid=HQM'</script>
        <script type="text/javascript">document.cookie='my_t_lines=40'</script>
        <script type="text/javascript">document.cookie='my_link_mode=0'</script>
        <script type="text/javascript">document.cookie='my_def_mode=0'</script>
        <script type="text/javascript">document.cookie='my_img_resize=2'</script>
        <script type="text/javascript">document.cookie='my_page_mode=0'</script>
        <script language="javascript">document.location='/main.html'</script>
        """
        #return ';'.join([value for i, value in enumerate(source.split("'")[1:-2]) if 0==i%2][3:-1])
        """
        For byhhegg:
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <script type="text/javascript">document.cookie='utmpnum=1471'</script>
        <script type="text/javascript">document.cookie='utmpuserid=guest'</script>
        <script type="text/javascript">document.cookie='utmpkey=21018260'</script>
        <script type="text/javascript">document.cookie='utmpnum=397'</script>
        <script type="text/javascript">document.cookie='utmpkey=76023629'</script>
        <script type="text/javascript">document.cookie='utmpuserid=BYHHegg'</script>
        <script language="javascript">document.location='/main.html'</script>
        """
        return ';'.join([value for i, value in enumerate(source.split("'")[1:-2]) if 0 == i % 2][3:])


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
        _content = [': ' + line.strip() for i, line in enumerate(_content) if i < 7]
        re_url = source.split('[<a href=')[3].split('id')[0][1:-2]
        return _title, [hanzi('【 在 ') + _id + hanzi('的大作中提到: 】'), ] + _content, _reply.strip(), re_url

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
        req = urllib2.Request(url, urllib.urlencode({'title': self.title, 'signature': self.signature, 'start': self.start, 'text': self.text}))
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

    log.i(cookie)

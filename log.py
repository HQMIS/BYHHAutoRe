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
# 1、This Python Script is  Function for log


import os
import time
import logging


class LOG:
    def __init__(self):
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'log.txt'))
        if 0 == len(self.logger.handlers):
            self.logger.addHandler(self.handler)
        else:
            pass
        self.logger.setLevel(logging.NOTSET)

    def i(self, info):  # info
        self.logger.info(os.linesep.join(['INFO: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info]) + os.linesep)

    def e(self, error):  # error
        self.logger.error(os.linesep.join(['ERROE: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), error]) + os.linesep)


if __name__ == '__main__':
    log = LOG()
    log.i('This is test for info')
    log.e('This is test for error')

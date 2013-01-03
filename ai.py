#-*-coding:utf-8-*-

import time
from simsimi import SimSimi

print 'initing simi...'
simi = SimSimi()
print 'simi is online'

# some magic here
def magic(text):
    return simi.chat(text).encode('utf-8')

if __name__ == '__main__':
    print magic('最后一个问题')

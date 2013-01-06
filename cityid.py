#-*-coding:utf-8-*-

import requests
import cPickle as pickle

cityidDict = {}

r = requests.get('http://m.weather.com.cn/data5/city.xml')
provinceList = [province.split('|')[0] for province in r.text.split(',')]
print provinceList

for province in provinceList:
    e = requests.get('http://m.weather.com.cn/data5/city'+province+'.xml')
    cityList = [city.split('|')[0] for city in e.text.split(',')]
    print cityList
    
    for city in cityList:
        q = requests.get('http://m.weather.com.cn/data5/city'+city+'.xml')
        for county in q.text.split(','):
            flag = 1
            while flag:
                try:
                    cityidDict[county.split('|')[1]] = requests.get('http://m.weather.com.cn/data5/city'+county.split('|')[0] +'.xml').text.split('|')[1]
                    flag = 0
                except:
                    pass
#print cityidDict

print cityidDict
f = file('./cityid', 'w')
pickle.dump(cityidDict, f, True)
f.close()

if __name__ == '__main__':
    print "cityid"

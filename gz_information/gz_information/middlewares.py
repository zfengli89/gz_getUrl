import random
import base64
import json
#from settings import PROXIES

import urllib
import json
import random

import sqlite3
import math



cnt_ip =0
# get ip use local DB base
def get_ip():
    print 'run get_ip'
    while True:
        cx = sqlite3.connect("/home/sugo/IPProxys-master/data/proxy.db")
        c = cx.cursor()
        #random_num = c.execute("SELECT max(rowid) FROM proxys")
        # rows = c.execute("select * from proxys")
        max_row = c.execute("select count(*) from proxys")
        for aa in max_row:
            print aa

        row = c.execute("SELECT * FROM proxys ORDER BY RANDOM() LIMIT 1")
        print row
        #max_row = c.execute("SELECT count(*) FROM proxys")
        IP_infor = row.fetchone()
        proxy_ip = IP_infor[1]
        proxy_port = str(IP_infor[2])
        whole_ip = proxy_ip + ":" + proxy_port
        last_ip = str(whole_ip)
        print last_ip
        if last_ip is not None:
            break
    c.close()
    cx.close()
    return last_ip

# get ip use http API
'''def get_ip():
    print 'abc'
    url = "http://192.168.0.49:8000/get?num=500"

    page = urllib.urlopen(url)
    data = page.read()
    print data
    file = open("code.json","w")
    file.write(data)

    file.close()
    print "output json succeed"
    dic = json.loads(data)
    a = random.choice(dic["data"])
    print a
    b = a['ip_port']
    print b
    return b
    '''


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""#

    def __init__(self, agents):
        self.agents = agents
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
	print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):

    def process_request(self, request, spider):
        print 'run request'
        #PROXIES = [
        #             {"ip_port": "111.155.116.237:8123", "user_pass": ""}, {"ip_port": "120.15.168.146:8118", "user_pass": ""}, {"ip_port": "120.25.171.183:8080", "user_pass": ""}, {"ip_port": "60.13.74.187:843", "user_pass": ""}, {"ip_port": "183.61.236.54:3128", "user_pass": ""}, {"ip_port": "101.201.235.141:8000", "user_pass": ""}, {"ip_port": "101.231.250.102:80", "user_pass": ""}, {"ip_port": "119.53.124.91:8118", "user_pass": ""}, {"ip_port": "122.190.229.20:8118", "user_pass": ""}, {"ip_port": "114.33.202.73:8118", "user_pass": ""}, {"ip_port": "171.38.182.37:8123", "user_pass": ""}, {"ip_port": "220.166.242.152:8118", "user_pass": ""}, {"ip_port": "123.57.52.171:80", "user_pass": ""}, {"ip_port": "115.160.137.178:8088", "user_pass": ""}, {"ip_port": "171.39.234.9:80", "user_pass": ""}, {"ip_port": "222.42.230.76:80", "user_pass": ""}, {"ip_port": "123.134.196.78:80", "user_pass": ""}, {"ip_port": "111.201.197.141:8118", "user_pass": ""}, {"ip_port": "202.107.92.213:80", "user_pass": ""}
        #]
        #proxy_ip = "153.126.163.109:8000"
        proxy_ip = get_ip()
        user_pass = ""
        #proxy = random.choice(PROXIES)
        if proxy_ip is not None:
            request.meta['proxy'] = "http://%s" % proxy_ip
            encoded_user_pass = base64.encodestring(user_pass)
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy_ip
        else:
            print "**************ProxyMiddleware no pass************" + proxy_ip
            request.meta['proxy'] = "http://%s" % proxy_ip

        #proxy = random.choice(PROXIES)
        #if proxy['user_pass'] is not None:
        #    request.meta['proxy'] = "http://%s" % proxy['ip_port']
        #    encoded_user_pass = base64.encodestring(proxy['user_pass'])
        #    request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
	    #print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        #else:
	    #print "**************ProxyMiddleware no pass************" + proxy['ip_port']
        #    request.meta['proxy'] = "http://%s" % proxy['ip_port']



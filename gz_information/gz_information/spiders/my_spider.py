# -*- coding:utf-8 -*-
import scrapy
import string
import random
import math
import time
import json
import codecs
from scrapy import optional_features
from gz_information.items import GzInformationItem
#from scrapy.http.request import Request
from scrapy.http.request import Request

import sqlite3

optional_features.remove('boto')

ADD = 0
URL_NUM = 0
json_file = codecs.open('gz_sub_url_20160801_2.5w-2.6w.json', 'w', encoding='utf-8')
rest_num = 0

start_page = 25000
end_page = 26000

class gzSpider(scrapy.Spider):
    name = 'get_url'
    allow_domains = ["baidu.com"]
    start_urls = ["http://www.baidu.com"]

    def start_requests(self):
        print 'start '
        pages = []

        global start_page
        global end_page

        for i in range(start_page,end_page):
            urls = "http://cri.gz.gov.cn/Search/Result?keywords=&page=%s"%i
            page = scrapy.Request(urls, callback = self.parse, errback=self.err_parse, dont_filter=True)
            pages.append(page)
        return pages
        pass


    def parse(self, response):

        #if (str(response.__class__.__name__) == 'Response'):
        #    print(response.__class__.__name__)
        #    return Request(response.request.url, callback=self.parse,
        #            errback=self.err_parse,
        #            dont_filter=True)

        global rest_num
        rest_num = rest_num + 1
        print rest_num
        if rest_num >= 5000:
            time.sleep(40)
            rest_num = 0


        if len(response.body) < 2000 :
            return Request(response.request.url, callback=self.parse,
                    errback=self.err_parse,
                    dont_filter=True)
        items = []
        urls_items = []
        item = GzInformationItem()
        print(response.__class__.__name__)
        print type(response.__class__.__name__)
        sub_urls = response.selector.xpath(
            '/html/body/div[@class="container s-results margin-bottom-50"]/div/div[@class="col-md-10"]/div[@class="inner-results"]/h3/a/@href').extract()
        global ADD
        ADD = ADD + 1
        item['cnt'] = ADD
        item['sub_url'] = sub_urls

        for sub_url in sub_urls:
            global URL_NUM
            URL_NUM = URL_NUM + 1
            gz_url = {}
            gz_url['page'] = ADD
            gz_url['cnt'] = URL_NUM
            last_url = sub_url.encode('utf-8')
            #line = '{\"url\": \"' + sub_url + ',\"cnt\": \"' + str(URL_NUM) + '\",\"page\": \"' + str(ADD) + '\"},' + '\n'
            line = '{\"url\": \"' + sub_url + '\",\"cnt\": \"' + str(URL_NUM) + '\",\"page\": \"' + str(ADD) + '\"}' + ',\n'
            json_file.write(line)

            try:
                conn = sqlite3.connect('gz_inf.db')
                cur = conn.cursor()
                #cur.execute('create table table_gz2(cnt int, page int, url varchar(100) UNIQUE )')
                cur.execute("insert into table_gz2 values('%d','%d','%s')" %(URL_NUM,ADD,sub_url))
                conn.commit()
                cur.close()
                conn.close()
            except Exception, e:
                print "repeat"
                pass

        #print item['cnt']
        if sub_urls:
            print 'get urls success!'

        else:
            print 'get urls failture!'
            return Request(response.request.url, callback=self.parse,
                    errback=self.err_parse,
                    dont_filter=True)

        items.append(item)
        return items

    def err_parse(self,response):
        print 'run err_parse_page'
        return Request(response.request.url, callback=self.parse,
                       errback=self.err_parse,
                       dont_filter=True)




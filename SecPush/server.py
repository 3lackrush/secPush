#!/usr/bin/env python
#--*-- coding:utf-8 --*--

import json
from urllib import request
#from xml.etree.ElementTree import parse #it's not good to parse long html
import xml.etree.ElementTree as ET
from termcolor import colored
from lib.secpushSQL import secPushSQL
from lib.db import *
import ssl

class Feed(object):

    def __init__(self, data):
        self.data = data
        self.dbobj = secPushSQL(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASS,MYSQL_DBNAME)

    def _getFeed(self):
        with open(self.data, 'r') as f:
            feeddata = json.loads(f.read())
            return feeddata

    def _getSinglefeed(self):

        feed_list = self._getFeed()
        for _ in feed_list:

            parse_url = _['parse_url']
            parse_title = _['parse_title']
            parse_date = _['parse_date']
            feed_url = _['rss']
            parse_config = [feed_url, parse_url, parse_title, parse_date]
            self._getContent(parse_config)

    def _getContent(self, parse_config):
        head = {}
        head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        if parse_config[0].startswith("https"):
            context = ssl._create_unverified_context()
            req = request.Request(parse_config[0], headers=head)
            response = request.urlopen(req,context=context)
            html = response.read().decode('utf-8')
        else:
            req = request.Request(parse_config[0], headers=head)
            response = request.urlopen(req)
            html = response.read().decode('utf-8')

        doc = ET.fromstring(html)

        for item in doc.iterfind('channel/item'):
            title = item.findtext(parse_config[2])
            url = item.findtext(parse_config[1])
            date = item.findtext(parse_config[3])
            #store 2 databas
            query = (title,url,date)
            print(colored(query, "yellow"))
            self.dbobj.insert2db(query)


    def run(self):
        self._getSinglefeed()

if __name__ == '__main__':
    feedobj = Feed("./data/feed.json")
    feedobj.run()

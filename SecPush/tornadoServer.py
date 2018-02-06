#!/usr/bin/env python
#__author__ == 'Kios'

import os
from wechatpy import parse_message, create_reply
from wechatpy.replies import ArticlesReply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
	InvalidSignatureException,
)
import schedule
from datetime import timedelta
import tornado.wsgi
from tornado.options import define, options
from lib.secpushSQL import secPushSQL
from lib.db import *
from lib.ipSearch import get_location
from tornado.escape import json_encode
import datetime
import json

TOKEN = os.getenv('WECHAT_TOKEN', '#')
AES_KEY = os.getenv('WECHAT_AES_KEY', '#')
APPID = os.getenv('WECHAT_APPID', '#')

define("port", default=9000, help="run on the given port", type=int)

class WeiXinHandler(tornado.web.RequestHandler):

	def get(self):
		signature = self.get_argument('signature', '')
		timestamp = self.get_argument('timestamp', '')
		nonce = self.get_argument('nonce', '')
		echostr = self.get_argument('echostr', '')
		try:
			check_signature(TOKEN, signature, timestamp, nonce)
		except InvalidSignatureException:
			self.set_stauts('403')
			self.write('error,code 403')
		self.write(echostr)
	def post(self):
		signature = self.get_argument('signature', '')
		timestamp = self.get_argument('timestamp', '')
		nonce = self.get_argument('nonce', '')
		echostr = self.get_argument('echostr', '')
		msg = parse_message(self.request.body)
		if msg.type == 'text':
			content = msg.content.strip()
			if content == 'biu':
				try:
					datePush = '{0:%Y-%m-%d}'.format(datetime.datetime.now()) + "安全资讯推送"
					retmsg = [{"title": datePush, "url": "https://opensource.mkernel.com/view"},]
					reply = ArticlesReply(message=msg, articles=retmsg)
				except Exception as e:
					print(str(e))
				self.write(reply.render())
			elif content == 'help':
				retmsg = create_reply("1.获取最新资讯: 输入代码 biu \n2.获取ip地址信息: 输入代码 ip 1.1.1.1")
				reply = create_reply(retmsg, msg)
				self.write(reply.render())
			elif content.startswith('ip'):
				ipaddress = content.split(" ")[1]
				retmsg = create_reply(get_location(ipaddress))
				reply = create_reply(retmsg, msg)
				self.write(reply.render())
			else:
				reply = create_reply("对不起,无效的命令! 输入help查看", msg)
				self.write(reply.render())
		elif msg.type == 'event':
			help_str = "欢迎关注我的微信公众号~ 输入biu获取最新安全资讯 :)\n"
			reply = create_reply(help_str, msg)
			self.write(reply.render())

class WeixinJsonHandler(tornado.web.RequestHandler):

	def get(self):
		dbobj = secPushSQL(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASS,MYSQL_DBNAME)
		retmsg = dbobj.getFeedFromDb()
		dataobj_list = []
		for each in retmsg:
			dataobj = {}
			dataobj['title'] = each['title']
			dataobj['url'] = each['url']
			dataobj_list.append(dataobj)
		self.write(json_encode(dataobj_list))

	def post(self):
		pass


class WexinViewHandler(tornado.web.RequestHandler):

	def get(self):
		datepush = '{0:%Y-%m-%d}'.format(datetime.datetime.now())
		self.render('./templates/index.html', title="Sec Push", datepush=datepush)

	def post(self):
		pass


app = tornado.wsgi.WSGIApplication([
	(r"/", WeiXinHandler),
	(r"/json", WeixinJsonHandler),
	(r"/view", WexinViewHandler),

])

if __name__=="__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

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
from tornado.escape import json_encode
import datetime
import json

TOKEN = os.getenv('WECHAT_TOKEN', 'kevinishandsome1992')
AES_KEY = os.getenv('WECHAT_AES_KEY', 'gv6SgJQ4oZyzIzUQozBLDH3eKzgo4TyBxrVDCqGlGQ1')
APPID = os.getenv('WECHAT_APPID', 'wx780feb7a21fc82e0')

define("port", default=9000, help="run on the given port", type=int)

class WeiXinHandler(tornado.web.RequestHandler):

	#用于微信公众号网页修改基本信息时的验证
	def get(self):
		# 获取微信公众平台发送的验证参数
		signature = self.get_argument('signature', '')
		timestamp = self.get_argument('timestamp', '')
		nonce = self.get_argument('nonce', '')
		echostr = self.get_argument('echostr', '')
		try:
			check_signature(TOKEN, signature, timestamp, nonce)
		except InvalidSignatureException:
			self.set_stauts('403')
			self.write('error,code 403')
		#按照约定，如果正常，则原样返回echostr
		self.write(echostr)
	def post(self):
		# 获取微信公众平台发送的验证参数
		signature = self.get_argument('signature', '')
		timestamp = self.get_argument('timestamp', '')
		nonce = self.get_argument('nonce', '')
		echostr = self.get_argument('echostr', '')
		# 获取所有值并解析
		msg = parse_message(self.request.body)
		if msg.type == 'text':
			content = msg.content.strip()
			if content == 'biu':
				try:
					#dbobj = secPushSQL(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASS,MYSQL_DBNAME)
					#retmsg = dbobj.getFeedFromDb()
					#print(">>> ", retmsg)
					#reply = create_reply(retmsg, msg)
					#reply = TextReply(content=retmsg, message=msg)
					datePush = '{0:%Y-%m-%d}'.format(datetime.datetime.now()) + "安全资讯推送"
					retmsg = [{"title": datePush, "url": "https://opensource.mkernel.com/view"},]
					reply = ArticlesReply(message=msg, articles=retmsg)
					#dbobj.cursor.close()
					#dbobj.db.close()
				except Exception as e:
					print(str(e))
				self.write(reply.render())
			elif content == 'help':
				retmsg = create_reply("获取最新资讯: 输入代码 biu")
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
	# 这里需要根据修改为自己的URL匹配
	(r"/", WeiXinHandler),
	(r"/json", WeixinJsonHandler),
	(r"/view", WexinViewHandler),

])

if __name__=="__main__":
	# 启动tornado实例
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

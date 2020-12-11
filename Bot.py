#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import hashlib
import base64
import json
import os

con = "Recive a message form Server"
baseUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?debug=1&key="
m = json.dumps({"msgtype":"text","text":{"content":"","mentioned_list":["@all"]}})

class Bot():

	def __init__(self, key):
		'''
		A sending model using WechatBot
		'''
		self.url = baseUrl + key

	def send(self, msgtype="text", content=con, mention=True):
		'''
		Usage:

		bot = Bot(key)
		bot.useWechatBot(msgtype, content, mention=True)
		
		msgtype:
			- text 
			- markdown
			- image
		content: you text, markdown, or exist filename
			- text
			- markdown text(need Raw String)
			- filename
		mention: @all member in Group
			- True:   Enable @all
			- False:  Disable @all
		'''
		url = self.url
		data, img = {}, {"base64": None, "md5": None}
		data['msgtype'] = msgtype

		if msgtype == "text" or msgtype == "markdown":
			data[msgtype] = {"content":content}
			print(json.dumps(data))

		elif msgtype == "image":
			b64, md5 = self.baseImage(content)
			if not (b64 or md5):
				return False
			img["base64"], img["md5"] = b64, md5
			data["image"] = img

		else:
			print("[-] msgtype NOT exist")
			return False

		requests.post(url, data=json.dumps(data))
		if mention:
			requests.post(url, data=m)

		print("[+] Send Successfully")

	def baseImage(self, filename):
		'''
		- Input: 	Image Name
		- Output:	Base64encode(Image), md5(Image)
		'''
		if not os.path.exists(filename):
			print("[-] File NOT exist")
			return None, None

		with open(filename, "rb") as file:
			data = file.read()
		md5 = hashlib.md5(data).hexdigest()
		b64 = base64.b64encode(data).decode()
		return b64, md5

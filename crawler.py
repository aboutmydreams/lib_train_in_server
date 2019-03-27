import os,requests,sys,random,time
import numpy as np
from flask import Flask,redirect,url_for,render_template,request,send_file,send_from_directory
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from array import array
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

import tfmain
import make_captcha,solve_it,tfmain


train_img_path1 = 'imgs/'

def save_test_imgs(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list[::10]:
        if file != '.DS_Store':
            img = Image.open(train_img_path + file)
            img = solve_it.dele_noise(img, N=2, Z=1)
            img = solve_it.clear_lib_line(img)
            img_list = solve_it.cut_img_to_img_list(img,30,background=255)
            for k,i in enumerate(img_list):
                random_num = str(time.time())[-10:-3].replace('.',str(random.random())[2:4])
                i.save('test_imgs/{}.png'.format(file[k]+'-'+random_num))
        os.remove(train_img_path + file)

def save_train_imgs(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list:
        if file != '.DS_Store':
            img = Image.open(train_img_path + file)
            img = solve_it.dele_noise(img, N=2, Z=1)
            img = solve_it.clear_lib_line(img)
            img_list = solve_it.cut_img_to_img_list(img,30,background=255)
            for k,i in enumerate(img_list):
                random_num = str(time.time())[-10:-3].replace('.',str(random.random())[2:4])
                i.save('train_imgs/{}.png'.format(file[k]+'-'+random_num))

def remove_file(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list:
        os.remove(train_img_path + file)


class ImgVerifier:

	csrf = None
	img = None


	def __init__(self,usename,password):

		self.renewSession()
		self.usename = usename
		self.password = password
		pass


	def renewSession(self):
		self.session = requests.session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
		}


	def getLoginData(self):
		self.renewSession()
		res = self.session.get("http://210.35.251.243/reader/login.php")
		soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")
		csrf = soup.select("input[name='csrf_token']")[0].get("value")

		img_res = self.session.get("http://210.35.251.243/reader/captcha.php")
		cookie = requests.utils.dict_from_cookiejar(res.cookies)
		img = Image.open(BytesIO(img_res.content))



		self.img = img
		self.csrf = csrf
		self.cookie = cookie
		return {
			"img": img,
			"csrf": csrf
		}


	def verify(self):
		try:
			code = tfmain.break_capt(self.img)
		except Exception as e:
			self.img.save('error_imgs/{}.png'.format(str(random.randint(1000,99999))))
			code = "ABCD"
			f = open('log.txt','a')
			f.write(str(e))
			f.close

		self.session.headers["Content-Type"] = "application/x-www-form-urlencoded"
		data = {
			"number": "{}".format(self.usename),
			"passwd": "{}".format(self.password),
			"captcha": code,
			"select": "cert_no",
			"returnUrl": "",
			"csrf_token": self.csrf
		}
		res = self.session.post("http://210.35.251.243/reader/redr_verify.php", data=data)
		print(code)
		res.encoding = "utf-8"
		# cookie = PHPSESSID=nqt448vldkf9eh5qpuhsndb335

		if "验证码错误" in res.text:
			# self.img.show()
			# mycode = input('输入：')
			# if len(mycode) != 4:
			# 	return False
			self.img.save('error_imgs/{}.png'.format(code + '-' + str(time.time())[-10:-3].replace('.',str(random.random())[2:4])))
			return 2,self.cookie
		elif ("读者证件不存在" in res.text) or ("密码错误" in res.text):
			self.img.save('imgs/{}.png'.format(code + '-' + str(time.time())[-10:-3].replace('.',str(random.random())[2:4])))
			return 4,self.cookie
		else:
			# self.img.save('imgs/{}.png'.format(code + '-' + str(time.time())[-10:-3].replace('.',str(random.random())[2:4])))
			return True,self.cookie

def lib_login(usename,password):
	verifier = ImgVerifier(usename,password)
	verifier.getLoginData()
	return verifier.verify()

def get_lib_img(times):
	verifier = ImgVerifier('123','123')
	n = 0
	all = 0
	for i in tqdm(range(times)):
		verifier.getLoginData()
		try:
			# print(verifier.verify())
			if verifier.verify()[0] == 4:
				n+=1
			all+=1
			print(n/all)
			
		except requests.exceptions.ConnectionError:
			pass

	f = open('log.txt','a')
	f.write('准确率:'+str(n/all) + '\n')
	f.close()

def trains(times):
	get_lib_img(times)
	save_test_imgs(train_img_path1)
	save_train_imgs(train_img_path1)
	remove_file(train_img_path1)

# data = verifier.getLoginData()
# data["img"].show()
# print(verifier.verify(a))


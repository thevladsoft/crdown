import cookielib
import urllib
import urllib2
import fileinput
import sys
import re

class CrunchyLogin(object):
	def __init__(self, config_path):
		self.cookies_path = config_path + '/cookies.txt'

	def create_cookies(self):
		cookie_jar = cookielib.MozillaCookieJar(self.cookies_path)
		cookie_jar.save()

	def try_login(self, username, password):
		cookie_jar = cookielib.MozillaCookieJar(self.cookies_path)
		cookie_jar.load()

		# Logging in
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
		opener.addheaders =[('Referer', 'https://www.crunchyroll.com/login'),
							('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'),
							('Content-Type','application/x-www-form-urlencoded')]

		url = 'https://www.crunchyroll.com/?a=formhandler'
		data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : username, 'password' : password}
		req = urllib2.Request(url, urllib.urlencode(data))
		res = opener.open(req)

		# Checking if login is succesful
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
		opener.addheaders =[('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'),
							('Connection','keep-alive')]
		url = 'http://www.crunchyroll.com/'
		req = opener.open(url)
		site = req.read()

		if re.search(username+'(?i)',site):
			cookie_jar.save()

			for line in fileinput.input(self.cookies_path,inplace =1):
				line = line.strip()
				if not 'c_visitor' in line:
					print line
			return True
		else:
			return False


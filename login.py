#!/usr/bin/env python2

import cookielib, urllib2, urllib, fileinput, sys, re

def login(username,password):
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	opener.addheaders =[('Referer', 'https://www.crunchyroll.com/login'),
						('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'),
						('Content-Type','application/x-www-form-urlencoded')]

	url = 'https://www.crunchyroll.com/?a=formhandler'
	data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : username, 'password' : password}
	req = urllib2.Request(url, urllib.urlencode(data))
	res = opener.open(req)

def main():
	cookie_jar = cookielib.MozillaCookieJar('cookies.txt')
	cookie_jar.load()
	username = raw_input('Crunchyroll username: ')
	password = raw_input('Crunchyroll password: ')
	login(username,password)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	opener.addheaders =[('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'),
						('Connection','keep-alive')]
	url = 'http://www.crunchyroll.com/'
	req = opener.open(url)
	site = req.read()

	if re.search(username+'(?i)',site):
		print 'Login successful.'
		cookie_jar.save()

		for line in fileinput.input('cookies.txt',inplace =1):
			line = line.strip()
			if not 'c_visitor' in line:
				print line
	else:
		print 'Login failed.'
		sys.exit()

if __name__ == '__main__':
	main()

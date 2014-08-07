# -*- coding: utf-8 -*-

import cookielib
import lxml
import os
import re
import sys
import urllib
import urllib2
import shutil
import subprocess
from ConfigParser import SafeConfigParser
from urlparse import urlparse
from tempfile import mkdtemp

from bs4 import BeautifulSoup
from unidecode import unidecode

from crunchy.decoder import crunchyDec
# I hate unicode, bring on python 3.3

def config(config_path):
	config = SafeConfigParser(
		defaults={'video_quality':'highest',
		'language':'English',
		'result_path':'./export',
		'retry':'3'})
	config.read(config_path + '/settings.ini')

	global video_format
	global resolution
	quality = config.get('DEFAULT', 'video_quality')
	if quality == 'android': #doesn't work?
		video_format = '107'
		resolution = '71'
	elif quality == '360p':
		video_format = '106'
		resolution = '60'
	elif quality == '480p':
		video_format = '106'
		resolution = '61'
	elif quality == '720p':
		video_format = '106'
		resolution = '62'
	elif quality == '1080p':
		video_format = '108'
		resolution = '80'
	elif quality == 'highest':
		video_format = '0'
		resolution = '0'

	global lang
	lang = config.get('DEFAULT', 'language')
	if lang == 'Espanol_Espana':
		lang = 'Espanol (Espana)'
	elif lang == 'Francais':
		lang = 'Francais (France)'
	elif lang == 'Portugues':
		lang = 'Portugues (Brasil)'
	elif lang == 'English':
		lang = 'English|English (US)'

	global result_path
	result_path = os.path.expanduser(config.get('DEFAULT', 'result_path'))

	global retry
	retry = int(config.get('DEFAULT', 'retry'))

def playerRev (url):
	global html
	html = getHTML(url)
	global player_revision
	try:
		player_revision = re.findall(r'flash\\/(.+)\\/StandardVideoPlayer.swf', html).pop()
	except IndexError:
		url = url+'?skip_wall=1' #perv
		html = getHTML(url)
		try:
			player_revision = re.findall(r'flash\\/(.+)\\/StandardVideoPlayer.swf', html).pop()
		except IndexError:
			#update every so often, only used when the original page is region-locked, but that's what _start_proxy is for
			player_revision = '20140102185427.932a69b4165d0ca944236b7ca43ae8e5' 

def getHTML (url):
	urlparse(url)
	try:
		if sys.argv[2] == 'proxy':
			opener = urllib2.build_opener(urllib2.ProxyHandler({"http" : "127.0.0.1:8118"}))
		else:
			opener = urllib2.build_opener()
	except IndexError:
		opener = urllib2.build_opener()
	opener.addheaders =[('Referer', 'http://crunchyroll.com/'),('Host','www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)')]
	res = opener.open(url).read()
	return res

def getXML (req, media_id):
	url = 'http://www.crunchyroll.com/xml/'
	if req == 'RpcApiSubtitle_GetXml':
		data = {'req' : 'RpcApiSubtitle_GetXml', 'subtitle_script_id' : media_id}
	elif req == 'RpcApiVideoPlayer_GetStandardConfig':
		data = {'req' : 'RpcApiVideoPlayer_GetStandardConfig','media_id' : media_id,'video_format' : video_format,'video_quality' : resolution,'auto_play' : '1','show_pop_out_controls' : '1','current_page' : 'http://www.crunchyroll.com/'}
	else:
		data = {'req' : req, 'media_id' : media_id, 'video_format' : video_format, 'video_encode_quality' : resolution}
	cookie_jar = cookielib.MozillaCookieJar('cookies.txt')
	cookie_jar.load()
	cookie = urllib2.HTTPCookieProcessor(cookie_jar)
	try:
		if sys.argv[2] == 'proxy':
			opener = urllib2.build_opener(urllib2.ProxyHandler({"http" : "127.0.0.1:8118"}), cookie)
		else:
			opener = urllib2.build_opener(cookie)
	except IndexError:
		opener = urllib2.build_opener(cookie)
	opener.addheaders =[('Referer', 'http://static.ak.crunchyroll.com/flash/'+player_revision+'/StandardVideoPlayer.swf'),('Host','www.crunchyroll.com'),('Content-type','application/x-www-form-urlencoded'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)')]
	req = urllib2.Request(url, urllib.urlencode(data))
	res = opener.open(req).read()
	return res

def vidurl(url): #experimental, although it does help if you only know the program page.
	res = getHTML(url)
	slist = re.findall('<a href="#" class="season-dropdown content-menu block text-link strong(?: open| ) small-margin-bottom" title="(.+?)"',res)
	if slist != []: #multiple seasons
		if len(re.findall('<a href=".+episode-(01|1)-(.+?)"',res)) > 1: #dirty hack, I know
#			print list(reversed(slist))
#			seasonnum = int(raw_input('Season number: '))
			seasonnum = sys.argv[3]
#			epnum = raw_input('Episode number: ')
			epnum = sys.argv[2]
			seasonnum = slist[seasonnum]
			if url.endswith('/'):
				return url+re.findall('<a href=".+episode-(0'+epnum+'|'+epnum+')-(.+?)"',res)[slist.index(seasonnum)][1]
			else:
				return url+'/'+re.findall('<a href=".+episode-(0'+epnum+'|'+epnum+')-(.+?)"',res)[slist.index(seasonnum)][1]
		else:
#			print list(reversed(re.findall('<a href=".+episode-(.+?)-',res)))
#			epnum = raw_input('Episode number: ')
			epnum = sys.argv[2]
			if url.endswith('/'):
				url = url+re.findall('<a href=".+episode-(0'+epnum+'|'+epnum+')-(.+?)"',res).pop()[1]
			else:
				url = url+'/'+re.findall('<a href=".+episode-(0'+epnum+'|'+epnum+')-(.+?)"',res).pop()[1]
			print url
			return url
	else:
#		print re.findall('<a href=".+episode-(.+?)-',res)
#		epnum = raw_input('Episode number: ')
		epnum = sys.argv[2]
		if url.endswith('/'):
			url = url+re.findall('<a href=".+episode-(0'+epnum+'|'+epnum+')-(.+?)"',res).pop()[1]
		else:
			url = url+'/'+re.findall('<a href=".+episode-(0'+epnum+'|'+epnum+')-(.+?)"',res).pop()[1]
		global page_url
		page_url = url
		print url
		return url

def getVideo(page_url):
	#http://www.crunchyroll.com/miss-monochrome-the-animation/episode-2-645085
	#page_url = 'http://www.crunchyroll.com/media-645085'
	if page_url.startswith('www'):
		page_url = 'http://'+page_url
	try:
		int(page_url)
		page_url = 'http://www.crunchyroll.com/media-'+page_url
	except ValueError:
		try:
			int(page_url[-6:])
		except ValueError:
			page_url = vidurl(page_url)
	playerRev(page_url)
	media_id = page_url[-6:]
	xmlconfig = BeautifulSoup(getXML('RpcApiVideoPlayer_GetStandardConfig', media_id), 'xml')
	#xmlmeta = BeautifulSoup(getXML('RpcApiVideoPlayer_GetMediaMetadata', media_id), 'xml')
	if '<code>4</code>' in xmlconfig: #this is in VideoEncode_GetStreamInfo, but better to nip it in the bud early on
		print 'Video not available in your region.'
		sys.exit()
	vid_id = xmlconfig.find('media_id').string

	#----------

	title = unicode((re.findall('<title>(.+?)</title>',html).pop().replace('Crunchyroll - Watch ','')),encoding='utf-8')
	title = unidecode(title).replace('/',' - ').replace(':','-').replace('?','.').replace('"','\'').strip()

	#----------

	# normally 'RpcApiVideoEncode_GetStreamInfo' but some first episodes f*ck up and show 1080p no matter the settings
	#xmlstream = BeautifulSoup(getXML('RpcApiVideoPlayer_GetStandardConfig', media_id), 'xml')
	try:
		host = xmlconfig.find('host').string
	except AttributeError:
		print 'Downloading 2 minute preview.'
	#	xmlmeta = BeautifulSoup(getXML('RpcApiVideoPlayer_GetMediaMetadata', media_id), 'xml')
		media_id = xmlconfig.find('media_id').string
		xmlconfig = BeautifulSoup(getXML('RpcApiVideoEncode_GetStreamInfo', media_id), 'xml')
		try:
			host = xmlconfig.find('host').string
		except AttributeError:
			sys.exit(xmlconfig.find('msg').string)

	host_grr = re.search('fplive\.net', host) #why host_grr? well, there was a time when fplive videos couldn't be downloaded, so...
	if host_grr:
		url1 = re.findall('.+/c[0-9]+', host).pop()
		url2 = re.findall('c[0-9]+\?.+', host).pop()
	else:
		url1 = re.findall('.+/ondemand/', host).pop()
		url2 = re.findall('ondemand/.+', host).pop()
	file = xmlconfig.find('file').string

	#----------

	xmllist = unidecode(unicode(getXML('RpcApiSubtitle_GetListing', media_id), 'utf-8')) #could we get rid of unidecode?
	xmllist = xmllist.replace('><','>\n<')

	if '<media_id>None</media_id>' in xmllist:
		print 'The video has hardcoded subtitles.'
		hardcoded = True
	else:
		try:
			sub_id = re.findall("id=([0-9]+)' title='.+"+lang.replace('(','\(').replace(')','\)')+"'", xmllist).pop()
			hardcoded = False
		except IndexError:
			try:
				sub_id = re.findall("id\=([0-9]+)' title='.+English", xmllist).pop() #default back to English
				print 'Language not found, reverting to English'
				hardcoded = False
			except IndexError:
				print 'The video\'s subtitles cannot be found, or are region-locked.'
				hardcoded = True

	tmpdir = mkdtemp() + '/'
	if hardcoded == False:
		xmlsub = getXML('RpcApiSubtitle_GetXml', sub_id)
		formattedSubs = crunchyDec().returnSubs(xmlsub)
		try:
			subfile = open(tmpdir+title+'.ass', 'wb')
		except IOError:
			title = title.split(' - ', 1)[0] #episode name too long, splitting after episode number
			subfile = open(tmpdir+title+'.ass', 'wb')
		subfile.write(formattedSubs.encode('utf-8-sig'))
		subfile.close()
		shutil.move(tmpdir+title+'.ass', result_path)

	#---------------

	print 'Downloading video...'
	cmd = 'rtmpdump -r "'+url1+'" -a "'+url2+'" -f "WIN 11,8,800,50" -m 15 -W "http://static.ak.crunchyroll.com/flash/'+player_revision+'/ChromelessPlayerApp.swf" -p "'+page_url+'" -y "'+file+'" -o "'+tmpdir+title+'.flv"'

	for i in range(retry+1):
		status = subprocess.call(cmd, shell=True)
		if status != 0:
			if i == retry+1: 
				if os.path.exists('error.log'):
					file = open('error.log', 'a')
				else:
					file = open('error.log', 'w')
				file.write(page_url+'\n')
				file.close()
				os.remove(tmpdir+title+'.flv')
				sys.exit('Video failed to download. Check error.log for details...')
			else:
				print 'Video failed to download, trying again. ({}/{})'.format(i+1,retry)
		else:
			shutil.move(tmpdir+title+'.flv', result_path)
			break
	shutil.rmtree(tmpdir)
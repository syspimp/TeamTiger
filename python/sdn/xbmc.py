import sys,os
import json
import urllib
import urllib2
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
from sdn import config


class xbmc():
	def __init__(self,hostname,username=config.xbmcusername,password=config.xbmcpassword,port=config.xbmcport,debug=False):
		self.hostname=hostname
		self.username=username
		self.password=password
		self.login=self.username+':'+self.password+'@'
		self.port=port
		self.debug=debug
		self.url='http://' + self.hostname + ':' + self.port + '/jsonrpc'
		self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		if self.debug: self.urlOpener.add_handler(urllib2.HTTPHandler(debuglevel=1))
		self.reqCount=1
		self.playerid=None
		self.whattype=None

		print "url is %s" % self.url

	def debugit(self,msg):
		if self.debug is not False:
			print msg

	def _router_request(self,  method, data={}, idtype=0):
		# Contruct a standard URL request for API calls
		req = urllib2.Request(self.url)

		# NOTE: Content-type MUST be set to 'application/json' for these requests
		req.add_header('Content-type', 'application/json; charset=utf-8')

		# Convert the request parameters into JSON
		reqData = json.dumps([dict(
					method=method,
					params=data,
					jsonrpc='2.0',
					id=idtype)])

		# Increment the request count ('tid'). More important if sending multiple
		# calls in a single request
		self.reqCount += 1

		# Submit the request and convert the returned JSON to objects
		dump=json.loads(self.urlOpener.open(req, reqData).read())
		print "xbmcapi._router_request = %s" % reqData
		print "xbmcapi._router_result = %s" % dump

		#return json.loads(self.urlOpener.open(req, reqData).read())
		return dump

	def play_pause(self):
		data ={}
		if not self.playerid:
			print "see whats playing first"
			return False
		else:
			data['playerid'] = self.playerid
		return self._router_request('Player.PlayPause', data)

	def get_item(self,itemtype,playerid):
		data={}
		if itemtype == 'audio':
			data['properties'] = ["title", "album", "artist", "duration", "thumbnail", "file", "fanart", "streamdetails"]
			data['playerid'] = 0
			idtype = "AudioGetItem"
			return self._router_request('Player.GetItem', data, idtype=idtype)['result']
		if itemtype == 'video':
			data['properties'] = ["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "thumbnail", "file", "fanart", "streamdetails"]
			data['playerid'] = 1
			idtype = "VideoGetItem"
			
		try:
			getitem=self._router_request('Player.GetItem', data, idtype=idtype)
			for key in getitem:
				print "key is %s" % key['result']['item']['label']
				return key['result']['item']['label']
				#for item in key['result']:
				#	print "item is %s" % item
				#	player=item['playerid']
				#	whattype=item['type']
				#	return self.get_item(whattype,player)
		except Exception, e:
			print "xmbc.get_item: i could not find out what is playing"
			for i in e:
				print i
			pass
	def what(self):
		data ={}
		whatisplaying=self._router_request('Player.GetActivePlayers', data)
		try:
			for key in whatisplaying:
				print "xbmc.what: key is %s" % key
				for item in key['result']:
					print "item is %s" % item
					self.playerid=item['playerid']
					self.whattype=item['type']
					return self.get_item(self.whattype,self.playerid)
		except Exception, e:
			print "xbmc.what: i could not find out what is playing"
			for i in e:
				print i
			pass
			

import sys,os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
from sdn import config
from sdn import access

class openstack:
  def __init__(self,osuser=config.osuser,ospass=config.ospass,tenantid=config.tenantid,oshost=config.oshost):
    self.novahost=config.oshost+':8774'
    self.keystonehost=config.oshost+':5000'
    cmds = {	'host':	self.keystonehost,
		'url':	'/v2.0/tokens',
		'method':	'POST',
		'params':	'{"auth":{"passwordCredentials":{"username": "'+osuser+'", "password":"'+ospass+'"}, "tenantId":"'+tenantid+'"}}',
		'headers':	{"Content-Type": "application/json"}
	}
    self.tenantid=tenantid
    print cmds
    try:
    	dd = access(None,None)._json_access(cmds)
	self.apitoken = dd['access']['token']['id']
	#self.apiurl = dd['access']['serviceCatalog']['nova'][0]['publicURL']
	#self.apiurlt = urlparse(dd['access']['serviceCatalog']['nova'][0]['publicURL'])
    except Exception, e:
	print "openstack execption: aaaarch"
	for i in e:
		print i
  def _poll(self,url,method='GET'):
    cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+url,
		'method':	method,
		'params':	'{"X-Auth-Token": self.apitoken}',
		'headers':	{"X-Auth-Token": self.apitoken}
	}
    try:
	print cmds
    	dd = access(None,None)._json_access(cmds)
	return dd
    except Exception, e:
	for i in e:
		print i
  def list_servers(self):
    url='/servers'
    return self._poll(url)
	
  def list_flavors(self):
    url='/flavors'
    return self._poll(url)
	
  def list_images(self):
    url='/images'
    return self._poll(url)
	
  def show_server(self,id):
    url='/servers/'+id
    return self._poll(url)

  def show_server_ips(self,id):
    url='/servers/'+id+'/ips'
    return self._poll(url)

  def show_flavor(self,id):
    url='/flavors/'+id
    return self._poll(url)

  def server_reboot(self,serverid=None,rebootType = "HARD"):
    cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+'/servers/'+serverid+'/action',
		'method':	'POST',
		'params':	'{"reboot": {"type": rebootType}}',
		'headers':	{"X-Auth-Token": self.apitoken,
				"Content-type": "application/json"}
	}
    try:
    	dd = access(None,None)._json_access(cmds)
	return dd
    except Exception, e:
	for i in e:
		print i
  def server_stop(self):
	return
  def server_start(self):
	return
  def server_pause(self):
	return
  def server_unpause(self):
	return
  def server_modify(self):
	return
  # default is ubuntu-chef-client3
  def server_boot(self,servername=None,flavorRef="http://10.55.2.155:8774/v2/938b8b2c602d4640891a61289463b168/flavors/1",imageRef="http://10.55.2.155:8774/v2/938b8b2c602d4640891a61289463b168/images/6bdffc76-c890-476d-b0f1-bf0f9229c411",secgroup='"Management"',key_name='dtaylor-openstack'):
    cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+'/servers',
		'method':	'POST',
		'params':	'{"server": {"flavorRef": "'+flavorRef+'", "personality": [{"path": "", "contents": ""}], "name": "'+servername+'", "imageRef": "'+imageRef+'", "metadata": {"Server Name": "'+servername+'"}, "security_group": '+secgroup+', "key_name": "'+key_name+'"}}',
		'headers':	{"X-Auth-Token": self.apitoken,
				"Content-type": "application/json"}
	}
    try:
    	dd = access(None,None)._json_access(cmds)
	return dd
    except Exception, e:
	for i in e:
		print i

  def server_terminate(self,serverid):
    cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+'/servers/'+serverid,
		'method':	'DELETE',
		'params':	'{}',
		'headers':	{"X-Auth-Token": self.apitoken,
				"Content-type": "application/json"}
	}
    try:
    	dd = access(None,None)._json_access(cmds)
	return dd
    except Exception, e:
	for i in e:
		print i
  def server_floatip(self,action,serverid):
	if action == "ADD":
    		cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+'/os-floating-ips',
		'method':	'POST',
		'params':	'{"pool": "nova"}',
		'headers':	{"X-Auth-Token": self.apitoken,
				"Content-type": "application/json"}
		}
    		try:
    			ips = access(None,None)._json_access(cmds)
			floatip=ips['floating_ip']['ip']
    		except Exception, e:
			for i in e:
				print i
    		cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+'/servers/'+serverid+'/action',
		'method':	'POST',
		'params':	'{"addFloatingIp": {"address": "'+floatip+'"}}',
		'headers':	{"X-Auth-Token": self.apitoken,
				"Content-type": "application/json"}
		}
    		try:
    			dd = access(None,None)._json_access(cmds)
			return floatip
    		except Exception, e:
			for i in e:
				print i
	elif action == "DEL":
    		cmds = {	'host':	self.novahost,
		'url':	'/v2/'+self.tenantid+'/servers/'+serverid+'/action',
		'method':	'POST',
		'params':	'{"removeFloatingIp": {"address": "'+floatip+'"}}',
		'headers':	{"X-Auth-Token": self.apitoken,
				"Content-type": "application/json"}
		}
    		try:
    			dd = access(None,None)._json_access(cmds)
			return dd
    		except Exception, e:
			for i in e:
				print i
		
	return

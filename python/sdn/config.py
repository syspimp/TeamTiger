
authorized_admins=['under.my.control@gmail.com','private-chat-afa0bf1e-935b-4d85-ac35-5d3471567db6@groupchat.google.com','private-chat-afa0bf1e-935b-4d85-ac35-5d3471567db6@groupchat.google.com','1marsara1@gmail.com']
rootusername='root'
rootpassword='xxxxx'
username='dtaylortest'
password='dtaylortest'
xbmcusername='xbmc'
xbmcpassword='xbmc'
xbmcport='8081'
xbmchostname='10.55.2.161'
zenossuser='admin'
zenosspass='xxxxx'
sshkey=None
# device types allowed
# these will have methods defined
device_types = ['linux','ciscoswitch','arista','ciscoasa','ciscorouter','quanta','xbmc']
zenosshost = 'http://admin3.tfound.org:8080'

# mapping of devices to access type, 
# uses device_type as a key
access_types = 	{
			'ciscoswitch':	'telnet',
			'ciscorouter':	'ssh',
			'arista':	'ssh',
			'bigip':	'soap',
			'hpswitch':	'telnet',
			'quanta':	'telnet',
			'linux':	'ssh',
			'xbmc':		'json',
			}
terminalprompts = {
			'ciscoswitch':	'#',
			'ciscorouter':	'#',
			'arista':	'#',
			'bigip':	'#',
			'hpswitch':	'#',
			'quanta':	'(Quanta) >',
			'linux':	'#',
}
logouts = {
			'ciscoswitch':	'exit',
			'ciscorouter':	'exit',
			'arista':	'exit',
			'bigip':	'exit',
			'hpswitch':	'exit',
			'quanta':	'quit',
			'linux':	'exit',
}
sites = ['tfound','dal2','iad2']
# this uses the device_type as a key
# under each type, info is in a list
tfound_devices = [{	
				'linux':	
					[{
					'hostname':	'10.55.2.155',
					'username':	rootusername,
					'password':	rootpassword,
					}],
			},
			{	'linux':	
					[{
					'hostname':	'10.55.2.161',
					'username':	rootusername,
					'password':	rootpassword,
					}],
			},
			{	'linux':
					[{
					'hostname':	'10.55.20.7',
					'username':	rootusername,
					'password':	rootpassword,
					}]
			},
			{	'xbmc':
					[{
					'hostname':	'10.55.2.161',
					'username':	xbmcusername,
					'password':	xbmcpassword,
					'port':		'8081',
					'label':	'master'
					}]
			},
			{	'xbmc':
					[{
					'hostname':	'10.55.2.102',
					'username':	xbmcusername,
					'password':	xbmcpassword,
					'port':		'8080',
					'label':	'frontroom'
					}]
			}]
dal2_devices = [{	
				'quanta':	
					[{
					'hostname':	'192.168.112.1',
					'username':	'admin',
					'password':	password,
					}],
			},
			{	'arista':	
					[{
					'hostname':	'192.168.112.4',
					'username':	username,
					'password':	password,
					}],
			},
			{	'arista':
					[{
					'hostname':	'192.168.112.5',
					'username':	username,
					'password':	password,
					}]
			}]
static_devices = dal2_devices

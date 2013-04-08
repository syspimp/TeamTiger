debug=False
room='private-chat67db6@groupchat.google.com/bot'
authorized_admins=['user1@gmail.com','user2@gmail.com']
rootusername='root'
rootpassword='xxxxx'
username='test'
password='xxxx'
xbmcusername='xbmc'
xbmcpassword='xbmc'
xbmcport='8081'
xbmchostname='10.55.2.161'
zenossuser='admin'
zenosspass='xxxx'
sshkey=None
# device types allowed
# these will have methods defined
device_types = ['hpswitch','linux','ciscoswitch','arista','ciscoasa','ciscorouter','quanta','xbmc','chefclient','chefserver']
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
					'label':	'openstack-nova',
					'port':		'22'
					}],
			},
			{	'linux':	
					[{
					'hostname':	'10.55.2.161',
					'username':	rootusername,
					'password':	rootpassword,
					'label':	'master',
					'port':		'22'
					}],
			},
			{	'chefserver':
					[{
					'hostname':	'10.55.20.7',
					'username':	rootusername,
					'password':	rootpassword,
					'label':	'chef-server',
					'port':		'22'
					}]
			},
			{	'chefclient':
					[{
					'hostname':	'10.55.20.8',
					'username':	rootusername,
					'password':	rootpassword,
					'label':	'mrtg-tftp-sdnbot',
					'port':		'22'
					}]
			},
			{	'xbmc':
					[{
					'hostname':	'10.55.2.161',
					'username':	xbmcusername,
					'password':	xbmcpassword,
					'port':		'8081',
					'label':	'masterxbmc'
					}]
			},
			{	'xbmc':
					[{
					'hostname':	'10.55.2.102',
					'username':	xbmcusername,
					'password':	xbmcpassword,
					'port':		'8080',
					'label':	'frontroom-droid'
					}]
			},
			{	'ciscorouter':
					[{
					'hostname':	'10.55.2.1',
					'username':	rootusername,
					'password':	rootpassword,
					'port':		'23',
					'label':	'gateway router'
					}]
			},
			{	'hpswitch':
					[{
					'hostname':	'10.55.2.3',
					'username':	rootusername,
					'password':	rootpassword,
					'port':		'23',
					'label':	'core switch'
					}]
			},
			]
dal2_devices = [{	
				'quanta':	
					[{
					'hostname':	'192.168.112.1',
					'username':	'admin',
					'password':	password,
					'label':	'quanta1',
					'port':		'22'
					}],
			},
			{	'arista':	
					[{
					'hostname':	'192.168.112.4',
					'username':	username,
					'password':	password,
					'label':	'arista4',
					'port':		'22'
					}],
			},
			{	'arista':
					[{
					'hostname':	'192.168.112.5',
					'username':	username,
					'password':	password,
					'label':	'arista5',
					'port':		'22'
					}]
			}]
static_devices = dal2_devices

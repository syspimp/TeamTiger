debug=True
# openstack
oshost = "10.55.2.155"
osuser = "admin"
ospass = "notarealpass"
tenantid = "938b8b2c602d4640891a61289463b168"

room='private-chat-afa0bf1e-935b-4d85-ac35-5d3471567db6@groupchat.google.com/assistantibot'
authorized_admins=['youremailhere@gmail.com','myemailhere@gmail.com']
rootusername='root'
rootpassword='notarealpass'
username='admintest'
password='admintest'
xbmcusername='xbmc'
xbmcpassword='xbmc'
xbmcport='8081'
xbmchostname='10.55.2.161'
zenossuser='admin'
zenosspass='notarealpass'
sshkey=None
# device types allowed
# these will have methods defined
device_types = ['hpswitch','linux','ciscoswitch','arista','ciscoasa','ciscorouter','quanta','xbmc','chefclient','chefserver','openstack']
zenosshost = 'http://admin3.zenoss.server:8080'

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
			'chefserver':	'ssh',
			'chefclient':	'ssh',
			'openstack':	'json',
			}
terminalprompts = {
			'ciscoswitch':	'#',
			'ciscorouter':	'#',
			'arista':	'#',
			'bigip':	'#',
			'hpswitch':	'#',
			'quanta':	'(Quanta) >',
			'linux':	'#',
			'chefserver':	'#',
			'chefclient':	'#',
}
logouts = {
			'ciscoswitch':	'exit',
			'ciscorouter':	'exit',
			'arista':	'exit',
			'bigip':	'exit',
			'hpswitch':	'exit',
			'quanta':	'quit',
			'linux':	'exit',
			'chefserver':	'exit',
			'chefclient':	'exit',
}
sshkeys = {
			'chefserver':	"/home/ubuntu/.ssh/admin-openstack.priv",
			'chefclient':	"/home/ubuntu/.ssh/admin-openstack.priv",
			'linux':	"/home/ubuntu/.ssh/id_rsa",
}
# these sites should map to data bags in chef
sites = ['tfound','dal2','iad2']

# static site configuration
# this uses the device_type as a key
# under each type, info is in a list
#
# a sites databag will contain the same structure
tfound_devices = [{	
				'openstack':	
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
			{	'linux':	
					[{
					'hostname':	'10.55.20.3',
					'username':	rootusername,
					'password':	rootpassword,
					'label':	'admin3',
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
			{	'xbmc':
					[{
					'hostname':	'10.55.2.162',
					'username':	xbmcusername,
					'password':	xbmcpassword,
					'port':		'8080',
					'label':	'basementxbmc'
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
			{	'windows':
					[{
					'hostname':	'10.55.2.162',
					'username':	rootusername,
					'password':	rootpassword,
					'port':		'8081',
					'label':	'basement'
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

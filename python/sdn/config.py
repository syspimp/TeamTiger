# device types allowed
# these will have methods defined
username='dtaylortest'
password='dtaylortest'
sshkey=None
device_types = ['ciscoswitch','arista','ciscoasa','ciscorouter','quanta']

# mapping of devices to access type, 
# uses device_type as a key
access_types = 	{
			'ciscoswitch':	'telnet',
			'ciscorouter':	'ssh',
			'arista':	'ssh',
			'bigip':	'soap',
			'hpswitch':	'telnet',
			'quanta':	'telnet',
			}
terminalprompts = {
			'ciscoswitch':	'#',
			'ciscorouter':	'#',
			'arista':	'#',
			'bigip':	'#',
			'hpswitch':	'#',
			'quanta':	'(Quanta) >',
}
logouts = {
			'ciscoswitch':	'exit',
			'ciscorouter':	'exit',
			'arista':	'exit',
			'bigip':	'exit',
			'hpswitch':	'exit',
			'quanta':	'quit',
}

# this uses the device_type as a key
# under each type, info is in a list
static_devices = [{	
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

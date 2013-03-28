#!/usr/bin/env python
# backup.py
# ref: http://lathama.net/Using_Python_and_Wiki-Tools_with_Cisco_devices
# ref: http://stackoverflow.com/questions/3586106/perform-commands-over-ssh-with-python
# usage
#  ./backup.py -h <mgmt_ip> -u <user> -p <pass> -t <device_type> -d <destination>
# or
#  ./backup.py --cron
import sys
import logging
logging.getLogger('backup').addHandler(logging.NullHandler())
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-x", "--connect", type="string", dest="HOST", help="Host device to connect to.", default=False)
parser.add_option("-u", "--user", type="string", dest="USER", help="User to use to login", default=False)
parser.add_option("-p", "--pass", type="string", dest="PASS", help="Password to use.", default=False)
parser.add_option("-t", "--type", type="string", dest="TYPE", help="Device type that Host is, options are ciscoswitch,ciscoasa,bigip,arista,hp. default ciscoswitch", default="ciscoswitch")
parser.add_option("-d", "--destination",  type="string", dest="DESTINATION", help="Directory to save the backups, underneath /var/lib/tftpboot, default is backups/", default=False)
parser.add_option("-c", "--cron", action="store_true", dest="CRON", help="Run as a cron", default=False)
parser.add_option("-k", "--key", type="string", dest="SSHKEY", help="The path to the SSH Key to use.", default=False)

class sdn:
	def __init__(self,device_type="",hostname="",username="",password="",destination="/backups",tftproot="/var/lib/tftpboot",tftpserver = "10.55.20.3"):
		# these creds should be somewhere safe, maybe imported separately from script
		self.hostname=hostname
		self.username=username
		self.password=password
		self.device_type=device_type
		self.tftpserver=tftpserver
		self.terminalprompt="#"
		self.logout="exit"
		self.connections=[]

		if options.DESTINATION != False:
			self.destination = options.DESTINATION
		else:
			self.destination = destination
		self.backupdest = "tftp://"+ self.tftpserver + "/" + self.destination + "/" + self.hostname + ".cfg"
		# device types to backup
		self.device_types = ['ciscoswitch','arista','ciscoasa','ciscorouter','quanta']

		# mapping of devices to access type, 
		# uses device_type as a key
		self.access_types = 	{
					'ciscoswitch':	'telnet',
					'ciscorouter':	'ssh',
					'arista':	'ssh',
					'bigip':	'soap',
					'hpswitch':	'telnet',
					'quanta':	'telnet',
					}

		# this uses the device_type as a key
		self.static_devices = [{	
						'quanta':	
							[{
							'hostname':	'192.168.112.1',
							'username':	'admin',
							'password':	'xxxx',
							}],
					},
					{	'arista':	
							[{
							'hostname':	'192.168.112.4',
							'username':	'dtaylortest',
							'password':	'xxxx',
							}],
					},
					{	'arista':
							[{
							'hostname':	'192.168.112.5',
							'username':	'dtaylortest',
							'password':	'xxxx',
							}]
					}]
	def check_device_type(self):
		# device types are functions which perform the work
		# so we make sure the device_type is known
		checkit = self.device_type
		if checkit not in self.device_types:
			print "Device Type %s" % checkit
			raise Exception("Device Type is not known")
	
		if checkit not in self.access_types:
			print "Access Type %s" % checkit
			raise Exception("Access Type  is not known")

	def prepare_tftproot(self):
		#is the file there? chmod'ed 777 ?
		print "TFTP preparing!"
		return
	def perform_backup_cron(self):
			print "Cron job started ... "
			chef_devices = []
			i = 0
			for device_type in self.device_types:
				#chefarray = chef.exec("who is a " + device_type + "gimme assoc array(hostname,username,password) pls")
				chefarray = []
				for chefdev in chefarray:
					chef_devices[device_type][i] = chefdev
					i=i+1
			# merge the results with static entries
			#alldevices = self.static_devices + chef_devices
			alldevices =[]
			#print self.static_devices
			# perform the backups
			print self.static_devices
			print "all devices above"
			for device_type in self.device_types:
				try:
					for staticdevs in self.static_devices:
						#print staticdevs
						#print "staticdevs"
						try:
							for staticdev in staticdevs[device_type]:
								print device_type
								print "device_type"
								print staticdev
								print "staticdev"
								self.username=staticdev["username"]
								self.password=staticdev["password"]
								self.hostname=staticdev["hostname"]
								self.device_type=device_type
								self.perform_backup()		

						except Exception,e:
							pass
#							for i in e:
#								print "Staticdev Exception is: %s" % i
				except Exception,e:
					for i in e:
						print "Staticdevs Exception is: %s" % i
				for key in alldevices:
					self.username=alldevices[device_type][key]["username"]
					self.password=alldevices[device_type][key]["password"]
					self.hostname=alldevices[device_type][key]["hostname"]
					self.device_type=device_type
					self.perform_backup()

	def perform_backup(self):
		# sanity check
		self.check_device_type()
		self.prepare_tftproot()
		print "Performing %s %s backup" % (self.device_type,self.access_types[self.device_type])
		# generate command to run
		exec("cmd=self.%s_backup()" % self.device_type)
		# execute based on access_type to device_type mapping
		exec("self._%s_access(cmd)" % self.access_types[self.device_type])

	def commit_changes(self):
		# svn commit -m "Another commit from backup cron"
		return

	def _soap_acccess(self,cmd):
		# soap request
		return

	def _ssh_access(self,cmds):
		import paramiko
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(
			paramiko.AutoAddPolicy())
		try:
			if options.SSHKEY:
				client.connect(self.hostname, 
					username=self.username, 
					password=self.password,
					timeout=5,
					key_filename=options.SSHKEY)
			else:
				client.connect(self.hostname, 
					username=self.username, 
					password=self.password,
					timeout=5)				
		except:
			client.connect(self.hostname, 
				username=self.username, 
				password=self.password,
				timeout=5)
		print "Connected!"
		for cmd in cmds:
			stdin, stdout, stderr = client.exec_command(cmd["write"])
			try:
				if cmd["read"]:
					data = stdout.read().splitlines()
					for line in data:
						if cmd["read"] in line:
							print "matched %s,breaking" % line
							break
			except:
				pass
			stdin.flush()
			data = stdout.read().splitlines()
			for line in data:
			    print line	
		try:
			stdin.close()
			client.close()
		except:
			pass
 		

	def _telnet_access(self,cmds):
		import telnetlib
		telnet_timeout = 5
		try:
			device = telnetlib.Telnet(self.hostname)
			print device.read_until("User", telnet_timeout)
			device.write(self.username + "\r")
			print device.read_until("Pass", telnet_timeout)
			device.write(self.password + "\r")
			print device.read_until(self.terminalprompt, telnet_timeout)
			if self.device_type != 'quanta':
				device.write(self.password + "terminal length 0\r")
			for cmd in cmds:
		 		device.write(cmd["write"] +"\r")     
				try:
					if cmd["read"]:
						print device.read_until(cmd["read"],telnet_timeout)
				except:
					print device.read_until(self.terminalprompt,telnet_timeout)
					
			device.write(self.logout+"\r")
			print "Completed Sucessfully"
		except Exception as e:
			for i in e:
				print "Exception is: %s" % i
	def ciscoswitch_backup(self):
		# perform cisco backup
		cmd=	[{	"write":	"copy running-config "+ self.backupdest,
				},
				{	"write":	"",
				},
				{	"write":	"",
				},
#				{	"write":	"sho ver",
#					"read":		"--More--"
#				{	"write":	"sho ver",
#					"read":		"--More--"
#				},
#				{	"write":	" ",
#				}
				]
		return cmd

	def ciscorouter_backup(self):
		# perform cisco backup
		#cmd = ["copy", "running-config", self.backupdest]
		cmd=	[{	"write":	"copy running-config "+ self.backupdest,
				},
				{	"write":	"",
				},
				{	"write":	"",
				},
				]
		return cmd

	def hpswitch_backup(self):
		return ciscorouter_backup()

	def ciscoasa_backup(self):
		# perform asa backup
		return ciscorouter_backup()

	def arista_backup(self):
		# ...
		#cmd = ["show", "version", self.backupdest]
		cmd=	[
				{	"write":	"show version",
				},
#				{	"write":	"enable",
#				},
#				{	"write":	"",
#				},
#				{	"write":	"copy running-config "+ self.backupdest,
#				},
#				{	"write":	"",
#				},
#				{	"write":	"",
#				},
				]
		return cmd
	def bigip_backup(self):
		# ...
		return
	def quanta_banIp(self,attacker):
		return
	def quanta_backup(self):
		self.terminalprompt = "(Quanta) >"
		self.logout = "quit"
		# ...
		cmd=	[	{	"write":	"show serial",
#					"read":		"--More--"
				}
				]
		return cmd
	def banIP(self,attacker):
		return
		
if __name__=='__main__':
	try:
		"""
		perform chef query to pull in devices and device_type
		however magical this may work
		will chef provide a list prior to run or are we querying it during a cron run?
		this is to query during the run
		"""
		(options, args) = parser.parse_args()
		if options.CRON == True:
			sdn().perform_backup_cron()
		else:
			# check the basic info
			if options.USER and options.HOST:
				pass
			else:
				raise Exception("Usage: python backup.py -u user -p pass -x host OR python backup.py --cron")
			print "Performing backup on device %s, type %s ... " % (options.HOST,options.TYPE)
			dobackup   = sdn(options.TYPE, options.HOST, options.USER, options.PASS)
			dobackup.perform_backup()
			dobackup.commit_changes()
	except Exception as e:
		print e

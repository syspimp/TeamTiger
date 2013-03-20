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
parser.add_option("-d", "--destination",  type="string", dest="DESTINATION", help="Directory to save the backups, underneath /var/lib/tftpboot, default is backups/", default="False")
parser.add_option("-c", "--cron", action="store_true", dest="CRON", help="Run as a cron", default=False)
parser.add_option("-k", "--key", type="string", dest="SSHKEY", help="The path to the SSH Key to use.", default=False)

class do_backup:
	def __init__(self,device_type,hostname,username,password,destination="/backups",tftproot="/var/lib/tftpboot",tftpserver = "10.55.20.3"):
		# these creds should be somewhere safe, maybe imported separately from script
		self.hostname=hostname
		self.username=username
		self.password=password
		self.device_type=device_type
		self.tftpserver=tftpserver

		if options.DESTINATION:
			self.destination = options.DESTINATION + "/" + self.hostname + ".cfg"
		else:
			self.destination = "/backups/" + self.hostname + ".cfg"
		# device types to backup
		self.device_types = ['ciscoswitch','arista','ciscoasa','ciscorouter']

		# mapping of devices to access type, 
		# uses device_type as a key
		self.access_types = {
						'ciscoswitch':	'telnet',
						'ciscorouter':	'ssh',
						'arista':		'telnet',
						'bigip':		'soap',
						'hpswitch':		'telnet'
						}

		# this uses the device_type as a key
		self.static_devices = {'ciscoswitch':	{
										'hostname':		'attlabsw1',
										'username':		'tset',
										'password':		'test'
										}}
		# sanity check
		self.check_device_type()
		self.perform_backup()

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

	def perform_backup(self):
		self.prepare_tftproot()
		# example: if device type = ciscoswitch
		# this should call ciscoswitch() function
		# and its why we check the device types above
		#self.device_type()
		#or we run it through exec
		exec("cmd = self.%s()" % self.device_type)
		self.commit_changes()

	def commit_changes(self):
		# svn commit -m "Another commit from backup cron"
		return

	def _soap_acccess(self,cmd):
		# soap request
		return

	def _ssh_access(self,cmd):
		# ref: https://pypi.python.org/pypi/spur
		import spur
		if options.SSHKEY:
			shell = spur.SshShell( hostname=self.hostname, username=self.username, password=self.password, private_key_file=options.SSHKEY)
		else:
			shell = spur.SshShell( hostname=self.hostname, username=self.username, password=self.password)
		result = shell.run(cmd)
		return result.output # prints hello

	def _telnet_access(self,cmd):
		import telnetlib
		telnet_timeout = 5

		try:
		 device = telnetlib.Telnet(self.hostname)
		 print device.read_until("Username:", telnet_timeout)
		 device.write(self.username + "\r")
		 print device.read_until("Password:", telnet_timeout)
		 device.write(self.password + "\r")
		 print device.read_until("#", telnet_timeout)
		 device.write("\r")
		 terminal = device.read_until("#")
		 device.write("term length 0\r\n")
		 device.read_until(terminal)
		 device.write
		 device.write(cmd +"\r\n")     
		 print device.read_until(terminal)
		 device.write("exit\r\n")
		 print "Completed Sucessfully"
		except:
		 print "Error Connecting.  Is " + self.HOST + " reachable?"
		 
	def ciscoswitch(self):
		# perform cisco backup
		print "Performing ciscoswitch telnet backup"
		backupdest = "tftp://"+ self.tftpserver + "/" + self.destination
		cmd = ["copy", "running-config", backupdest]
		self._telnet_access(cmd)
		return

	def ciscorouter(self):
		# perform cisco backup
		print "Performing ciscorouter ssh backup"
		backupdest = "tftp://"+ self.tftpserver + "/" + self.destination
		cmd = ["copy", "running-config", backupdest]
		self._ssh_access(cmd)
		return
	def hpswitch(self):
		print "Performing hpswitch telnet backup"
		backupdest = "tftp://"+ self.tftpserver + "/" + self.destination
		cmd = ["copy", "running-config", backupdest]
		self._telnet_access(cmd)
		return

		
	def ciscoasa(self):
		# perform asa backup
		self.ciscoasa()
		return
	def arista(self):
		# ...
		return
	def bigip(self):
		# ...
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
			alldevices = self.static_devices + chef_devices
			# perform the backups
			for device_type in self.device_types:
				for key in alldevices:
					do_backup(device_type, alldevices[device_type][key]["hostname"], alldevices[device_type][key]["username"], alldevices[device_type][key]["password"])
		else:
			# check the basic info
			if options.USER and options.HOST:
				pass
			else:
				raise Exception("Usage: python backup.py -u user -p pass -x host OR python backup.py --cron")
			print "Performing backup on device %s, type %s ... " % (options.HOST,options.TYPE)
			do_backup(options.TYPE, options.HOST, options.USER, options.PASS)
	except Exception as e:
		print e

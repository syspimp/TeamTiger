import sys,os
import logging
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
from sdn import config

class devices():
	def __init__(self,device_type,hostname,username='',password='',terminalprompt='',logout='',backupdest='',tftpserver='',destination='backups'):
		# sanity check
		self.device_type=device_type
		check_device_type()
		# lets go!
		self.hostname=hostname
		self.username=username
		self.password=password

		self.tftpserver=tftpserver
		if terminalprompt == '':
			self.terminalprompt = config.terminalprompts[device_type]
		else:
			self.terminalprompt = terminalprompt
		if logout == '':
			self.logout = config.logouts[device_type]
		else:
			self.logout = logout
		self.logout=logout
		self.destination = destination
		self.backupdest = "tftp://"+ self.tftpserver + "/" + self.destination + "/" + self.hostname + ".cfg"
		
		return

	def check_device_type(self):
		# device types are functions which perform the work
		# so we make sure the device_type is known
		checkit = self.device_type
		if checkit not in config.device_types:
			print "Device Type %s" % checkit
			raise Exception("Device Type is not known")
	
		if checkit not in config.access_types:
			print "Access Type %s" % checkit
			raise Exception("Access Type  is not known")

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
		return ciscorouter_backup(self.backupdest)

	def ciscoasa_backup(self):
		# perform asa backup
		return ciscorouter_backup(self.backupdest)

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
		# ...
		cmd=	[	{	"write":	"show serial",
#					"read":		"--More--"
				}
				]
		return cmd

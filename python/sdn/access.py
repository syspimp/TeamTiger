import sys,os
import logging
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
from sdn import config
logging.getLogger('backup').addHandler(logging.NullHandler())

class access():
	def __init__(self,device_type,hostname,username=config.username,password=config.password,sshkey=config.sshkey,debug=False):
		self.hostname=hostname
		self.username=username
		self.password=password
		self.device_type=device_type
		self.debug=debug
		self.sshkey=sshkey
	def debugit(self,msg):
		if self.debug is not False:
			print msg

	def _soap_acccess(self,cmd):
		# soap request
		return

	def _ssh_access(self,cmds):
		import paramiko
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(
			paramiko.AutoAddPolicy())
		try:
			if self.sshkey is not None:
				client.connect(self.hostname, 
					username=self.username, 
					password=self.password,
					timeout=5,
					key_filename=sshkey)
			else:
				client.connect(self.hostname, 
					username=self.username, 
					password=self.password,
					timeout=5)				
		except Exception as e:
			for i in e:
				print "Exception is: %s" % i
			return

		self.debugit("Connected!")
		for cmd in cmds:
			msg="Writing: "+cmd["write"]
			self.debugit(msg)
			stdin, stdout, stderr = client.exec_command(cmd["write"])
			try:
				if cmd["read"]:
					msg="Reading: " +cmd["read"]
					self.debugit(msg)
					data = stdout.read().splitlines()
					for line in data:
						if cmd["read"] in line:
							msg="matched "+line+",breaking"
							self.debugit(msg)
							break
			except:
				pass
			stdin.flush()
			data = stdout.read().splitlines()
			if self.debug is not False:
				for line in data:
					self.debugit(line)
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
			self.debugit(device.read_until("User", telnet_timeout))
			device.write(self.username + "\r")
			self.debugit(device.read_until("Pass", telnet_timeout))
			device.write(self.password + "\r")
			self.debugit(device.read_until(self.terminalprompt, telnet_timeout))
			if self.device_type != 'quanta':
				device.write(self.password + "terminal length 0\r")
			for cmd in cmds:
		 		device.write(cmd["write"] +"\r")     
				try:
					if cmd["read"]:
						self.debugit(device.read_until(cmd["read"],telnet_timeout))
				except:
					self.debugit(device.read_until(self.terminalprompt,telnet_timeout))
					
			device.write(self.logout+"\r")
			self.debugit("Completed Sucessfully")
		except Exception as e:
			for i in e:
				print "Exception is: %s" % i

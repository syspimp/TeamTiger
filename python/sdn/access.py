import sys,os
import logging
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
from sdn import config
logging.getLogger('backup').addHandler(logging.NullHandler())

class access():
	def __init__(self,device_type,hostname,username=config.username,password=config.password,sshkey=config.sshkey):
		self.hostname=hostname
		self.username=username
		self.password=password
		self.device_type=device_type

	def _soap_acccess(self,cmd):
		# soap request
		return

	def _ssh_access(self,cmds):
		import paramiko
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(
			paramiko.AutoAddPolicy())
		try:
			if sshkey != None:
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

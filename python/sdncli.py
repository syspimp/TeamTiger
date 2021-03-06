#!/usr/bin/python
import sdn
import sys
import paramiko
import cmd, logging
logging.getLogger('backup').addHandler(logging.NullHandler())
class sdncli(cmd.Cmd,object):
	""" Simple shell to run a command on the host """

	prompt = 'sdn > '
	debug=True

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.hosts = []
		self.connections = []
		self.timeout=5
		self.device_type=None
		
		self.defaultprompt=self.prompt

	def do_connect(self, args):
		"""Connect to all hosts in the hosts list"""
		for host in self.hosts:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(
				paramiko.AutoAddPolicy())
			try:
				client.connect(host[0], 
					username=host[1], 
					password=host[2],
					timeout=5)
				self.connections.append(client)
				self.prompt = self.prompt.replace('>','#')
			except:
				print "could not connect to %s" % host[0]

	def do_run(self, command):
		"""run 
		Execute this command on all hosts in the list"""
		if command:
			for host, conn in zip(self.hosts, self.connections):
				stdin, stdout, stderr = conn.exec_command(command)
				stdin.close()
				for line in stdout.read().splitlines():
					print 'host: %s: %s' % (host[0], line)
		else:
			print "usage: run "

	def do_close(self, args):
		for conn in self.connections:
			conn.close()
		self.prompt = self.prompt.replace('#','>')



	def do_add_aristas(self,args):
		"""add_aristas
		Add all the static aristas to host list"""
		self.add_static_hosts('arista')

	def do_add_quantas(self,args):
		"""add_quantas
		Add all the static quantas to host list"""
		self.add_static_hosts('quanta')

	def add_static_hosts(self,device_type):
		self.device_type=device_type
		for staticdevs in sdn.config.static_devices:
			try:
				for staticdev in staticdevs[self.device_type]:
					self.hosts.append([staticdev["hostname"],staticdev["username"],staticdev["password"],self.device_type])
			except:
				pass
		self.prompt = 'sdn - %s > ' % self.device_type

	def do_add_host(self, args):
		"""add_host 
		Add the host to the host list"""
		if args:
			hosts=args.split(',')
			self.hosts.append(hosts)
			try:
				if hosts[3]:
					self.device_type=hosts[3]
			except:
				pass
		else:
			hostname=raw_input('host or ip?')
			username=raw_input('username?')
			password=raw_input('password?')
			device=raw_input('device_type (arista,quanta,etc)?')
			self.hosts.append([hostname,username,password])
			self.device_type=device

	def do_clear(self,args):
		"""clear
		Clears the host list, prompt"""
		self.hosts = []
		self.prompt = self.defaultprompt
		self.device_type=None

	def do_backup(self, args):
		"""backup 
		performs a backup on the device"""
		if self.device_type is not None:
			for host in self.hosts:
				print "Backing up %s" % host[0]
				guardian_angel=sdn.actions(self.device_type, host[0], host[1], host[2],debug=self.debug)
				guardian_angel.perform_backup()
		else:
			print "Not connected or configured"

	def do_list(self,args):
		"""list 
		Lists all hosts in host list"""
		print "Loaded hosts:"
		print self.hosts
		print "Current Device Type is %s" % self.device_type

	def do_ban_ip(self,attacker):
		if self.device_type is not None:
			for host in self.hosts:
				banhammer=sdn.actions(self.device_type, host[0], host[1], host[2],debug=self.debug)
				banhammer.ban_ip(attacker)

	def postloop(self):
		print 'Later...'
		super(sdncli,self).postloop()

	def emptyline(self):
		return cmd.Cmd.emptyline(self)

	def do_exit(self, args):
		do_quit(args)

	def do_quit(self, args):
		if raw_input('really quit ?(y/n):')=='y':
			try:
				do_close('all')
			except:
				pass
			sys.exit(0)

if __name__ == '__main__':
	sdncli().cmdloop()


#!/usr/bin/python
import sdn
import sys
import paramiko
import cmd

class RunCommand(cmd.Cmd):
	""" Simple shell to run a command on the host """

	prompt = 'sdn > '

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.hosts = []
		self.connections = []
		self.timeout=5

	def do_add_host(self, args):
		"""add_host 
		Add the host to the host list"""
		if args:
			self.hosts.append(args.split(','))
		else:
			print "usage: host "
	def do_connect(self, args):
		"""Connect to all hosts in the hosts list"""
		for host in self.hosts:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(
				paramiko.AutoAddPolicy())
			client.connect(host[0], 
				username=host[1], 
				password=host[2],
				timeout=5)
			self.connections.append(client)
		self.prompt = self.prompt.replace('>','#')

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

	def do_add_aristas(self,args):
		"""add_aristas
		Add all the static aristas to host list"""
		aristas=[]
		s_arista=''
		for staticdevs in sdn.config.static_devices:
			#print staticdevs
			#print "staticdevs"
			try:
				for staticdev in staticdevs['arista']:
					s_arista=staticdev["hostname"] + ','+staticdev["username"]+','+staticdev["password"]
					self.hosts.append([staticdev["hostname"],staticdev["username"],staticdev["password"]])
			except:
				pass
		self.prompt = 'sdn - aristas > '


	def do_close(self, args):
		for conn in self.connections:
			conn.close()

	def do_quit(self, args):
		try:
			do_close('all')
		except:
			pass
		sys.exit(0)
if __name__ == '__main__':
	RunCommand().cmdloop()

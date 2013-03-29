from sdn import config,devices,access

class actions():
	def __init__(self,device_type='',hostname='',username=config.username,password=config.password,debug=False):
		try:
			self.device=devices(device_type,hostname,username,password)
		except:
			print "LOL give it up, you can't win!"
		self.debug=debug
		self.device_type=device_type
		self.hostname=hostname
		self.username=username
		self.password=password


	def debugit(self,msg):
		if self.debug is not False:
			print msg

	def prepare_tftproot(self):
		#is the file there? chmod'ed 777 ?
		self.debugit("TFTP preparing!")
		return

	def perform_backup_cron(self):
			self.debugit("Cron job started ... ")
			chef_devices = []
			i = 0
			for device_type in config.device_types:
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
			self.debugit("perform_backup_cron: all devices")
			self.debugit(config.static_devices)
			for device_type in config.device_types:
				try:
					for staticdevs in config.static_devices:
						try:
							for staticdev in staticdevs[device_type]:
								self.debugit("perform_backup_cron: device_type")
								self.debugit(device_type)
								self.debugit("perform_backup_cron: staticdev")
								self.debugit(staticdev)
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
		msg="Performing "+self.device_type+" "+config.access_types[self.device_type]+" backup"
		self.debugit(msg)
		# sanity check
		self.prepare_tftproot()
		
		# generate command to run
		exec("cmd=devices(self.device_type,self.hostname,self.username,self.password,debug=%s).%s_backup()" % (self.debug,self.device_type))
		# execute based on access_type to device_type mapping
		self.debugit("cmd chat script:")
		self.debugit(cmd)
		exec("access(self.device_type,self.hostname,self.username,self.password,debug=%s)._%s_access(cmd)" % (self.debug,config.access_types[self.device_type]))

	def commit_changes(self):
		# svn commit -m "Another commit from backup cron"
		return

	def ban_ip(self,attacker):
		self.debugit("Banning IP "+attacker+"! Complete!")
		return

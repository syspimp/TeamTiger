from sdn import config

class actions():
	def __init__(self,device_type,hostname,username=config.username,password=config.password):
		try:
			self.device=devices(device_type,hostname,username,password)
		except:
			print "LOL give it up, you can't win!"

	def prepare_tftproot(self):
		#is the file there? chmod'ed 777 ?
		print "TFTP preparing!"
		return
	def perform_backup_cron(self):
			print "Cron job started ... "
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
			print config.static_devices
			print "all devices above"
			for device_type in config.device_types:
				try:
					for staticdevs in config.static_devices:
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
		device.prepare_tftproot()
		print "Performing %s %s backup" % (self.device_type,self.access_types[self.device_type])
		# generate command to run
		exec("cmd=self.%s_backup()" % self.device_type)
		# execute based on access_type to device_type mapping
		exec("self._%s_access(cmd)" % self.access_types[self.device_type])

	def commit_changes(self):
		# svn commit -m "Another commit from backup cron"
		return
	def banIP(self):
		return

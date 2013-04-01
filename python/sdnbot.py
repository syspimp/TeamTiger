﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

#
# This is an sample PyGtalkRobot that serves to set the show type and status text of robot by receiving message commands.
#

import sys
import time
from sdncli import sdncli
from sdn import config
from sdn import zenossapi
from sdn import actions
from sdn import xbmc
from PyGtalkRobot import GtalkRobot
# debug switch
#bigbadbug=['nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth', 'bind', 'socket', 'CONNECTproxy', 'TLS', 'roster', 'browser', 'ibb']
bigbadbug=['socket']
#bigbadbug=[]


#bigbadbug=[]
############################################################################################################################

class SdnBot(GtalkRobot):
	
	#Regular Expression Pattern Tips:
	# I or IGNORECASE <=> (?i)      case insensitive matching
	# L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
	# M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
	# S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
	# U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
	# X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
	debug=True
	devload=sdncli()
	z=zenossapi()
	x=None
	xbmchosts=[]
	xbmcactive=0
	site=None

	#"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
	#This method is used to change the state and status text of the bot.
	def command_001_setState(self, user, message, args):
		#the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
		#The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
		'''([Aa]vailable|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
		show = args[0]
		status = args[1]
		jid = user.getStripped()

		# Verify if the user is the Administrator of this bot
		if jid in config.authorized_admins:
			print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
			self.setState(show, status)
			self.replyMessage(user, "State settings changed！")
		else:
			self.replyMessage(user, "Sorry "+jid+", your tin cans are no match for me! Access denied!")

	#This method is used to send email for users.
	def command_002_SendEmail(self, user, message, args):
		#email ldmiao@gmail.com hello dmeiao, nice to meet you, bla bla ...
		'''[email|mail|em|m]\s+(.*?@.+?)\s+(.*?),\s*(.*?)(?i)'''
		email_addr = args[0]
		subject = args[1]
		body = args[2]
		#call_send_email_function(email_addr, subject,  body)
		
		self.replyMessage(user, "\nEmail sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
	def command_003_zenossEvents(self,user,message,args):
		'''([Zz]enoss|[Zz]en)\s+(events|close)( +(.*))?$(?i)'''
		max=5
		#if args[2]:
		#    max = args[2]
		print "in zenossEvents: args1 is xx%sxx" % args[1]
		if args[1] == "events":
			#print "getting events"
			i=1
			try:
				try:
					 print "args2 is xxx%sxxx" % args[2]
					 if args[2] != None:
						max=args[2]
						max=max.lstrip()
				except:
					 print "Im passing!"
					 pass
				events=self.z.get_events()
				#print events
				for event in events['events']:

					if i >= max:
						break
					#print "----NEW EVENT---"
					ack="Ack'd: "
					evts=self.z.get_event(event['evid'])
					now=1
					for key in evts['events']:
						if now >= max:
							break
						print "doing evt %s" % key
						msg= "Event id: " +key['evid']+ "\n" + key['eventState'] + ": " + key['summary']
						self.replyMessage(user, msg)
						time.sleep(2)
						now=now+1
						#print "this is evt"
						#print 
					i=i+1
			except Exception, e:
				for i in e:
					msg="Exception: %s" % e
					self.replyMessage(user, msg)
		elif args[1] =="close":
				print "args2 is xxx%sxxx"  % args[2]
				try:
					 if args[2] != None:
						evid=args[2]
						self.replyMessage(user, "Closing event evid "+evid.lstrip())
						self.z.close_event(evid.lstrip())
					 else:
						raise Exception()
				except:
					 self.replyMessage(user, "You need to give me an evid to ack.")
	def command_004_zenossDevicess(self,user,message,args):
		'''([Zz]enoss|[Zz]en)\s+(get|add)( +(.*))?$(?i)'''
		max=5
		#if args[2]:
		#    max = args[2]
		print "in zenossDevices: args1 is xx%sxx" % args[1]
		if args[1] == "get":
			#print "getting events"
			i=1
			try:
				try:
					print "args2 is xxx%sxxx" % args[2]
					if args[2] != None:
						cmds=args[2].lstrip()
						cmds=cmds.split(',')
					else:
						cmds= ['dev',None]
				except:
					 print "Im passing!"
					 pass
				try:
					if cmds[0] == 'grp':
						try:
							if cmds[1]:
								search="/zport/dmd/Groups"+cmds[1]
							else:
								search="/zport/dmd/Groups/"
						except:
							search="/zport/dmd/Groups"
							pass
					elif cmds[0] == 'dev':
						try:
							if cmds[1]:
								search=cmds[1]
							else:
								search="/zport/dmd/Devices/"
						except:
							search="/zport/dmd/Devices/"
							pass
					elif cmds[0] == 'sys':
						try:
							if cmds[1]:
								search="/zport/dmd/Systems"+cmds[1]
							else:
								search="/zport/dmd/Systems/"
						except:
							search="/zport/dmd/Systems/"
							pass

					devices=self.z.get_devices(search)
					print devices
				except Exception, e:
					for i in e:
						msg="Exception: %s" % e
						self.replyMessage(user, msg)
					
				for device in devices['devices']:
					if i >= max:
						break
					print "here is the device"
					print device['ipAddressString']
					ip=device['ipAddressString']
					name=device['name']
					alerts=device['events']['info']['count']
					groups=''
					for group in device['groups']:
						if group:
							groups  = groups + "\n" + group['name']
					msg=name + '/' + ip + "\n"+ "Alert count:" + str(alerts) + "\nGroup membership:" + groups+"\n"
					msg+="Uid:"+device['uid']+"\n"
					msg+= "==========\n"
					print msg
					self.replyMessage(user, msg)
					time.sleep(2)
					i=i+1
			except Exception, e:
				for i in e:
					msg="Exception displaying device: %s" % e
					self.replyMessage(user, msg)
		elif args[1] =="add":
				print "args2 is xxx%sxxx"  % args[2]
				try:
					 if args[2] != None:
						devid=args[2]
						self.replyMessage(user, "Adding device "+devid.strip()+ "into zenoss for monitoring")
						self.z.add_device(devid.strip())
					 else:
						raise Exception()
				except:
					 self.replyMessage(user, "You need to give me an ip/hostname to add.")

	def command_005_listSdn(self,user,message,args):
		'''([Ss]dn)\s+(list)( +(.*))?$(?i)'''
		action=args[1]
		try:
			print "args"
			print args
			if args[2] != None:
				target=args[2]
				target=target.lstrip()
			else:
				target='all'
		except:
			pass
		if action == "list":
			try:
				if not self.devload.hosts:
					self.replyMessage(user, "You need to load a site first.")
				else:
					self.replyMessage(user, "Site " +self.site+ " is loaded.")
					for host in self.devload.hosts:
						self.replyMessage(user, "Host "+host[0] + " is loaded.")
			except:
				self.replyMessage(user, "You need to load a site first.")

	def command_06_backupSdn(self, user, message, args):
		'''([Ss]dn)\s+(backup)'''
		action=args[1]
		try:
			print "args"
			print args
			if args[2] != None:
				target=args[2]
				target=target.lstrip()
			else:
				target='all'
		except:
			pass
		if action == "backup":
			try:
				if not self.devload.hosts:
					self.replyMessage(user, "You need to load a site first.")
				else:
					for host in self.devload.hosts:
						self.replyMessage(user, "Performing backup on "+host[0])
						print host
						self.devload.device_type=host[3]
						guardian_angel=actions(host[3], host[0], host[1], host[2],debug=self.debug)
						self.replyMessage(user, "Backing up "+  host[0])
						guardian_angel.perform_backup()
			except Exception, e:
				for i in e:
					msg="Exception: %s" % e
					self.replyMessage(user, msg)
				pass

	def command_07_loadSdn(self, user, message, args):
		'''([Ss]dn)\s+(load|banip)\s+(.*?)\s+(.*?)$'''
		#'''(sdn)\s+(load|backup|banip)( +(.*))?$(?i)'''
		action=args[1]
		try:
			print "args"
			print args
			if args[2] != None:
				target=args[2]
				target=target.lstrip()
			else:
				target='all'
		except:
			pass
		if action == "load":
			if target in config.device_types or target == 'site':
				print "step 1"
				if target == 'site':
					try:
						print "args3 is xx%sxx" % args[3]
						if args[3] != None:
							self.site=args[3].lstrip()
						else:
							self.site='dal2'
						self.replyMessage(user, "Loading devices for site "+self.site)
					except:
						pass
					print "step 2"
					try:
						self.devload.hosts=[]
						for device_type in config.device_types:
							#print "device_type and static_devicse"
							#print device_type
							#print config.static_devices
							exec("sitedevs=config.%s_devices" % self.site)
							try:
								for staticdevs in sitedevs:
									#print "staticdevs"
									#print staticdevs
									try:
										for staticdev in staticdevs[device_type]:
											self.devload.hosts.append([staticdev["hostname"],staticdev["username"],staticdev["password"],device_type])
											self.replyMessage(user, "Loaded "+staticdev["hostname"])
									except:
										pass
							except:
								pass
						print self.devload.hosts
					except Exception, e:
						for i in e:
							msg="Exception: %s" % e
							self.replyMessage(user, msg)
				if target in config.device_types:
					try:
						if not self.site:
							raise Exception()
					except:
						self.replyMessage(user,"You need to pick a site first.")

					print "sdn.command_07_loadSdn: pulling in device types"
					self.devload.hosts = []
					try:
						for staticdev in config.static_devices[target]:
							self.devload.hosts.append([staticdev["hostname"],staticdev["username"],staticdev["password"],target])
							self.replyMessage(user, "Loaded "+staticdev["hostname"])
							time.sleep(1)
					except:
						msg="Device type %s is not valid." % target
						self.replyMessage(user,msg)
			else:
				print "step 4"
				self.replyMessage(user, "examples: sdn load site dal2 # load all of dal2 devices")
				self.replyMessage(user, "examples: sdn load quanta # load all quantas")
				self.replyMessage(user, "examples: sdn add_host 127.0.0.1,root,password,linux # not yet")
	def command_08_doXbmc(self, user, message, args):
		'''([Xx]bmc)\s+(switch|play|pause|what)( +(.*))?$(?i)'''
		action=args[1]
		try:
			print "args"
			print args
			if args[2] != None:
				target=args[2]
				target=target.lstrip()
			else:
				target='all'
		except:
			pass
		try:
			if self.site is None:
				raise Exception("you must pick load site that has xbmc devices.")
			# try to load the xbmcs
			if not self.xbmchosts:
				exec("sitedevs=config.%s_devices" % self.site)
				for staticdevs in sitedevs:
					print staticdevs
					print "staticdevs above. adding devs to xbmc"
					try:
						if staticdevs['xbmc']:
						   pass
					except:
						continue
					try:
						print "step 99 staticdevs[xbmc] below"
						print staticdevs['xbmc']
						#for key,val in staticdevs:
						#   if key !="xbmc":
						#     print "not adding xbmc devs"
						#     print staticdevs
						#     continue
						#   else:
						#     print "key is not xbmc"
						#     print key
						for staticdev in staticdevs['xbmc']:
							print "adding xbmc devs to hosts"
							self.xbmchosts.append([staticdev["hostname"],staticdev["username"],staticdev["password"],staticdev["port"],staticdev["label"]])
							self.replyMessage(user, "Loaded "+staticdev["label"])
						self.xbmcactive=0
						self.x=xbmc(self.xbmchosts[self.xbmcactive][0],username=self.xbmchosts[self.xbmcactive][1],password=self.xbmchosts[self.xbmcactive][2],port=self.xbmchosts[self.xbmcactive][3])
						print "xbmc connected!!"
					except Exception, e:
					    for i in e:
					        self.replyMessage(user, "xbmchosts: "+e)
					    pass
				self.replyMessage(user,"Switching to "+self.xbmchosts[self.xbmcactive][4])
						
			else:
				print "xbmchosts"
				print self.xbmchosts
				self.xbmcactive=0
				self.x=xbmc(self.xbmchosts[self.xbmcactive][0],username=self.xbmchosts[self.xbmcactive][1],password=self.xbmchosts[self.xbmcactive][2],port=self.xbmchosts[self.xbmcactive][3])
				print "xbmc connected!!"
		except Exception, e:
			for i in e:
				msg="xbmc Exception: %s" % e
				self.replyMessage(user, msg)
		if action == "play"  or action == 'pause':
			result=self.x.play_pause()
			if result:
				msg = "Toggling play/pause on "+self.xbmchosts[self.xbmcactive][0]
				self.replyMessage(user, msg)
			else:
				self.replyMessage(user,"See what's playing first")
		if action == "what":
			try:
				whatisplaying=self.x.what()
				print "xbmc what: host is below, active index below that"
				print self.xbmchosts
				print self.xbmcactive
				if whatisplaying:
					self.replyMessage(user,whatisplaying+" is playing on "+self.xbmchosts[self.xbmcactive][0])
				else:
					self.replyMessage(user,"Nothing is playing on "+self.xbmchosts[self.xbmcactive][0])
					
			except Exception, e:
				for i in e:
					self.replyMessage(user,"sdnbot.what: Exception is "+i)
				pass
		if action == 'switch':
			self.xbmcactive+=1
			try:
			  print "len of xbmchosts is %d" % len(self.xbmchosts)
			  if self.xbmcactive >= len(self.xbmchosts):
				self.xbmcactive=0
			  self.x=xbmc(self.xbmchosts[self.xbmcactive][0],username=self.xbmchosts[self.xbmcactive][1],password=self.xbmchosts[self.xbmcactive][2],port=self.xbmchosts[self.xbmcactive][3])
			  self.replyMessage(user,"Switching to "+self.xbmchosts[self.xbmcactive][4])
			  try:
					whatisplaying=self.x.what()
					print "xbmc what: host is below, active index below that"
					print self.xbmchosts
					print self.xbmcactive
					if whatisplaying:
						self.replyMessage(user,whatisplaying+" is playing on "+self.xbmchosts[self.xbmcactive][0])
					else:
						self.replyMessage(user,"Nothing is playing on "+self.xbmchosts[self.xbmcactive][0])
					
			  except Exception, e:
					for i in e:
						self.replyMessage(user,"xbmc.switch.what: Exception is "+i)
					pass

			except:
			  self.replyMessage(user,"could not switch :/")

	#This method is used to response users.
	def command_09_sayHello(self, user, message, args):
		'''([Hh]ello|[Hh]i|[Hh]ola)'''
		msg = args[0]
		self.replyMessage(user, msg)

	def command_10_sayHelp(self, user, message, args):
		'''(help|Help)'''
		msg = """
		Help:

		sdn -- SDN module to control network devices
		sdn list
		  lists current working site and devices
		sdn load site [dal2|iad]
		  load the static devices for a site
		sdn banip [attacker]
		   ban the ip for the site
		sdn backup
		  backup all devices in the site

		xbmc -- Xbox Media Center module
		xbmc what -- what is playing
		xbmc play|pause -- toggle play/pause
		
		zen -- Zenoss monitoring module
		zen get|add [grp|sys|dev],[grpname|sysname|devuid]
		  get device,systems,groups information, or add a new device to monitor.
		  example: zen get
		  example: zen get dev,/zport/dmd/Devices/Server/Linux/devices/master.tfound.org
		zen events
		  view the current alarming/alerting devices
		zen close [evid]
		  close event by passing the event id
		"""
		self.replyMessage(user, msg)

	def command_900_default(self, user, message, args):
		'''.*?(?s)(?m)'''
		#ignore
		print "user %s" % user
		print "message %s" % message
		print args
		#self.replyMessage(user, "Booyah!")

############################################################################################################################
if __name__ == "__main__":
	bot = SdnBot(debug=bigbadbug)
	bot.setState('available', "How may I help?")
	bot.start("tfound.assistant@gmail.com", "p1zz4t1m3")
	#bot.replyMessage("private-chat-afa0bf1e-935b-4d85-ac35-5d3471567db6@groupchat.google.com","Happy New Year!")

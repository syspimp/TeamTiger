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
import sdn
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
			sdn.actions.perform_backup_cron()
		else:
			# check the basic info
			if options.USER and options.HOST:
				pass
			else:
				raise Exception("Usage: python backup.py -u user -p pass -x host OR python backup.py --cron")
			print "Performing backup on device %s, type %s ... " % (options.HOST,options.TYPE)
			dobackup = sdn.actions(options.TYPE, options.HOST, options.USER, options.PASS, debug=True)
			dobackup.perform_backup()
			dobackup.commit_changes()
	except Exception as e:
		print e

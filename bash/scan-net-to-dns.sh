#!/bin/bash
# scan a subnet for snmp hostnames
# and put into bind format
DNS=/tmp/dnsrecords
COMMUNITY='attcommunity'
SUBNET='10.55.2'
LOWERRANGE=1
UPPERRANGE=254

while getopts "s:c:hl:u:" OPTION
do
    case "$OPTION" in
    	s) SUBNET=$OPTARG
    	;;
    	c) COMMUNITY=$OPTARG
    	;;
    	h) echo ; echo "usage: $0 -c community -s subnet -u upperrange -l lowerrange" ; echo ; exit 1
		;;
		l) LOWERRANGE=$OPTARG
		;;
		u) UPPERRANGE=$OPTARG
		;;
    esac
done
for i in `seq $LOWERRANGE $UPPERRANGE` ; 
do 
	IP="$SUBNET.${i}" ; 
	echo "checking $IP ..." ; 
	NAME=$(snmpget -r 1 -v 1 -c $COMMUNITY $IP sysName.0 2> /dev/null| awk '{print $4}');  
	if [ ! -z "$NAME" ] ; 
	then 
		# adjust this dns record as needed
		# the \t are tabs
		echo -e "$NAME\tIN\tA\t$IP" >> $DNS ; 
	fi 
done
echo "Your DNS records are in $DNS"
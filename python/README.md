Software Defined Network Module
===============================

The SDN python module is designed to abstract common network actions over common network devices.

There are several submodules:

config:
    This contains all user/pass information, and static device configuration.

actions:
    This contains all public functions that can be performed on devices

devices:
    This contains device specific methods to perform requested actions.

access:
    This contains methods related to various ways to access devices, ie soap, json, telnet, ssh.

zenossapi:
    Functions to interact with Zenoss monitoring tool

xbmc:
    Functions to interact with Xbox Media Center


How to Use
===========

There are several User Interfaces available to showcase how to use the SDN module:

CLI:
    Interactive command line version
XMPP Bot:
    Interactive Gtalk or Jabber capable client
Script:
    Make a one function script, ie banip.py or backup.py


SDN CLI Help
=============

The cli lets you interact directly with devices managed by the SDN module. It allows you to control more than one device at a time.

To start you will have to load devices, then you can execute commands on them.

add_host:

        add one host to the loaded device list.  comma separated ip,username,password,device_type
        sdn > add_host 192.168.1.1,root,myrootpassword,arista

clear:
        
        clear the loaded device list.

add_aristas:
    
        add all the arista devices to the loaded device list

add_quantas:
    
        add all the quantas devices to the loaded device list

list:

        list all loaded devices.

backup:

        backup all loaded devices.

ban_ip:
        
        ban ip on all loaded devices.

run:

        run a command on all loaded devices:
        sdn - ciscorouter > run show version

exit|quit:

        quit the application.

SDN Bot Help
=============

sdn -- SDN module to control network devices

sdn list

    lists current working site and devices

sdn load site [dal2|iad]

    load the static devices for a site

snd load [device_type or label]

    loads a specific group of device types, ie ciscorouter, or a single device

sdn banip [attacker]

    ban the ip on the loaded devices

sdn backup

    backup all devices in the loaded device list


xbmc -- Xbox Media Center module

xbmc what

    see what is playing

xbmc play|pause

    toggle play/pause

xbmc switch
    
    switch to the next xbmc server in the list


zen -- Zenoss monitoring module

zen get|add [grp|sys|dev],[grpname|sysname|devuid]

    get device,systems,groups information, or add a new device to monitor.

    example: zen get

    example: zen get dev,/zport/dmd/Devices/Server/Linux/devices/master.tfound.org

zen events

    view the current alarming/alerting devices

zen close [evid]

    close event by passing the event id


chef -- Chef command module

chef bootstrap [target] runlist="cookbook1,cookbook2"

    performs a knife bootstrap command on the chef-server type

chef knife [cmds]

    wrapper for general knife commands
                                                  

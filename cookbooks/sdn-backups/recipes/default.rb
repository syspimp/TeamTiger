#
# Cookbook Name:: sdn-backups
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
# find all network devices
nodes = search(:node, "dmi_systems_manufacturer:Arista AND tags:backup")

# create the cron
nodes.each do |netdevice|
	template '/etc/cron.d/#{netdevice}.cron' do
  		source    'backup.py.erb'
		variables ({:username	=> node['username'],
					:password	=> node['password'],
					:target		=>	netdevice
				})
		action :create
	end
end

# find all network devices
nodes = search(:node, "dmi_systems_manufacturer:Arista AND tags:backup")

# create the cron
<nodes.each do |node| -%>
0 0 * * * root /usr/bin/python /opt/scripts/backup.py -x <%= node['hostname'] %> -u <%= username %> -p <%= password %>
<% end -%>
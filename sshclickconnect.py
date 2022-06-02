#!/usr/bin/env python3

from os import path,listdir

hosts = {}

# Default path for SSH config file
default_ssh_config_path = path.expanduser('~') + "/.ssh/config"

# Default command to start ssh session
# Possible alternative:
# default_ssh_command = "x-terminal-emulator -e ssh"
default_ssh_command = "terminator -x ssh"

# Icons for extension and entries
# Available icon names can be taken from here https://commons.wikimedia.org/wiki/GNOME_Desktop_icons
extension_icon = "network-idle"
host_icon = "utilities-terminal"

def gather_includes_from_config():
    """
    gather_includes_from_config checks for any includes inside ssh config file.

    :return: Dictionary with all include entries divided by type (file and directory)
    """
    with open(default_ssh_config_path) as f:
        content = f.read().splitlines()
    includes = {}
    for line in content:
        # Check for directory includes
        if line.startswith("Include") and line.endswith("*"):
            includes["directory"] = line.split(" ")[1].replace("~","%s" % path.expanduser('~')).replace("*","")
        # Check for file includes
        elif line.startswith("Include") and not line.endswith("*"):
            includes["files"] = line.split(" ")[1].replace("~","%s" % path.expanduser('~'))
    return includes

def gather_hosts_from_config(file_path):
    """
    gather_hosts_from_config gathers all hosts from a ssh config file and store them into dictionary.

    :file_path: Path to config file to read from.
    """    
    # Read file and store into variable
    with open(file_path, 'r') as f:
        add_content = f.read().splitlines()

    # Extract filename from path and set as category inside hosts
    temp_list = str(file_path).split("/")
    category = str(temp_list[len(temp_list) -1])
    hosts[category] = []
        
    # Extract hostname and store inside category based on filename
    for line in add_content:
        if line.startswith("Host "):
            ssh_host = (line.split(" ")[1], host_icon, default_ssh_command + " %s" %line.split(" ")[1])
            hosts[category].append(ssh_host)

# Read default ssh config
gather_hosts_from_config(default_ssh_config_path)

# Read files from includes if present
results = gather_includes_from_config()
if (results != ''):
    for type,item in results.items():
        # If include type is directory, iterate over all files inside and read content
        if type == "directory":
            for file in listdir(item):
                file_path = f"{item}{file}"
                gather_hosts_from_config(file_path)
        # If include type is file, read content of it
        if type == "files":
            gather_hosts_from_config(item)

# Show extension only as icon in taskbar
print(" | iconName=%s \n---" % extension_icon)

# Output all SSH hosts into category
for category, hosts in sorted(hosts.items()):
    print(category)
    for host in sorted(hosts):
        # Do not show wildcard entry in list
        if host[0] != "*":
            print("--%s | useMarkup=false iconName=%s bash='%s' terminal=false" % host)

print("---")
# Refresh button
print("Refresh... | refresh=true")

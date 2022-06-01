#!/usr/bin/env python3

from os import path,listdir

hosts = {}

# Default path for SSH config file
default_ssh_config_path = path.expanduser('~') + "/.ssh/config"

# icons
host_icon = "utilities-terminal"
extension_icon = "network-idle"

# check for active include lines and return path for it
def read_add_config_files():
    additional_ssh_config_dir = ""
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

def read_text_file(file_path):
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
            ssh_host = (line.split(" ")[1], host_icon, "terminator -x ssh %s" %line.split(" ")[1])
            hosts[category].append(ssh_host)

# Read default ssh config
read_text_file(default_ssh_config_path)

# Read files from includes if present
results = read_add_config_files()
if (results != ''):
    for type,item in results.items():
        # if include type is directory, iterate over all files inside and read content
        if type == "directory":
            for file in listdir(item):
                file_path = f"{item}{file}"
                read_text_file(file_path)
        # if include type is file, read content of it
        if type == "files":
            read_text_file(item)

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

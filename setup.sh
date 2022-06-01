#!/usr/bin/env bash

set -e

# Clone repository
if [[ -d "/home/$(whoami)/.local/share/gnome-shell/extensions/argos/argos@pew.worldwidemann.com" ]]; then
  cd "/home/$(whoami)/.local/share/gnome-shell/extensions/argos/argos@pew.worldwidemann.com"
  git fetch origin master
  git reset --hard origin/master
else
  git clone https://github.com/p-e-w/argos.git /home/$(whoami)/.local/share/gnome-shell/extensions/argos
fi

# Set softlink, if not present
if [[ ! -L "/home/$(whoami)/.local/share/gnome-shell/extensions/argos@pew.worldwidemann.com" ]]; then
  echo "Set softlink into correct directory..."
  ln -s /home/$(whoami)/.local/share/gnome-shell/extensions/argos/argos@pew.worldwidemann.com /home/$(whoami)/.local/share/gnome-shell/extensions/argos@pew.worldwidemann.com
fi

# Create argos config directory, if not present
if [[ ! -d "/home/$(whoami)/.config/argos" ]]; then
  echo "Create argos config directory..."
  mkdir -p /home/$(whoami)/.config/argos/
fi

# Copy python script to directory
git clone https://github.com/nliakm/sshclickconnect.git /tmp/sshclickconnect
cp /tmp/sshclickconnect/sshclickconnect.py /home/$(whoami)/.config/argos/
chmod +x /home/$(whoami)/.config/argos/sshclickconnect.py
rm -rf /tmp/sshclickconnect
echo -e '
Done!
---
Enable Argos extension:

If argos was installed the first time, restart GNOME Shell by pressing <Alt>+<F2>, then entering r.
On Wayland you have to re-login.
On some systems, you may additionally have to enable the Argos extension using GNOME Tweak Tool.'

exit 0
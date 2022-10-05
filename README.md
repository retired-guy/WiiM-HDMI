# WiiM-HDMI
Display now playing info from WiiM streamer to HDMI display

Instructions to install on the Inovato Quadra, an inexpensive Armbian box which is currently available, unlike the Raspberry Pi.

Open a terminal window

sudo apt update

sudp apt upgrade

sudo apt install python3-pip

sudo apt install python3-tk

git clone https://github.com/retired-guy/WiiM-HDMI.git

cd WiiM-HDMI

nano description.py

edit the IP address to that of your target WiiM, then save

From the menu Applications/Settings/Session and Startup, add an Application Autostart for the WiiM.  Select /home/quadra/WiiMHDMI/wiim.sh in the Command: input, and Trigger: on login.  Save.  (see screenshot file above).


To set up autologin, so that the WiiM Monitor app starts at bootup without a login prompt, press Ctl+Alt+F2 to open a new session.  Login as quadra.  Type 

sudo armbian-config, disable the desktop, then enable it again, but with autologin.  Save, exit and sudo reboot.  




![photo](https://raw.githubusercontent.com/retired-guy/WiiM-HDMI/main/FAB48D2B-CDA4-4798-9941-5C933B984995.jpeg)

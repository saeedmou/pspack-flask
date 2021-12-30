# pspack-flask
pOOBs4 PS4 exploit for v9.0 + automatic gold hen on Raspberry PI with lan and a Relay attached to pin 4
 
 ## About
 
This is just a repacked psOOBs4, as a flask package with the addition of automatic sending of GoldHEN. Some other small changes:

- Some magic numbers have been renamed (never looked at a PS4 bug before, and wanted to know wtf was going on)
- Some additional logging via HTTP requests (not massively useful as can't do a lot in critical section, but useful for kicking off goldenhen send)

All credit to the team behind pOOBs4

## Setup

1. Download [Python](https://www.python.org/downloads/) and install it, ideally 3.10
2. Install flask `python3 -m pip install -r requirements.txt`

## Exploiting

1. Run app `python3 app.py`. Might need to run as root to bind to port 1337
2. In the command line the IP address to navigate to will be printed e.g `* Running on http://192.168.1.200:1337/ (Press CTRL+C to quit)`
3. Navigate to port 1337 on that IP on your PS4
4. Same as psOOBs4
5. GoldHEN should be sent once the server detects success via log messages


## Help! It doesn't work on my machine

1. Try again
2. If you're not running 9.00, the exploit won't run. You'll need to modify [the template](https://github.com/mc-17/pspack-flask/blob/main/templates/index.html#L70) to match your version, or just remove the if/endif

## How to config Raspberry Pi
To run this git project on your raspberry pi do as following:
### Install and initializing the OS
1. burn the raspbbery Pi`s OS image on a sd card.
2. put a empty file named "ssh" on the boot dirve.
3. Insert the sd card in your RPi
4. config your RPi as allways (expand file system ...)
5. update and upgrade the packages
```
sudo apt-get update
sudo apt-get upgrade
```
### Config the IP and DHCP Server
1. Open DHCPCD to setup the static IP address
```
sudo nano /etc/dhcpcd.conf
```
2. Copy the following to the file then Ctrl+X, Y, enter
```
# Example static IP configuration:
interface eth0
static ip_address=192.168.1.5
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```
3. Install dnsmasq to run DHCP Server
```
sudo apt-get install dnsmasq
```
if installation failed, retry again, if it dosent work then
```
cd /home/pi/Downloads
wget http://raspbian.mirror.axinja.net/raspbian/pool/main/d/dns-root-data/dns-root-data_2021011101_all.deb
sudo dpkg -i dns-root-data_2021011101_all.deb
```
4. Config the DNSMASQ
```
sudo nano /etc/dnsmasq.conf
```
put this in it and then Ctrl+X, Y, enter
```
interface=eth0
bind-dynamic
domain-needed
bogus-priv
dhcp-range=192.168.1.71,192.168.1.75,255.255.255.0,12h
```
5. Restart the service
```
sudo service dnsmasq restart
```
6. Restart the RPi
```
sudo reboot
```
7. Now you have ssh access to your RPi with the IP=192.168.1.5
8. If you connect your PS4 to this RPi, it will get IP address from the DHCP Server on RPi

### Run the Server Script as a Service
These steps are from this [refrence](https://devstudioonline.com/article/deploy-python-flask-app-on-linux-server).
1. create Service config file 
```
sudo nano /etc/systemd/system/ps4jb.service
```
2. Put this code in it then Ctrl+X, Y, enter
```
[Unit]
Description=My PS4 J
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/Downloads/pspack-flask
ExecStart=/usr/bin/python3 /home/pi/Downloads/pspack-flask/app.py > /home/pi/Downloads/pspack-flask/log.txt
Type=idle

[Install]
WantedBy=multi-user.target
```
3. Change the service file permission to 644
```
sudo chmod 644 /etc/systemd/system/ps4jb.service
```
4. Now apply this service and enable to execute.
```
sudo systemctl daemon-reload
sudo systemctl enable ps4jb.service 
dufo systemctl start ps4jb.service
```

5. Now service is ready to use.
6. Other commands to manage the service is
    1. To Stop the app
    ```
    sudo systemctl stop ps4jb.service
    ```
    2. To Check the status of the service
    ```
    sudo systemctl status ps4jb.service
    ```
    3. To Restart the service
    ```
    sudo systemctl reload ps4jb.service
    ```
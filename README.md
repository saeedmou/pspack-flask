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
2. In the command line the IP address to navigate to will be printed e.g `* Running on http://192.168.1.100:1337/ (Press CTRL+C to quit)`
3. Navigate to port 1337 on that IP on your PS4
4. Same as psOOBs4
5. GoldHEN should be sent once the server detects success via log messages


## Help! It doesn't work on my machine

1. Try again
2. If you're not running 9.00, the exploit won't run. You'll need to modify [the template](https://github.com/mc-17/pspack-flask/blob/main/templates/index.html#L70) to match your version, or just remove the if/endif

## How to config Raspberry Pi
To run this git project on your raspberry pi do as following:
### Install and initializing the OS
1. burn the raspbbery Pi`s OS image on a sd card using Raspberry Pi Imager.
2. Define a user and set password in Raspberry Pi Imager and enable ssh.
4. Insert the sd card in your RPi
5. config your RPi as allways (expand file system ...)
6. update and upgrade the packages
```
sudo apt update
sudo apt full-upgrade
```
6. Clean old packages.
```
sudo apt autoremove
sudo apt clean
```
7. Reboot RBP
```
sudo reboot
```

### Config the IP and DHCP Server (in old OS. new one use networkMan)
1. Open DHCPCD to setup the static IP address
```
sudo nano /etc/dhcpcd.conf
```
2. Copy the following to the file then Ctrl+X, Y, enter
```
# Example static IP configuration:
interface eth0
static ip_address=192.168.1.100
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
7. Now you have ssh access to your RPi with the IP=192.168.1.100
8. If you connect your PS4 to this RPi, it will get IP address from the DHCP Server on RPi
### Clone git repository.
1. First create a Token with repo permisions "TOKEN" like:
```
ghp_BbV0GnjURK5vHNNlEOM3aSuSEwAKkd31Rabs
```
3. install git on RBP:
```
sudo apt install git
```
4. Set email and Name:
```
--global user.email "EMAIL"
--global user.name "NAME"
```
4. Goto directory:
```
cd /home/pi/
```
5. clone the repository
```
git clone https://saeedmou:TOKEN@github.com/saeedmou/pspack-flask.git
```
6. goto `pspack-flask` directory and run:
```
python3 -m pip install -r requirements.txt
```
7. Then run the following code to modify and see the results:
```
flask run --reload --host=0.0.0.0 --port=1337
```
### Run the Server Script as a Service
These steps are from this [refrence](https://devstudioonline.com/article/deploy-python-flask-app-on-linux-server).
1. create Service config file 
```
sudo nano /etc/systemd/system/ps4jb.service
```
2. Put this code in it then Ctrl+X, Y, enter
```
[Unit]
Description=PS4 Jailbreak Server
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/pspack-flask
ExecStart=/home/pi/pspack-flask/venv/bin/flask run --host=0.0.0.0 --port=1337
Environment="FLASK_APP=app.py"
Environment="PATH=/home/pi/pspack-flask/venv/bin"
Restart=always

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
sudo systemctl start ps4jb.service
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
7. Redirect port 80 to port 1337. a safe method
```
sudo apt install iptables iptables-persistent
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 1337
sudo netfilter-persistent save
```
## Development
### IDE
[Visual Studio Code](https://code.visualstudio.com/download) with these extensions by [Microsoft](https://marketplace.visualstudio.com/publishers/Microsoft):

1. [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
2. [Remote - SSH: Editing Configuration Files](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh-edit)

Add the following in .ss/config file
```
Host ps4jb
  HostName ps4jb
  User pi
```
or add the host manually.
### Making changes
First stop the service:

```
sudo systemctl stop ps4jb.service
```

Then run the following code to modify and see the results:
```
flask run --reload --host=0.0.0.0 --port=1337
```
or if Nodemon is installed:
```
nodemon --exec python3  app.py --ext py,json,css,js,htm,html
```

after finishing the modification,  press
```
CTRL+C
```
to quit and run the following or reboot the device:
```
sudo systemctl start ps4jb.service
```

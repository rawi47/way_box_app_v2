sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y hostapd ipset dnsmasq libmicrohttpd-dev python3 python3-dev python3-pip nginx-common nginx gunicorn  libpq-dev python-dev



cd opt/nodogsplash/
sudo make && make install
cd ..

pip3 install -r requirements.txt

sudo cp -rf opt/config/* /etc
sudo cp -rf opt/w.zone/ /var/www/
sudo cp -rf opt/settings/nginx/sites-available/* /etc/nginx/sites-available
sudo cp -rf opt/settings/systemd/system/middleware.service /etc/systemd/system/middleware.service

sudo ln -s /etc/nginx/sites-available/middleware /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/w.club /etc/nginx/sites-enabled

sudo systemctl daemon-reload
sudo systemctl enable middleware

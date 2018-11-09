sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y hostapd ipset dnsmasq libmicrohttpd-dev python3 python3-dev python3-pip nginx-common nginx gunicorn  libpq-dev python-dev



cd opt/nodogsplash/
sudo make && make install
cd ..

pip3 install -r requirements.txt

cp -R opt/w.zone/ /var/www/
cp -R opt/settings/nginx/sites-available/* /etc/nginx/sites-available
cp -R opt/settings/systemd/system/middleware.service /etc/systemd/system/middleware.service

ln -s /etc/nginx/sites-available/middleware /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/w.club /etc/nginx/sites-enabled

systemctl daemon-reload
systemctl enable middleware

apt-get update
apt-get -y upgrade
sudo apt-get install -y hostapd ipset dnsmasq libmicrohttpd-dev python3 python3-dev python3-pip nginx-common nginx inotify-tools



cd nodogsplash/
make && make install
cd ../

cd middleware/
pip3 install -r requirements.txt
cd ../

cd gitwatch/
install -b gitwatch.sh /opt/gitwatch
cd ../

cp -R middleware/static/config/* /etc/
cp -R w.zone/ /var/www/
ln -s /etc/nginx/sites-available/middleware /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/w.club /etc/nginx/sites-enabled

systemctl enable middleware
systemctl enable gitwatch
systemctl daemon-reload

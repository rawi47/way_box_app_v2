apt-get update
apt-get -y upgrade
apt-get install -y hostapd ipset dnsmasq libmicrohttpd-dev nginx-common nginx

rm /var/lib/dpkg/info/pi-bluetooth*
apt-get install --reinstall pi-bluetooth
apt-get install -y jq

cd nodogsplash/
make && make install
cd ../

cd middleware/
python -m pip install -r requirements.txt


cp -R static/config/* /etc/
cp -R w.zone/ /var/www/
ln -s /etc/nginx/sites-available/middleware.conf /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/wc.com.conf /etc/nginx/sites-enabled
systemctl daemon-reload
systemctl enable middleware
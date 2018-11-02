apt-get update
apt-get -y upgrade
sudo apt-get install -y hostapd ipset dnsmasq libmicrohttpd-dev python3 python3-dev python3-pip nginx-common nginx gunicorn



cd /opt/nodogsplash/
make && make install
cd ../
cd ../

cd opt/
pip3 install -r requirements.txt
cd ../


cp -R opt/w.zone/ /var/www/
cp -R opt/settings/nginx/sites-available/* /etc/nginx/sites-available
cp -R opt/settings/systemd/system/middleware.service /etc/systemd/system/middleware.service

ln -s /etc/nginx/sites-available/middleware /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/w.club /etc/nginx/sites-enabled

systemctl enable middleware
systemctl daemon-reload

echo "0 5 * * * python3 /home/pi/way_box_app_v2/update.py" >> cron
crontab cron
rm cron

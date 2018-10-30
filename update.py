import os
import middleware.way_box_app_v2.settings as settings
from  python_libs import sqlite3 as sqlite3_lib
from  python_libs import utils as utils
import base64
import requests
import configparser
import git

version = remote_version = "0.0.0"
patch = remote_patch = "0.0.0"

user = ""
password = ""
output = []

repo_dir_update = "way-box-update.ini"
repo_dir = "way_box_app_v2_lock"

url_update = 'https://api.github.com/repos/rawi47/way_box_app_v2/contents/way-box-update.ini'
url = "https://github.com/rawi47/way_box_app_v2.git"


database = settings.DATABASES['default']['NAME']

# create a database connection
conn = sqlite3_lib.create_connection(database)
with conn:
    version,patch = sqlite3_lib.select_all_by(conn,'env_config_env',"version,patch")[0]
    user,password = sqlite3_lib.select_all_by(conn,'user_user',"name,password")[0]

try:
    req = requests.get(url_update)
    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        content = base64.decodebytes(req['content'].encode())

        utils._create_file(repo_dir,content.decode(),"w")
    else:
        print('Content was not found.')

    config = configparser.ConfigParser()
    config.read(repo_dir)
    remote_version = config['DEFAULT']['version']
    remote_patch = config['DEFAULT']['patch']


    if patch < remote_patch:
        print("do patch")
    if version < remote_version:
        cmd = "mkdir " + repo_dir
        utils.run(cmd,password,output)

except Exception as e:
    print(str(e))

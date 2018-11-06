import os
import middleware.way_box_app_v2.settings as settings
from  opt.python_libs import sqlite3 as sqlite3_lib
from  opt.python_libs import utils as utils
import base64
import requests
import configparser
import git
import  _thread, time,threading
import datetime

id = 0
version = remote_version = "0.0.0"
patch = remote_patch = "0.0.0"
root_dir = ""
app_dir = ""

password = ""

repo_dir_update = ""
repo_dir = ""

url_update = ''
url = ""
middleware_dir = ""
databases_backup_dir = ""


database = settings.DATABASES['default']['NAME']


# create a database connection
conn = sqlite3_lib.create_connection(database)
with conn:
    id,version,patch,root_dir,app_dir,url,url_update,repo_dir_update,repo_dir,middleware_dir,databases_backup_dir = sqlite3_lib.select_all_by(
        conn,
        'env_config_env',
        "id,version,patch,root_dir,app_dir,git_repo,git_repo_update,repo_dir_update,repo_dir,middleware_dir,databases_backup_dir"
        )[0]
    password = sqlite3_lib.select_all_by(conn,'user_user',"password")[0]

try:
    req = requests.get(url_update)
    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        content = base64.decodebytes(req['content'].encode())

        utils._create_file(repo_dir_update,content.decode(),"w")
    else:
        print('Content was not found.')

    config = configparser.ConfigParser()
    config.read(repo_dir_update)
    remote_version = config['DEFAULT']['version']
    remote_patch = config['DEFAULT']['patch']


    if patch < remote_patch:
        print("do patch")
    if version < remote_version:
        dir = os.path.join(root_dir , app_dir , repo_dir)
        utils._create_dir(dir )

        utils._clone_git(dir,url)
        with conn:
            # res = sqlite3_lib.update_by_id(conn,"env_config_env",remote_version,remote_patch,id)
            pass



except Exception as e:
    print(str(e))

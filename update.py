import os
import middleware.way_box_app_v2.settings as settings
from  opt.python_libs import sqlite3 as sqlite3_lib
from  opt.python_libs import utils as utils
import base64
import requests
import configparser
import git,json
import  _thread, time,threading
import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
    password = sqlite3_lib.select_all_by(conn,'user_user',"password")[0][0]

try:
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)


    resp = session.get(url_update)

    data = json.loads(resp.text)


    content = base64.decodebytes(data['content'].encode())

    utils._create_file(repo_dir_update,content.decode('utf-8'),"w")

    config = configparser.ConfigParser()
    config.read(repo_dir_update)
    remote_version = config['DEFAULT']['version']
    remote_patch = config['DEFAULT']['patch']


    if patch < remote_patch:
        print("do patch")
    if version < remote_version:
        origin_dir = os.path.join(root_dir , app_dir)

        utils.pull_git(origin_dir)

        with conn:
            res = sqlite3_lib.update_by_id(conn,"env_config_env",remote_version,remote_patch,id)




except AssertionError as e:
    print(str(e))

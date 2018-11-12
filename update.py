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
import git
from git import Repo

root_dir = ""
app_dir = ""
git_repo = ""
branch = ""
api_port = 5000

database = settings.DATABASES['default']['NAME']

# create a database connection
conn = sqlite3_lib.create_connection(database)
with conn:
    root_dir,app_dir,git_repo,branch,api_port = sqlite3_lib.select_all_by(
        conn,
        'env_config_env',
        "root_dir,app_dir,git_repo,branch,api_port"
        )[0]


try:

    path = "/boxes"

    url = "http://127.0.0.1:" + str(api_port) + path
    res_obj = {"commit_hash":"master"}

    method = "GET"
    data = {}
    params = {}



    try:
        response = utils._make_request(url,method,data,params)
        res_obj = json.loads(response.text)
    except Exception as e:
        print("Python exception : " + str(e))

    dir = os.path.join(root_dir , app_dir)
    print(dir)
    if "commit_hash" in res_obj:
        branch = res_obj["commit_hash"]
    utils._pull_git(dir)
    print("done !")

except AssertionError as e:
    print(str(e))

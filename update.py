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


root_dir = ""
app_dir = ""
git_repo = ""
branche = ""
password = ""

database = settings.DATABASES['default']['NAME']

# create a database connection
conn = sqlite3_lib.create_connection(database)
with conn:
    root_dir,app_dir,git_repo,branche = sqlite3_lib.select_all_by(
        conn,
        'env_config_env',
        "root_dir,app_dir,git_repo,branche"
        )[0]
    password = sqlite3_lib.select_all_by(conn,'user_user',"password")[0][0]

try:
        origin_dir = os.path.join(root_dir , app_dir)
        utils.pull_git(origin_dir)

except AssertionError as e:
    print(str(e))

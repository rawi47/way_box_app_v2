import json, os, requests
import middleware.way_box_app_v2.settings as settings
from  opt.python_libs import sqlite3 as sqlite3_lib
from  opt.python_libs import utils as utils

root_dir = ""
app_dir = ""
git_repo = ""
branch = ""
commit_hash = ""
api_port = 5000
password = ""

database = settings.DATABASES['default']['NAME']

# create a database connection
conn = sqlite3_lib.create_connection(database)
with conn:
    root_dir,app_dir,git_repo,branch,api_port = sqlite3_lib.select_all_by(
        conn,
        'env_config_env',
        "root_dir,app_dir,git_repo,branch,api_port"
        )[0]
    password = sqlite3_lib.select_all_by(conn,'user_user',"password")[0][0]



data = {}
params = {}

path = "/connection_status/?force=True"
url = "http://127.0.0.1:" + str(api_port) + path

try:
    response = requests.get(url)
except requests.ConnectionError:
    print("connection error")


dir = os.path.join(root_dir , app_dir)
os.chdir(dir)


# cmd = "git pull origin " + branch
cmd_remote = 'git log -1 --format=%H'
cmd_local = 'git rev-parse HEAD'
lst = []

utils.run(cmd_remote,password,lst)
utils.run(cmd_local,password,lst)

for line in lst:
    print(line)

print("done !")

# if len(lst) > 3:
#     try:
#         lst = []
#         cmd = "python3 middleware/manage.py migrate "
#         utils.run(cmd,password,lst)
#         cmd = "sudo reboot "
#         utils.run(cmd,password,lst)
#     except Exception as e:
#         print("Python exception : " + str(e))

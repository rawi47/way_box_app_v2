import json, os
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


res_obj = {"commit_hash":"master"}
data = {}
params = {}

path = "/connection_status/"
url = "http://127.0.0.1:" + str(api_port) + path
method = "GET"

try:
    params = {"force":True}
    response = utils._make_request(url,method,data,params)
    print(url)
    print(params)
    print(response)
except Exception as e:
    print("Python exception : " + str(e))

dir = os.path.join(root_dir , app_dir)

os.chdir(dir)
print(dir)

if "commit_hash" in res_obj:
    commit_hash = res_obj["commit_hash"]
try:
    cmd = "git pull origin " + branch
    lst = []
    utils.run(cmd,password,lst)
except Exception as e:
    print("Python exception : " + str(e))

print("done !")

if len(lst) > 3:
    try:
        lst = []
        cmd = "python3 middleware/manage.py migrate "
        utils.run(cmd,password,lst)
        cmd = "sudo reboot "
        utils.run(cmd,password,lst)
    except Exception as e:
        print("Python exception : " + str(e))



for li in lst:
    print(li)

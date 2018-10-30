import os
import middleware.way_box_app_v2.settings as settings
from  python_libs import sqlite3 as sqlite3_lib
from  python_libs import utils as utils
import git


version = "0.0.0"
patch = "0.0.0"

repo = "/"

git_url = "https://github.com/rawi47/way_box_app_v2/contents/way-box-update.ini?ref=master"

database = settings.DATABASES['default']['NAME']

# create a database connection
conn = sqlite3_lib.create_connection(database)
with conn:
    version,patch = sqlite3_lib.select_all_by(conn,'env_config_env',"version,patch")[0]

try:
    #utils._create_file(repo,"","w")
    git.Git(repo).clone(git_url)
except Exception as e:
    print(str(e))

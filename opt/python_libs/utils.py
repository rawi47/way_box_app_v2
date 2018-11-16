import os
import subprocess
import datetime
from shutil import copy2
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def _create_file(source,content,right):
    file = open(source,right)
    file.write(content)
    file.close()

def _create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def _copy_file(src, dst):
    copy2(src, dst)

def run(command,sudo_password,lst):

    command = command.split()
    try:
        cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
        popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        while True:
            line = popen.stdout.readline()
            line_err = popen.stderr.readline()

            if len(line) > 0:
                lst.append(line.decode().strip() )
            elif  len(line_err) > 0:
                lst.append(line_err.decode().strip() )
            else:
                break

        popen.wait()

    except Exception as e:
        lst.append("OSError > " + str(e))
    except:
        lst.append ("Error > ")

    return

def _pull_git(repo_dir,branch):
    try:
        cmd = "git pull origni " + branch
    except Exception as e:
        print(e)
def _rename_folder(old_name, new_name):
    os.rename(old_name,new_name)

def _requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def _make_request(url,method,data,params):
    if method == "GET":
        res = _requests_retry_session().get(url)
    elif method == "POST":
        res = _requests_retry_session().post(url)
    return res


import os
import subprocess
import datetime
import git
from git import Repo
from shutil import copy2


def _create_file(source,content,right):
    file = open(source,right)
    file.write(content)
    file.close()

def _create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def _copy_file(src, dst):
    copy2(src, dst)

def run(command,sudo_password,printLog=True,getDate=True,shell=False):

    command = command.split()
    try:
        cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
        popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell)
        while True:
            line = popen.stdout.readline()
            line_err = popen.stderr.readline()

            if len(line) > 0:
                getD = ""
                if getDate:
                    getD = str(datetime.datetime.now()) + " - "
                print(getD + line.decode().strip() )
            elif  len(line_err) > 0:
                getD = ""
                if getDate:
                    getD = str(datetime.datetime.now()) + " - "
                print(getD + line_err.decode().strip() )
            else:
                break

        popen.wait()

    except Exception as e:
        print ("OSError > " + str(e))
    except:
        print ("Error > ")

    return

def _pull_git(branche):
    try:
        repo = Repo(".")
        repo.git.checkout(branche)
        o = repo.remotes.origin
        o.pull()
    except FileExistsError as e:
        print(e)
def _rename_folder(old_name, new_name):
    os.rename(old_name,new_name)

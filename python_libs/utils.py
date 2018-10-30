
import os
import subprocess
import datetime

def _create_file(source,content,right):
    file = open(source,right)
    file.write(content)
    file.close()

def _create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run(command,user,lst,printLog=True,getDate=True,shell=False):
    sudo_password = user.password
    #lst.append(command)
    command = command.split()
    try:
        cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
        popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,shell=shell)
        while True:
            line = popen.stdout.readline()

            if len(line) > 0:
                getD = ""
                if getDate:
                    getD = str(datetime.datetime.now()) + " - "
                lst.append(getD + line.decode().strip() )
            else:
                break

        popen.wait()

    except Exception as e:
        lst.append ("OSError > " + str(e))
    except:
        lst.append ("Error > ")

    return

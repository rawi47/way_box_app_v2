import  _thread, time,threading
import json
from boxes.models import BoxStatus
from env_config.models import Env
from user.models import User
from boxes.serializers import BoxStatusSerializer

from utils.cmd import Cmd
from utils.httpHandler import Httphandler

import logging
log = logging.getLogger(__name__)

webFunctions  = Httphandler()
cmd = Cmd()

def _save_status():

    user_obj = User.objects.order_by('id')[0]
    env_obj = Env.objects.order_by('api_key')[0]
    infos = {}
    pkgs = ["dhcpcd","dnsmasq","hostapd"]
    for line in pkgs:
        res = []
        cmd._systemctl_status(line,user_obj,res)

        message = {}
        for ln in res:
            if ":" in ln:
                param = ln.split(":")
                message[param[0]] = param[1]
        active = False
        if "Active" in message:
            if "running" in message["Active"]:
                active = True
        infos[line] = active,message


    lst = []
    cmd._ndsctl_status(user_obj,lst)

    message = {}
    for ln in lst:
        if ":" in ln:
            param = ln.split(":")
            message[param[0]] = param[1]

    active = False
    connected = 0




    if "Current clients" in message:
        active = True
        connected = message["Current clients"]

    infos["nodogsplash"] = active,message,connected


    internet_connection,internet_connection_message = cmd._is_connected("https://www.google.com")
    infos["internet_connection"] = internet_connection,internet_connection_message

    boxesStatus_obj = BoxStatus.objects.create(
        dhcpd_running= "True",
        dhcpd_message= "Bouraoui test",
        dnsmasq_running= "True",
        dnsmasq_message= "True",
        hostapd_running= "True",
        hostapd_message= "True",
        nodogsplash_running= "True",
        connected_customers= 1,
        nodogsplash_message= "True",

        internet_connection_active= "True",
        internet_connection_message= "True"

    )

    if boxesStatus_obj:
         boxesStatusSerializer = BoxStatusSerializer(boxesStatus_obj)
         response_data = boxesStatusSerializer.data


    path = "/portal/boxes/status/"
    api_port = env_obj.api_port

    url = "http://127.0.0.1:" + str(api_port) + path
    data = response_data
    method = "POST"
    params = {}


    str_data = json.dumps(data)

    data = str_data.encode('utf-8')



    try:
        t = _thread.start_new_thread( webFunctions._make_request, (url,method,data,params,) )
    except Exception as e:
        log.error("post request exception : " + str(e))

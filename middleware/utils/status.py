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
          dhcpd_running= infos["dhcpcd"][0],
          dhcpd_message= infos["dhcpcd"][1],
          dnsmasq_running= infos["dnsmasq"][0],
          dnsmasq_message= infos["dnsmasq"][1],
          hostapd_running= infos["hostapd"][0],
          hostapd_message= infos["hostapd"][1],
          nodogsplash_running= infos["nodogsplash"][0],
          connected_customers= infos["nodogsplash"][2],
          nodogsplash_message= infos["nodogsplash"][1],

          internet_connection_active= internet_connection,
          internet_connection_message= internet_connection_message

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

    data = {
            "dhcpd_running": "True",
            "dhcpd_message": "TEST",

            "dnsmasq_running": "True",
            "dnsmasq_message": "b",

            "hostapd_running": "True",
            "hostapd_message": "c",

            "nodogsplash_running": "True",
            "nodogsplash_message": "d",

            "internet_connection_active": "True",
            "internet_connection_message": "e",

            "connected_customers": 3
        }

    str_data = json.dumps(data)

    data = bytes(b'{\n            "dhcpd_running": "True",\n            "dhcpd_message": "TEST",\n\n            "dnsmasq_running": "True",\n            "dnsmasq_message": "b",\n\n            "hostapd_running": "True",\n            "hostapd_message": "c",\n\n            "nodogsplash_running": "True",\n            "nodogsplash_message": "d",\n\n            "internet_connection_active": "True",\n            "internet_connection_message": "e",\n\n            "connected_customers": 3\n        }')



    try:
        t = _thread.start_new_thread( webFunctions._make_request, (url,method,data,params,) )
    except Exception as e:
        log.error("post request exception : " + str(e))

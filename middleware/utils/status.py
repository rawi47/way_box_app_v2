import  _thread, time,threading
import json, requests
from env_config.models import Env
from utils.cmd import Cmd
from utils.httpHandler import Httphandler
import logging
log = logging.getLogger(__name__)


cmd = Cmd()
webFunctions = Httphandler()


def _save_status():


    env_obj = Env.objects.order_by('api_key')[0]
    infos = {}
    pkgs = ["dhcpcd","dnsmasq","hostapd"]
    for line in pkgs:
        res = []
        cmd._systemctl_status(line,env_obj,res)

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
    cmd._ndsctl_status(env_obj,lst)

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

    response_data = {
        "dhcpd_running": infos["dhcpcd"][0],
        "dhcpd_message": str(infos["dhcpcd"][1]),
        "dnsmasq_running": infos["dnsmasq"][0],
        "dnsmasq_message": str(infos["dnsmasq"][1]),
        "hostapd_running": infos["hostapd"][0],
        "hostapd_message": str(infos["hostapd"][1]),
        "nodogsplash_running": infos["nodogsplash"][0],
        "connected_customers": infos["nodogsplash"][2],
        "nodogsplash_message": str(infos["nodogsplash"][1]),

        "internet_connection_active": internet_connection,
        "internet_connection_message": str(internet_connection_message)
    }

    print(response_data)


    path = "/portal/boxes/status/"
    api_port = env_obj.api_port

    url = "http://127.0.0.1:" + str(api_port) + path
    data = response_data

    str_data = json.dumps(data)
    data = str_data.encode('utf-8')
    res = requests.post(url,data=data)

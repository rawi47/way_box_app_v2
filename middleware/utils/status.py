import  _thread, time,threading

from boxes.models import BoxStatus
from env_config.models import Env
from user.models import User
from boxes.serializers import BoxStatusSerializer

from utils.cmd import Cmd
from utils.httpHandler import Httphandler

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
        dhcpcd= infos["dhcpcd"][0],
        dhcpcd_message= infos["dhcpcd"][1],
        dnsmasq= infos["dnsmasq"][0],
        dnsmasq_message= infos["dnsmasq"][1],
        hostapd= infos["hostapd"][0],
        hostapd_message= infos["hostapd"][1],
        nodogsplash= infos["nodogsplash"][0],
        connected_clients= infos["nodogsplash"][2],
        nodogsplash_message= infos["nodogsplash"][1],
        internet_connection= infos["internet_connection"][0],
        branch= env_obj.branch,
        git_hash= env_obj.commit_hash

    )

    if boxesStatus_obj:
         boxesStatusSerializer = BoxStatusSerializer(boxesStatus_obj)
         response_data = boxesStatusSerializer.data


    path = "/portal/boxes/status"
    api_port = env_obj.api_port

    url = "http://127.0.0.1:" + str(api_port) + path

    method = "POST"
    params = {}

    try:
        t = _thread.start_new_thread( webFunctions._make_request, (url,method,response_data,params,) )
    except Exception as e:
        log.error("post request exception : " + str(e))

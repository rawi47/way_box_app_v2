from env_config.models import Env
from user.models import User
import json,hmac,hashlib
import requests
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
log = logging.getLogger(__name__)
from utils.cmd import Cmd
from utils.httpHandler import Httphandler
from django.shortcuts import render
from django.template import loader
from boxes.models import BoxStatus
from boxes.serializers import BoxStatusSerializer
import re
import  _thread, time,threading

webFunctions  = Httphandler()

def sign(public_key, secret_key, data):
    h = hmac.new(
        secret_key.encode('utf-8'), public_key.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    h.update(json.dumps(data, sort_keys=True).encode('utf-8'))
    return str(h.hexdigest())

@csrf_exempt
def catch_all(request,path):
    env_obj = Env.objects.order_by('api_key')[0]
    API_HOST = env_obj.api_host
    API_URL = 'https://' + API_HOST + '/'
    API_KEY = env_obj.api_key
    API_SECRET = env_obj.api_secret
    if path == 'box':
        return HttpResponse(API_KEY)

    url = API_URL + path
    data = {}



    params = {}
    data = {}



    if request.method == 'GET':
        for key, value in request.GET:
            params[key] = value
        signature = sign(API_KEY, API_SECRET, params)
    elif request.method == 'POST':
        if len(request.body) > 1:
            if len(json.loads(request.body.decode('utf-8'))) > 3:
                data = request.body.decode('utf-8')
        signature = sign(API_KEY, API_SECRET, data)
    else:
        dataOpt = {}
        signature = sign(API_KEY, API_SECRET, dataOpt)


    headers = {}
    for key, value in request.META.items():
        headers[key] = str(value)


    headers['Host'] = API_HOST
    headers['X-API-Key'] = API_KEY
    headers['X-API-Sign'] = signature


    esreq = requests.Request(method=request.method, url=url, data=request.body, params=params, headers=headers)
    resp = requests.Session().send(esreq.prepare())

    res = HttpResponse(resp.text, status= resp.status_code)

    for key, value in resp.headers.items():
        res[key] = value


    return res

def connection_status(Request):
    env_obj = Env.objects.order_by('api_key')[0]
    api_port = env_obj.api_port

    response_data,infos = _save_status()

    path = "/boxes/status"

    url = "http://raspberrypi.local:" + str(api_port) + path
    method = "POST"
    params = {}

    try:
        t = _thread.start_new_thread( webFunctions._make_request, (url,method,response_data,params,) )
    except Exception as e:
        log.error("post request exception : " + str(e))

    return HttpResponse(json.dumps(response_data),status=infos["internet_connection"][1], content_type="application/json")


def _error(request):
        template = loader.get_template('dashboard/error.html')
        boxesStatus_Serializer = {"internet_connection_message": ""}

        boxesStatus_obj = BoxStatus.objects.latest('id')
        if boxesStatus_obj:
             boxesStatusSerializer = BoxStatusSerializer(boxesStatus_obj)
             boxesStatus_Serializer = boxesStatusSerializer.data
        context = {
        'res' : boxesStatus_Serializer
        }
        return HttpResponse(template.render(context, request))


def _save_status():
    cmd = Cmd()
    user_obj = User.objects.order_by('id')[0]
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


    boxesStatus = BoxStatus(
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
        internet_connection_message= infos["internet_connection"][1]
    )
    boxesStatus.save()
    boxesStatusSerializer = BoxStatusSerializer(boxesStatus)
    response_data = boxesStatusSerializer.data

    return response_data,infos

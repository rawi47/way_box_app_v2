from env_config.models import Env
from user.models import User
import json,hmac,hashlib
import requests
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.cmd import Cmd
from utils.status import _save_status
from utils.httpHandler import Httphandler
from django.shortcuts import render
from django.template import loader
from boxes.models import BoxStatus
from boxes.serializers import BoxStatusSerializer
import re
import  _thread, time,threading
import logging
log = logging.getLogger(__name__)

webFunctions  = Httphandler()
cmd = Cmd()

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
    url = API_URL + path
    data = {}
    params = {}

    if request.method == 'GET':
        for key, value in request.GET.items():
            params[key] = value
        signature = sign(API_KEY, API_SECRET, params)
    elif request.method == 'POST':
        if len(request.body) > 1:
            if len(json.loads(request.body.decode('utf-8'))) > 3:
                data = json.loads(request.body.decode('utf-8'))
        signature = sign(API_KEY, API_SECRET, data)
    else:
        dataOpt = {}
        signature = sign(API_KEY, API_SECRET, dataOpt)

    log.error(data)

    headers = {}
    for key, value in request.META.items():
        headers[key] = str(value)

    headers['Host'] = API_HOST
    headers['X-API-Key'] = API_KEY
    headers['X-API-Sign'] = signature


    esreq = requests.Request(method=request.method, url=url, data=data, params=params, headers=headers)
    resp = requests.Session().send(esreq.prepare())

    res = HttpResponse(resp.text, status= resp.status_code)

    for key, value in resp.headers.items():
        res[key] = value



    return res

def connection_status(request):
    env_obj = Env.objects.order_by('api_key')[0]
    internet_connection = False
    internet_connection_message = 500
    force = False
    params = {}
    internet_connection,internet_connection_message = cmd._is_connected("https://www.google.com")
    if request.method == 'GET':
        for key, value in request.GET.items():
            params[key] = value

    if "force" in params:
        force = params['force']

    if int(internet_connection_message) != 200 or bool(force):
        _save_status()
    return HttpResponse(json.dumps(internet_connection_message),status=int(internet_connection_message), content_type="application/json")


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

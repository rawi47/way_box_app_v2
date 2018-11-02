from env_config.models import Env
import json,hmac,hashlib
import requests
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
log = logging.getLogger(__name__)
from utils.cmd import Cmd




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

def _is_connected(Request):
    url = "https://www.google.com"
    method = "GET"
    headers = {}
    params = {}
    data = {}

    esreq = requests.Request(method=method, url=url, data=data, params=params, headers=headers)
    resp = requests.Session().send(esreq.prepare())

    res = HttpResponse(resp.text, status= resp.status_code)

    return res

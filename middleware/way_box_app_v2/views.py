from env_config.models import Env
import json,hmac,hashlib
import requests
from django.http import HttpResponseRedirect

def sign(public_key, secret_key, data):
    h = hmac.new(
        secret_key.encode('utf-8'), public_key.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    h.update(json.dumps(data, sort_keys=True).encode('utf-8'))
    return str(h.hexdigest())

def catch_all(request,path):
    env_obj = Env.objects.order_by('api_key')[0]
    
    API_HOST = env_obj.api_host
    API_URL = 'https://' + API_HOST + '/'
    API_KEY = env_obj.api_key
    API_SECRET = env_obj.api_secret


    url = API_URL + path

    if path == 'box' or path == 'box/':
        return HttpResponseRedirect('/dashboard/')

    print(url)

    data = {}
    if request.body is not None:
        data = request.body

    params = {}
    for key, value in request.GET:
        params[key] = value

    if request.method == 'GET':
        signature = sign(API_KEY, API_SECRET, params)
    else:
        signature = sign(API_KEY, API_SECRET, data)

    headers = {}


    headers['Host'] = API_HOST
    headers['X-API-Key'] = API_KEY
    headers['X-API-Sign'] = signature

    esreq = requests.Request(method=request.method, url=url, data=request.body, params=params, headers=headers)
    resp = requests.Session().send(esreq.prepare())

    return (resp.text, resp.status_code, resp.headers.items())

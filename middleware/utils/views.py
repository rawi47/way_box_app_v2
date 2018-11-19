from env_config.models import Env
import json
import hmac
import hashlib
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.cmd import Cmd
from utils.status import _save_status
from django.template import loader
import logging


log = logging.getLogger(__name__)
cmd = Cmd()


def sign(public_key, secret_key, data):
    h = hmac.new(
        secret_key.encode('utf-8'), public_key.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    h.update(json.dumps(data, sort_keys=True).encode('utf-8'))
    return str(h.hexdigest())


@csrf_exempt
def catch_all(request, path):
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
    else:
        if request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        signature = sign(API_KEY, API_SECRET, data)

    headers = {
        k: v for k, v in request.META.items() if k.startswith('HTTP')
    }

    headers['Host'] = API_HOST
    headers['X-API-Key'] = API_KEY
    headers['X-API-Sign'] = signature

    esreq = requests.Request(method=request.method, url=url, json=data, headers=headers)
    resp = requests.Session().send(esreq.prepare())

    res = HttpResponse(resp.text, status=resp.status_code)

    for key, value in resp.headers.items():
        if key != "Connection":
            res[key] = value

    return res


def connection_status(request):
    internet_connection = False
    internet_connection_message = 500
    force = False
    params = {}
    internet_connection, internet_connection_message = cmd._is_connected("https://www.google.com")
    if request.method == 'GET':
        for key, value in request.GET.items():
            params[key] = value

    if "force" in params:
        force = params['force']

    if int(internet_connection_message) != 200 or bool(force):
        _save_status()
    return HttpResponse(json.dumps(internet_connection_message), status=int(internet_connection_message), content_type="application/json")


def _error(request):
    template = loader.get_template('error.html')
    status = {"internet_connection_message": 200}
    context = {
        'res': status
    }
    return HttpResponse(template.render(context, request))

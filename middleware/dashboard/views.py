from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from env_config.models import EnvSerializer,Env
from itertools import groupby
from django.contrib.auth.decorators import login_required
from .forms import ConfigForm
from utils.cmd import Cmd
from django.http import HttpResponseRedirect
from user.models import User
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from utils.httpHandler import HttpHandler
from SystemStatus.models import SystemStatus,SystemStatusSerializer

import os
from memory_profiler import memory_usage
import json
from way_box_app_v2 import run
import logging
from os import path
log = logging.getLogger(__name__)

cmd = Cmd()
httpHandler = HttpHandler()



static_path = settings.STATICFILES_DIRS[0] + "/config/"

@login_required
def index(request):
    template = loader.get_template('dashboard/index.html')

    systemStatus_obj = SystemStatus.objects.order_by('-id')[:10]
    x_data = []
    ctx_data = [1,3,6,18,2]
    for line in systemStatus_obj:
        x_data.append(line.date.strftime("%Y-%m-%d %H:%M:%S"))
        ctx_data.append(line.connected_clients)

    label = "Connected clients"
    env_obj = Env.objects.order_by('api_key')
    env_data = {}
    if env_obj:
        serializerEnv = EnvSerializer(env_obj[0])

        env_data = serializerEnv.data
    context = {
    	'env_obj' : env_data,
        'ctx_data' : ctx_data,
        'x_data' : x_data,
        'label' : label
    }
    return HttpResponse(template.render(context, request))



@login_required
def get_name(request):
    lst = []
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConfigForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            env_obj = Env.objects.order_by('api_key')[0]
            old_mode = env_obj.api_mode
            new_mode = form.cleaned_data['api_mode']

            Env.objects.filter(pk=env_obj.id).update(
                client_session_timeout=form.cleaned_data['client_session_timeout'],
                name=form.cleaned_data['name'],
                api_mode=form.cleaned_data['api_mode']
                )
            httpHandler._set_establichement_name(env_obj.api_host,env_obj.api_key,env_obj.api_secret,lst)

            if old_mode != new_mode:
                run._config_main_prog()
                print("diffrent")

            for line in lst:
                print(lst)
            return HttpResponseRedirect('/dashboard/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConfigForm()

    return render(request, 'dashboard/configuration.html', {'form': form})



@login_required
def run_config(request):
    response_data = []
    response_data = run._config_main_prog()


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def run_prog(request):
    response_data = []
    response_data = run._run_main_prog()


    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required
def reboot(request):
    response_data = []
    user_obj = User.objects.order_by('id')[0]
    cmd.run("reboot",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

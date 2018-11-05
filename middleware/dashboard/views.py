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
    ctx_data = []
    env_obj = Env.objects.order_by('api_key')
    env_data = {}
    if env_obj:
        serializerEnv = EnvSerializer(env_obj[0])

        env_data = serializerEnv.data
    context = {
    	'env_obj' : env_data,
        'ctx_data' : ctx_data
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
            Env.objects.filter(pk=env_obj.id).update(
                client_session_timeout=form.cleaned_data['client_session_timeout'],
                name=form.cleaned_data['name'],
                api_mode=form.cleaned_data['api_mode'],
                api_key=form.cleaned_data['api_key'],
                api_secret=form.cleaned_data['api_secret'],
                api_host=form.cleaned_data['api_host'],
                )
            httpHandler._set_establichement_name(form.cleaned_data['api_host'],form.cleaned_data['api_key'],form.cleaned_data['api_secret'],lst)

            for line in lst:
                print(lst)
            return HttpResponseRedirect('/dashboard/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConfigForm()

    return render(request, 'dashboard/configuration.html', {'form': form})

@login_required
def systemctl_stat(request):
    template = loader.get_template('dashboard/systemctl.html')

    systemctl_status = []
    user_obj = User.objects.order_by('id')[0]

    cmd.run("systemctl status",user_obj,systemctl_status,getDate=False)

    context = {
        'systemctl_status' : systemctl_status,

    }
    return HttpResponse(template.render(context, request))



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
def nds_ctl(request):
    template = loader.get_template('dashboard/nds_ctl.html')

    context = {

    }

    return HttpResponse(template.render(context, request))


@login_required
def nds_ctl_status(request):
    ndsctl_status = []
    user_obj = User.objects.order_by('id')[0]
    cmd.run("ndsctl status",user_obj,ndsctl_status,getDate=False)
    ndsctl_status_dict = {}
    for line in ndsctl_status:
        if ":" in line:
            key = line.split(":")[0]
            value = line.split(":")[1]

            ndsctl_status_dict[key] = value

    return HttpResponse(json.dumps(ndsctl_status_dict), content_type="application/json")


@login_required
def reboot(request):
    response_data = []
    user_obj = User.objects.order_by('id')[0]
    cmd.run("reboot",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def nds_stop(request):
    response_data = []
    user_obj = User.objects.order_by('id')[0]
    cmd.run("ndsctl stop",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def nds_start(request):
    response_data = []
    user_obj = User.objects.order_by('id')[0]
    cmd.run("nodogsplash",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def hostapd_restart(request):
    response_data = []
    user_obj = User.objects.order_by('id')[0]
    cmd.run("systemctl restart hostapd",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

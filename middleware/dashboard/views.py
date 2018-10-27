from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from env_config.models import EnvSerializer,Env,SettingApp,InstalledSoftwares
from itertools import groupby
from django.contrib.auth.decorators import login_required
from .forms import ConfigForm
from utils.networks import NetworksUtils
from utils.cmd import Cmd
from django.http import HttpResponseRedirect
from user.models import User
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.models import User

import os
from memory_profiler import memory_usage
import json
from way_box_app_v2 import run
import logging
log = logging.getLogger(__name__)

cmd = Cmd()
user_obj = User.objects.order_by('id')[0]


InstalledSoftwares_objs = InstalledSoftwares.objects.order_by('name')
static_path = settings.STATICFILES_DIRS[0] + "/config/"

@login_required
def index(request):
    env_obj = Env.objects.order_by('api_key')[0]
    template = loader.get_template('dashboard/index.html')

    serializerEnv = EnvSerializer(env_obj)
    networksutil = NetworksUtils()

    ctx_data = []


    context = {
    	'env_obj' : serializerEnv.data,
    	'netwrk_obj' : networksutil._get_interfaces(),
        'ctx_data' : ctx_data
    }
    return HttpResponse(template.render(context, request))



@login_required
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConfigForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print (form.cleaned_data)
            env_obj = Env.objects.order_by('api_key')[0]
            Env.objects.filter(pk=env_obj.id).update(client_session_timeout=form.cleaned_data['client_session_timeout'],api_mode=form.cleaned_data['api_mode'])
            return HttpResponseRedirect('/dashboard/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConfigForm()

    return render(request, 'dashboard/name.html', {'form': form})

@login_required
def systemctl_stat(request):
    template = loader.get_template('dashboard/systemctl.html')

    systemctl_status = []

    cmd.run("systemctl status",user_obj,systemctl_status,getDate=False)

    context = {
        'systemctl_status' : systemctl_status,

    }
    return HttpResponse(template.render(context, request))

@login_required
def config_files(request):
    template = loader.get_template('dashboard/configfile.html')
    env_obj = Env.objects.order_by('api_key')[0]
    setting_app_obj = SettingApp.objects.filter(api_mode__in=[env_obj.api_mode,'commun']).order_by('name')

    configs = {}
    for line in setting_app_obj:
        listR = []
        cmd._read_file(line.dest,user_obj,listR)

        configs[line.dest] = listR

    configsOrigin = {}
    for line in setting_app_obj:
        listRo = []
        cmd._read_file(static_path + line.origine,user_obj,listRo)

        configsOrigin[line.origine] = listRo

    context = {
        'configs' : configs,
        'configsOrigin' : configsOrigin,

    }
    return HttpResponse(template.render(context, request))

@login_required
def installed_software(request):
    template = loader.get_template('dashboard/istalledSoftware.html')

    listSo = {}
    for soft in InstalledSoftwares_objs:
        listS = []

        cmd.run(soft.command ,user_obj,listS)

        listSo[soft.name] = listS

    print (listSo)


    context = {
        'listSo' : listSo,

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
    cmd.run("reboot",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def nds_stop(request):
    response_data = []
    cmd.run("ndsctl stop",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def nds_start(request):
    response_data = []
    cmd.run("nodogsplash",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def hostapd_restart(request):
    response_data = []
    cmd.run("systemctl restart hostapd",user_obj,response_data,getDate=False)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

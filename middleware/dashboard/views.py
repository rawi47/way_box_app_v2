from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from env_config.models import EnvSerializer,Env,SettingApp,InstalledSoftwares,SettingAppSerializer
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

    cmd.run("systemctl status",user_obj,systemctl_status,getDate=False)

    context = {
        'systemctl_status' : systemctl_status,

    }
    return HttpResponse(template.render(context, request))

@login_required
def config_files(request):
    template = loader.get_template('dashboard/configfile.html')
    env_obj = Env.objects.order_by('api_key')[0]
    setting_app_obj = SettingApp.objects.filter(api_mode__in=[env_obj.api_mode,'commun']).order_by('sequence')

    static_path = path.join(env_obj.root_dir,env_obj.app_dir,env_obj.config_dir)
    configs = []
    for line in setting_app_obj:
        settingAppSerializer = SettingAppSerializer(line)
        cnf = settingAppSerializer.data
        listR = []
        file = path.join(static_path,cnf["directory"],cnf["origine"])

        if len(cnf["sub_directory"]) > 2:
            file = path.join(static_path,cnf["directory"],cnf['sub_directory'],cnf["origine"])

        cmd._read_file(file,user_obj,listR)
        cnf["origine_file"] = listR
        listR = []
        cmd._read_file(cnf["dest"],user_obj,listR)
        cnf["dest_file"] = listR
        configs.append(cnf)
        cnf["stat"] = []
        if cnf["status"]:
            lst = []
            cmd.run(cnf["cmd_status"] + " " + cnf["setting_type"],user_obj,lst)
            cnf["stat"] = lst


    context = {
        'configs' : configs,
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

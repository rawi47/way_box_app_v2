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

cmd = Cmd()
user_obj = User.objects.order_by('id')[0]
env_obj = Env.objects.order_by('api_key')[0]
setting_app_obj = SettingApp.objects.filter(api_mode__in=[env_obj.api_mode,'commun']).order_by('name')
InstalledSoftwares_objs = InstalledSoftwares.objects.order_by('name')
static_path = settings.STATICFILES_DIRS[0] + "/config/"

@login_required
def index(request):

    template = loader.get_template('dashboard/index.html')	
    
    serializerEnv = EnvSerializer(env_obj)
    networksutil = NetworksUtils()


    mem_usage = memory_usage(-1, interval=.2, timeout=1)
    ctx_data = []
    print(mem_usage)

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
            Env.objects.filter(pk=env_obj.id).update(client_session_timeout=form.cleaned_data['client_session_timeout'])
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
        print(soft.name)
        cmd.run(soft.name + " -version" ,user_obj,listS,getDate=False)
 
        listSo[soft.name] = listS


    context = { 
        'listSo' : listSo,
      
    }
    return HttpResponse(template.render(context, request))

def thirty_day_registrations():
    final_data = []

    cmd.run("echo /proc/meminfo" ,user_obj,final_data,getDate=False)



    return final_data

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('form', views.get_name, name='env_configuration'),
    path('systemctl', views.systemctl_stat, name='systemctl_stats'),
    path('run_config', views.run_config, name='run_config'),
    path('run_prog', views.run_prog, name='run_prog'),
    path('reboot', views.reboot, name='reboot'),
    path('nds_ctl', views.nds_ctl, name='nds_ctl'),

    path('nds_stop', views.nds_stop, name='nds_stop'),
    path('nds_start', views.nds_start, name='nds_start'),
    path('hostapd_restart', views.hostapd_restart, name='hostapd_restart'),
    path('nds_ctl_status', views.nds_ctl_status, name='nds_ctl_status'),

]

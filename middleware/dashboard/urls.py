from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('form', views.get_name, name='env_configuration'),
    path('run_config', views.run_config, name='run_config'),
    path('run_prog', views.run_prog, name='run_prog'),
    path('reboot', views.reboot, name='reboot'),


]

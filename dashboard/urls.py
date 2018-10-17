from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('form', views.get_name, name='env_configuration'),
    path('systemctl', views.systemctl_stat, name='systemctl_stats'),
    path('configFiles', views.config_files, name='config_filess'),
    path('installed_software', views.installed_software, name='installed_software'),
]
 


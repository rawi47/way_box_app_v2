from django import forms
from env_config.models import EnvSerializer,Env

class ConfigForm(forms.Form):

	ts = (
		(30,'30 minute'),
		(60,'1 heure')
	)

	modes = (
		('wlan','wlan'),
		('eth','eth')
	)
	def _get_name():
		env_obj = Env.objects.order_by('api_key')[0]
		return env_obj.name
	def _get_api_key():
		env_obj = Env.objects.order_by('api_key')[0]
		return env_obj.api_key

	def _get_api_secret():
		env_obj = Env.objects.order_by('api_key')[0]
		return env_obj.api_secret

	def _get_client_session_timeout():
		env_obj = Env.objects.order_by('api_key')[0]
		return env_obj.client_session_timeout

	def _get_api_mode():
		env_obj = Env.objects.order_by('api_key')[0]
		return env_obj.api_mode


	name = forms.CharField( max_length=100,initial=_get_name)
	api_key = forms.CharField( max_length=100,initial=_get_api_key)
	api_secret = forms.CharField( max_length=100,initial=_get_api_secret)

	client_session_timeout = forms.ChoiceField(
	    choices=ts,
	    widget=forms.Select(),
		initial=_get_client_session_timeout
	)
	api_mode = forms.ChoiceField(
	    choices=modes,
	    widget=forms.Select(),
		initial=_get_api_mode
	)

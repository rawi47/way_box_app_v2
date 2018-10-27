from django import forms

class ConfigForm(forms.Form):

	ts = (
		(30,'30 minute'),
		(60,'1 heure')
	)

	modes = (
		('wlan','wlan'),
		('eth','eth')
	)

	client_session_timeout = forms.ChoiceField(
	    choices=ts,
	    widget=forms.Select()
	)
	api_mode = forms.ChoiceField(
	    choices=modes,
	    widget=forms.Select()
	)



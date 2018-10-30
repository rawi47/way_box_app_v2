from django.db import models
import hmac, hashlib, json
import requests
from way_box_app_v2 import views
from env_config.models import Env
import datetime
import requests

class HttpHandler(models.Model):

	def _set_establichement_name(self,API_HOST,API_KEY,API_SECRET,lst):
		env_obj = Env.objects.order_by('api_key')[0]
		getD = str(datetime.datetime.now()) + " - "
		path = "/customers/establishment"
		url = "http://" + API_HOST + path
		method = "GET"
		data = {}
		params = {}

		headers = {}
		signature = views.sign(API_KEY, API_SECRET, params)


		headers['Host'] = API_HOST
		headers['X-API-Key'] = API_KEY
		headers['X-API-Sign'] = signature



		try:
			esreq = requests.Request(method=method, url=url, data=data, params=params, headers=headers)
			resp = requests.Session().send(esreq.prepare())

			res = (resp.text, resp.status_code, resp.headers.items())



			res_obj = json.loads(res[0])

			new_name = res_obj['name']

			if env_obj.name != new_name:
				print(new_name)
				print(env_obj.name)
				Env.objects.filter(pk=env_obj.id).update(name=new_name)

			lst.append(getD + new_name)
		except Exception as e:
			lst.append(getD + str(e))

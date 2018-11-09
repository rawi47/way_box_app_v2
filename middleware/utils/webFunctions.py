from django.db import models
import hmac, hashlib, json
import requests
from env_config.models import Env
import datetime
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class WebFunctions(models.Model):

	def _set_establichement_name(self,lst):
		env_obj = Env.objects.order_by('api_key')[0]
		api_port = env_obj.api_port
		getD = str(datetime.datetime.now()) + " - "

		path = "/customers/establishment"

		url = "http://127.0.0.1:" + str(api_port) + path
		method = "GET"
		data = {}
		params = {}


		res = self._make_request(url,method,data,params)

		res_obj = json.loads(res.text)


		new_name = res_obj['name']
		if env_obj.name != new_name:
			print(new_name)
			print(env_obj.name)
			Env.objects.filter(pk=env_obj.id).update(name=new_name)

		lst.append(getD + new_name)


	def _requests_retry_session(
		self,
	    retries=3,
	    backoff_factor=0.3,
	    status_forcelist=(500, 502, 504),
	    session=None,
	):
	    session = session or requests.Session()
	    retry = Retry(
	        total=retries,
	        read=retries,
	        connect=retries,
	        backoff_factor=backoff_factor,
	        status_forcelist=status_forcelist,
	    )
	    adapter = HTTPAdapter(max_retries=retry)
	    session.mount('http://', adapter)
	    session.mount('https://', adapter)
	    return session

	def _make_request(self,url,method,data,params):
		if method == "GET":
		    res = self._requests_retry_session().get(url)
		elif method == "POST":
			data = json.dumps(data)
			res = self._requests_retry_session().post(url,data=data)
		return res

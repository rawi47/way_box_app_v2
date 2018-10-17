from django.db import models
import hmac, hashlib, json
import requests

class HttpHandler(models.Model):

	def _sign(self,public_key, secret_key, data):
	    h = hmac.new(
	        secret_key.encode('utf-8'), public_key.encode('utf-8'),
	        digestmod=hashlib.sha1
	    )
	    h.update(json.dumps(data, sort_keys=True).encode('utf-8'))
	    return str(h.hexdigest())

	def _catch_all(self,url,data,params,headers,method):
		esreq = requests.Request(method=method, url=url, data=data, params=params, headers=headers)
		resp = requests.Session().send(esreq.prepare())

		return (resp.text, resp.status_code, resp.headers.items())

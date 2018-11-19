from django.db import models
import json
import requests
from env_config.models import Env

import logging
log = logging.getLogger(__name__)


class Httphandler(models.Model):

	def _set_establichement_name(self):
		try:
			env_obj = Env.objects.order_by('api_key')[0]
			api_port = env_obj.api_port
			path = "/portal/customers/establishment"
			url = "http://127.0.0.1:" + str(api_port) + path
			res = requests.get(url)
			res_obj = json.loads(res.text)
			new_name = res_obj['name']
			if env_obj.name != new_name:
				Env.objects.filter(pk=env_obj.id).update(name=new_name)

		except Exception as e:
			log.error(str(e))

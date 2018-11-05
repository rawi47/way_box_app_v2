from django.db import models
import netifaces


class NetworksUtils(models.Model):

	def _all_interfaces(self):
		interface_list = netifaces.interfaces()
		gateways_list = netifaces.gateways()
		return {
			'interface_list' : interface_list,
			'gateways_list' : gateways_list
		}

	def _get_interfaces(self):
		serializerNetworks = {}
		af_list = [(netifaces.AF_LINK,'AF_LINK'),(netifaces.AF_INET,'AF_INET'),(netifaces.AF_INET6,'AF_INET6')]
		ifs = self._all_interfaces()['interface_list']
		for i in ifs:



			addrs = netifaces.ifaddresses(i)
			for af in af_list:
				if af[0] in addrs:
					address = ""
					netmask = ""
					broadcast = ""
					peer = ""
					name = i + "-" + str(af[1])


					for addr in addrs[af[0]]:
						if 'addr' in addr:
							address = addr['addr']
						if 'netmask' in addr:
							netmask = addr['netmask']
						if 'broadcast' in addr:
							broadcast = addr['broadcast']
						if 'peer' in addr:
							peer = addr['peer']
						if_link = AfLinks(name = name,af_link_addr = address,af_link_broadcast = broadcast ,af_link_netmask = netmask,af_link_peer = peer,type = af[1])
						if i not in serializerNetworks:
							serializerNetworks[i] =  [AfLinksSerializer(if_link).data]
						else:
							serializerNetworks[i].append(AfLinksSerializer(if_link).data)

		return serializerNetworks

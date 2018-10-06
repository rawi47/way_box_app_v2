from django.contrib import admin

from .models import Env
from .models import Hostapd
from .models import Dnsmasq
from .models import IpTables
from .models import Interfaces
from .models import Nodogsplash
from .models import Hosts
from .models import Nodogsplash
from .models import Ipset

admin.site.register(Env)
admin.site.register(Hostapd)
admin.site.register(Dnsmasq)
admin.site.register(IpTables)
admin.site.register(Interfaces)
admin.site.register(Nodogsplash)
admin.site.register(Hosts)
admin.site.register(Ipset)
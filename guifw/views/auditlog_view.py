from django.shortcuts import render
from guifw.models.address import Address
from guifw.models.chain import Chain
from guifw.models.filter import Filter
from guifw.models.hostset import Hostset
from guifw.models.interface import Interface
from guifw.models.ipset import Ipset
from guifw.models.nat import Nat
from guifw.models.netset import Netset
from guifw.models.network import Network
from guifw.models.port import Port
from guifw.models.protocol import Protocol
from guifw.models.shappclass import Shappclass
from guifw.models.shapping import Shapping
from guifw.models.url import URL
from itertools import chain

# Create your views here.


def listAuditLog(request):
    logs = chain(Address.audit_log.all(),
                 Chain.audit_log.all(),
                 Filter.audit_log.all(),
                 Port.audit_log.all(),
                 Hostset.audit_log.all(),
                 Interface.audit_log.all(),
                 Ipset.audit_log.all(),
                 Nat.audit_log.all(),
                 Netset.audit_log.all(),
                 Network.audit_log.all(),
                 Protocol.audit_log.all(),
                 Shappclass.audit_log.all(),
                 Shapping.audit_log.all(),
                 URL.audit_log.all())
    context = {'logs': logs }
    return render(request, 'audit-log.html', context)
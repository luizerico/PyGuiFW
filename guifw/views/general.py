from django.shortcuts import render
from django.views import generic
from guifw.models.filter import Filter, FormFilter
from guifw.models.network import Network
from guifw.library.sysnet import Sysnet
from guifw.library.rule import Rule
from guifw.models.port import Port

# Create your views here.

#def listInterfaces(request):
#    ifaces = Sysnet()
#    if_all = {'rules':ifaces.allInterfaces()}
#    return render(request, 'rulecomposerview.html', if_all)

def ruleApply(request):
    natfile = Rule.writeNat()
    rulefile = Rule.writeFilter()
    context = {
            'rules': Rule.applyRules(rulefile),
            'nats': Rule.applyRules(natfile)
    }
    return render(request, 'ruleapply.html', context)


def ruleSave(request):
    natfile = Rule.writeNat()
    rulefile = Rule.writeFilter()
    context = {
            'rules': Rule.filterrulecomposer(),
            'nats': Rule.natrulecomposer()
    }
    return render(request,'ruleapply.html', context)


def ruleView(request):
    context = {
            'rules': Rule.filterrulecomposer(),
            'nats': Rule.natrulecomposer(),
            'shapping' : Rule.shappingrulecomposer()
    }
    return render(request, 'ruleview.html', context)


def network_view(request):
    network = Network.objects.all()
    context = {'network': network}
    return render(request, 'networklistview.html', context)


def listRoutes(request):
    routes = Sysnet.listRoutes()
    context = {'routes': routes}
    return render(request, 'routes.html', context)

def listInterfaces(request):
    interfaces = Sysnet.listInterfaces()
    context = {'interfaces': interfaces}
    return render(request, 'interfaces.html', context)

def listConnections(request):
    connections = Sysnet.listConnections()
    context = {'connections': connections }
    return render(request, 'connections.html', context)

def listProcesses(request):
    processes = Sysnet.listProcesses()
    context = {'connections': processes }
    return render(request, 'processes.html', context)

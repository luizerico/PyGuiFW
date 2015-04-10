from django.shortcuts import render
from django.views import generic
from guifw.models.filter import Filter, FormFilter
from guifw.models.network import Network
from guifw.library.sysnet import Sysnet
from guifw.library.rule import Rule

# Create your views here.

def listInterfaces(request):
    ifaces = Sysnet()
    if_all = {'rules':ifaces.allInterfaces()}
    return render(request, 'rulecomposerview.html', if_all)

def ruleApply(request):
    context = {
            'rules': Rule.filterrulecomposer(),
            'nats': Rule.natrulecomposer()
    }
    return render(request, 'ruleapply.html', context)

def ruleView(request):
    context = {
            'rules': Rule.filterrulecomposer(),
            'nats': Rule.natrulecomposer()
    }
    return render(request, 'ruleview.html', context)


def rule_view(request):
    rules = Filter.objects.all()
    context = {'rules': rules}
    return render(request, 'rulelistview.html', context)


def network_view(request):
    network = Network.objects.all()
    context = {'network': network}
    return render(request, 'networklistview.html', context)


class RuleListView(generic.ListView):
    model = Filter
    template_name = 'rulelistview.html'


class RuleEditView(generic.FormView):
    form_class = FormFilter
    template_name = 'baseformview.html'
    success_url = '/list/'

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
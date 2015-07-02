from django.shortcuts import render
from guifw.models.network import Network
from guifw.library.sysnet import Sysnet
from guifw.library.rule import Rule
from guifw.models.setting import Setting


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
    rule = Rule()
    setting = Setting.objects.filter(id=1)[0]
    context = {}

    if setting.create_dns_cache:
        context['hostnames'] = rule.cacheComposer()
    if setting.readable_rules:
        context['rules'] = rule.filterRuleComposer()
    if setting.restore_rules:
        context['restores'] = rule.filterSaveComposer()
    if setting.shapping_rules:
        context['shappings'] = rule.shappingRuleComposer()
    if setting.nat_rules:
        context['nats'] = rule.natRuleComposer()
    if setting.ipset_rules:
        context['ipsets'] = rule.setComposer()
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
    context = {'connections': connections}
    return render(request, 'connections.html', context)

def listProcesses(request):
    processes = Sysnet.listProcesses()
    context = {'connections': processes}
    return render(request, 'processes.html', context)

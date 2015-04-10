from django.shortcuts import render
from django.views import generic
from guifw.models.filter import Filter, FilterForm
from guifw.models.network import Network
from guifw.models.netset import Setnet
from guifw.models.hostset import Sethost


# Create your views here.

def ruleComposerView(request):
    rules = Filter.objects.all()
    context = {}
    tmp = []

    srcset = Sethost.buildSet() + " " + Setnet.buildSet()

    for set in Setnet.objects.all():
        tmp.append("#### Building the IPSET: " + set.name)
        tmp.append("ipset -N " + set.name + " nethash")
        for address in set.address.all():
            tmp.append("ipset -A " + set.name + " " + address.getFullAddress())

    for set in Sethost.objects.all():
        tmp.append("#### Building the IPSET: " + set.name)
        tmp.append("ipset -N " + set.name + " iphash")
        for address in set.address.all():
            tmp.append("ipset -A " + set.name + " " + address.getFullAddress())

    tmp.append("")
    tmp.append("#### Building the Firewall RULES")
    for rule in rules:
        cmp_rule = str(rule.chain)
        if rule.source.all( ):
            cmp_rule += " -s " + str(','.join([source.getFullAddress() for source in rule.source.all()]))

        if rule.srcset:
            cmp_rule += " -m set --set " + str(rule.srcset) + " src "

        if rule.srcport.all():
            cmp_rule += " -sport " + str(','.join([srcport.port for srcport in rule.srcport.all()]))

        if rule.destiny.all():
            cmp_rule += " -d " + str(','.join([destiny.getFullAddress() for destiny in rule.destiny.all()]))

        if rule.dstset:
            cmp_rule += " -m set --set " + str(rule.dstset) + " dst "

        if rule.dstport.all():
            cmp_rule += " -dport " + str(','.join([dstport.port for dstport in rule.dstport.all()]))

        if rule.protocol:
            cmp_rule += " -p " + str(rule.protocol.number)

        if rule.in_interface:
            cmp_rule += " -i " + str(rule.in_interface)

        if rule.out_interface:
            cmp_rule += " -o " + str(rule.out_interface )

        if rule.conn_state!='[]':
            states = ("NEW","RELATED","ESTABLISHED","INVALID","UNTRACKED")
            # Convert UNICODE values into a list of strings and after this
            # convert into a integer list to filter the STATES list
            list_states = map(int,(str(rule.conn_state).replace("u'","").translate(None, "]['")).split(','))
            selected_states = [states[x] for x in list_states]
            cmp_rule += " -m state --state " + str(selected_states).translate(None,"'[]")
            #cmp_rule += " -m state --state " + str(list_states)

        if rule.adv_options:
            cmp_rule += " " + str(rule.adv_options)

        if rule.log:
            if rule.log_preffix:
                log_rule = "iptables -I " + str(rule.order + 100) + " " + cmp_rule + \
                           " --log_preffix " + str(rule.log_preffix) + \
                           " --log_level " + str(rule.log_level) + " -j LOG "
            else:
                log_rule = "iptables -I " + str(rule.order + 100) + " " + cmp_rule  + \
                           " --log_level " + str(rule.log_level) + " -j LOG "
            tmp.append(log_rule)

        cmp_rule = "iptables -I " + str(rule.order + 1000) + " " + cmp_rule + " -j " + str(rule.action)

        tmp.append(cmp_rule)

    context = {'rules': tmp}

    return render(request, 'rulecomposerview.html', context)


def rule_view(request):
    rules = Rule.objects.all()
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
    form_class = FilterForm
    template_name = 'baseformview.html'
    success_url = '/list/'
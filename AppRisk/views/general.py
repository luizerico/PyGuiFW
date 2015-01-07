from django.shortcuts import render
from django.views import generic
from AppRisk.models.filter import Filter, FormFilter
from AppRisk.models.nat import Nat
from AppRisk.models.network import Network
from AppRisk.models.netset import Netset
from AppRisk.models.hostset import Hostset


# Create your views here.

def ruleComposerView(request):
    rules = Filter.objects.all()
    nats = Nat.objects.all()
    context = {}
    tmprule = []
    tmpnat = []

    #srcset = Hostset.buildSet() + " " + Netset.buildSet()

    tmprule.append("### Building the SET to the Firewall RULES")
    for set in Netset.objects.all():
        tmprule.append("### Building the IPSET: " + set.name)
        tmprule.append("ipset -N " + set.name + " nethash")
        for address in set.address.all():
            tmprule.append("ipset -A " + set.name + " " + address.getFullAddress())

    for set in Hostset.objects.all():
        tmprule.append("### Building the IPSET: " + set.name)
        tmprule.append("ipset -N " + set.name + " iphash")
        for address in set.address.all():
            tmprule.append("ipset -A " + set.name + " " + address.getFullAddress())

    tmprule.append("### Building the Filter Firewall RULES")
    tmpnat.append("### Building the NAT Firewall RULES")

    # Nat Rules Composer
    for nat in nats:
        cmp_rule = ""
        if nat.source:
            cmp_rule += " -s " + str(nat.source.getFullAddress())

        if nat.srcport.all():
            cmp_rule += " -sport " + str(','.join([srcport.port for srcport in nat.srcport.all()]))

        if nat.destiny:
            cmp_rule += " -d " + str(nat.destiny.getFullAddress())

        if nat.dstport.all():
            cmp_rule += " -dport " + str(','.join([dstport.port for dstport in nat.dstport.all()]))

        if nat.protocol:
            cmp_rule += " -p " + str(nat.protocol.number)

        if nat.in_interface:
            cmp_rule += " -i " + str(nat.in_interface)

        if nat.out_interface:
            cmp_rule += " -o " + str(nat.out_interface )

        if nat.conn_state!='[]':
            states = ("NEW","RELATED","ESTABLISHED","INVALID","UNTRACKED")
            # Convert UNICODE values into a list of strings and after this
            # convert into a integer list to filter the STATES list
            list_states = map(int,(str(nat.conn_state).replace("u'","").translate(None, "]['")).split(','))
            selected_states = [states[x] for x in list_states]
            cmp_rule += " -m state --state " + str(selected_states).translate(None,"'[]")
            #cmp_rule += " -m state --state " + str(list_states)

        if nat.adv_options:
            cmp_rule += " " + str(nat.adv_options)

        if nat.log:
            if nat.log_preffix:
                log_rule = "iptables -I " + str(nat.order + 100) + " " + cmp_rule + \
                           " --log_preffix " + str(nat.log_preffix) + \
                           " --log_level " + str(nat.log_level) + " -j LOG "
            else:
                log_rule = "iptables -I " + str(nat.order + 100) + " " + cmp_rule  + \
                           " --log_level " + str(nat.log_level) + " -j LOG "
            tmpnat.append(log_rule)

        if nat.action == "DNAT" or nat.action == "MASQUERADE":
            cmp_rule = "iptables -I " + str(nat.order) + " -t nat -A POSTROUTING " + cmp_rule + " -j " + str(nat.action)
        elif nat.action =="SNAT":
            cmp_rule = "iptables -I " + str(nat.order) + " -t nat -A PREROUTING " + cmp_rule + " -j " + str(nat.action)

        if nat.to_destiny:
            cmp_rule += " --to-destination " + str(nat.to_destiny)

        if nat.to_port:
            cmp_rule += " --to-port " + str(nat.to_port)


        tmpnat.append(cmp_rule)

    # Filter Rules Composer
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
            tmprule.append(log_rule)

        cmp_rule = "iptables -I " + str(rule.order + 1000) + " " + cmp_rule + " -j " + str(rule.action)

        tmprule.append(cmp_rule)

    context = {'rules': tmprule, 'nats': tmpnat}

    return render(request, 'rulecomposerview.html', context)


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
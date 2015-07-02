from datetime import datetime, date
import subprocess
import os
from django.conf import settings
from socket import gethostbyname

from guifw.models.filter import Filter
from guifw.models.nat import Nat
from guifw.models.shapping import Shapping
from guifw.models.netset import Netset
from guifw.models.hostset import Hostset
from guifw.models.interface import Interface
from guifw.models.shappclass import Shappclass
from guifw.models.chain import Chain
from guifw.models.url import URL


class Rule:
    # @staticmethod
    def cacheComposer(self):
        url_ip = []
        for url in URL.objects.all():
            try:
                url_ip.append(url.name + " (" + url.address + ") : " + gethostbyname(url.address))
            except:
                url_ip.append(url.name + " (" + url.address + ") : DNS ERROR: NOT RESOLVED")
        return url_ip

    # @staticmethod
    def applyRules(filename):
        print settings.RULES_DIR
        rulefile = os.path.join(settings.RULES_DIR, filename)
        result = subprocess.check_output(["sh", rulefile])
        return result

    # @staticmethod
    def writeFilter():
        rules = Rule.filtersavecomposer()
        # rules = Rule.filterrulecomposer()
        filename = datetime.now().strftime("%Y%m%d_%H%M") + "_filter.rule"
        filterfile = open(settings.RULES_DIR + "/" + filename, 'w')
        for rule in rules:
            filterfile.writelines(rule + "\n")
        filterfile.close()
        return filename

    # @staticmethod
    def writeNat(self):
        rules = Rule.natrulecomposer()
        filename = datetime.now().strftime("%Y%m%d_%H%M") + "_nat.rule"
        natfile = open(settings.RULES_DIR + "/" + filename, 'w')
        for rule in rules:
            natfile.writelines(rule + "\n")
        natfile.close()
        return filename

    # @staticmethod
    def filterSaveComposer(self):
        rules = Filter.objects.all()
        tmprule = []
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

        # Filter Rules Composer
        tmprule.append("### Building the Filter Firewall RULES")
        tmprule.append("### Building the Filter Firewall RULES")
        tmprule.append("*filter")
        for chain in Chain.objects.all():
            tmprule.append(":" + chain.name + " default " + chain.default)

        for rule in rules:
            cmp_rule = ""
            if rule.protocol:
                cmp_rule += " -p " + str(rule.protocol)

            if rule.srcset:
                cmp_rule += " -m set --match-set " + str(rule.srcset) + " src "

            if rule.srcport.exists():
                if (len(rule.dstport.all()) > 1 or len(rule.srcport.all()) > 1):
                    cmp_rule += " -m multiport --sports " + str(
                        ','.join([srcport.port for srcport in rule.srcport.all()]))
                else:
                    cmp_rule += " --sport " + str(','.join([srcport.port for srcport in rule.srcport.all()]))

            if rule.dstset:
                cmp_rule += " -m set --match-set " + str(rule.dstset) + " dst "

            if rule.dstport.exists():
                if (len(rule.dstport.all()) > 1 or len(rule.srcport.all()) > 1):
                    cmp_rule += " -m multiport --dports " + str(
                        ','.join([dstport.port for dstport in rule.dstport.all()]))
                else:
                    cmp_rule += " --dport " + str(','.join([dstport.port for dstport in rule.dstport.all()]))

            if (rule.time_start or rule.time_stop or rule.date_start or rule.date_stop or rule.week_days != '[]'):
                cmp_rule += " -m time "
                if (rule.time_start):
                    cmp_rule += " --timestart " + str(rule.time_start)
                if (rule.time_stop):
                    cmp_rule += " --timestop " + str(rule.time_stop)
                if (rule.date_start):
                    cmp_rule += " --datestart " + str(rule.date_start)
                if (rule.date_stop):
                    cmp_rule += " --datestop " + str(rule.date_stop)
                if rule.week_days != '[]':
                    weekdays = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
                    # convert into a integer list to filter the Days list
                    list_days = map(int, (str(rule.week_days).replace("u'", "").translate(None, "]['")).split(','))
                    selected_days = [weekdays[x] for x in list_days]
                    cmp_rule += " --weekdays " + (str(selected_days).translate(None, "'[]")).translate(None, " ")

            if rule.in_interface:
                cmp_rule += " -i " + str(rule.in_interface.device)

            if rule.out_interface:
                cmp_rule += " -o " + str(rule.out_interface.device)

            if rule.conn_state != '[]':
                states = ("NEW", "RELATED", "ESTABLISHED", "INVALID", "UNTRACKED")
                # convert into a integer list to filter the STATES list
                list_states = map(int, (str(rule.conn_state).replace("u'", "").translate(None, "]['")).split(','))
                selected_states = [states[x] for x in list_states]
                cmp_rule += " -m state --state " + (str(selected_states).translate(None, "'[]")).translate(None, " ")
                # cmp_rule += " -m state --state " + str(list_states)

            if rule.adv_options:
                cmp_rule += " " + str(rule.adv_options)

            if rule.log:
                if rule.log_preffix:
                    log_rule = cmp_rule + " -j LOG --log-prefix " + str(rule.log_preffix) + \
                               " --log-level " + str(rule.log_level)
                else:
                    log_rule = cmp_rule + " -j LOG --log-level " + str(rule.log_level)

            cmp_rule = cmp_rule + " -j " + str(rule.action)

            if rule.source.all() and rule.destiny.all():
                for source in rule.source.all():
                    for destiny in rule.destiny.all():
                        tmprule.append(" -A " + str(
                            rule.chain) + " -s " + source.getFullAddress() + " -d " + destiny.getFullAddress() + cmp_rule)
                        if rule.log:
                            tmprule.append(" -A " + str(
                                rule.chain) + " -s " + source.getFullAddress() + " -d " + destiny.getFullAddress() + log_rule)
            elif rule.source.all():
                for source in rule.source.all():
                    tmprule.append(" -A " + str(rule.chain) + " -s " + source.getFullAddress() + cmp_rule)
                    if rule.log:
                        tmprule.append(" -A " + str(
                            rule.chain) + " -s " + source.getFullAddress() + " -d " + destiny.getFullAddress() + log_rule)
            elif rule.destiny.all():
                for destiny in rule.destiny.all():
                    tmprule.append(" -A " + str(
                        rule.chain) + " -s " + source.getFullAddress() + " -d " + destiny.getFullAddress() + cmp_rule)
                    if rule.log:
                        tmprule.append(" -A " + str(
                            rule.chain) + " -s " + source.getFullAddress() + " -d " + destiny.getFullAddress() + log_rule)
            else:
                tmprule.append(" -A " + str(rule.chain) + cmp_rule)
                if rule.log:
                    tmprule.append(" -A " + str(rule.chain) + log_rule)

        tmprule.append("COMMIT")
        return tmprule

    def setComposer(self):
        tmprule = []

        for set in Netset.objects.all():
            tmprule.append("# Building the IPSET: " + set.name)
            tmprule.append("ipset -N " + set.name + " nethash")
            for address in set.address.all():
                tmprule.append("ipset -A " + set.name + " " + address.getFullAddress())

        for set in Hostset.objects.all():
            tmprule.append("# Building the IPSET: " + set.name)
            tmprule.append("ipset -N " + set.name + " iphash")
            for address in set.address.all():
                tmprule.append("ipset -A " + set.name + " " + address.getFullAddress())

        return tmprule

    # @staticmethod
    def filterRuleComposer(self):
        tmprule = []
        tmprule.append("### Building the Filter Firewall RULES")

        for rule in Filter.objects.all():
            cmp_rule = ""

            if (bool(rule.srcset) or bool(rule.source.all())):
                if rule.source.all():
                    cmp_rule += " -s " + str(','.join([source.getFullAddress() for source in rule.source.all()]))
                if rule.srcset:
                    cmp_rule += " -m set --match-set " + str(rule.srcset) + " src "
            else:
                cmp_rule = "Error in rule no. " + str(rule.order) + ": You must define the SOURCE."
                tmprule.append(cmp_rule)
                continue

            if (bool(rule.dstset) or bool(rule.destiny.all())):
                if rule.destiny.all():
                    cmp_rule += " -d " + str(','.join([destiny.getFullAddress() for destiny in rule.destiny.all()]))
                if rule.dstset:
                    cmp_rule += " -m set --match-set " + str(rule.dstset) + " dst "
            else:
                cmp_rule = "Error in rule no. " + str(rule.order) + ": You must define the DESTINY."
                tmprule.append(cmp_rule)
                continue

            if not (bool(rule.protocol) != bool(bool(rule.dstport.exists()) or bool(rule.srcport.exists()))):
                if rule.protocol:
                    cmp_rule += " -p " + str(rule.protocol)
                if rule.srcport.exists():
                    if (len(rule.dstport.all()) > 1 or len(rule.srcport.all()) > 1):
                        cmp_rule += " -m multiport --sports " + str(
                            ','.join([srcport.port for srcport in rule.srcport.all()]))
                    else:
                        cmp_rule += " --sport " + str(','.join([srcport.port for srcport in rule.srcport.all()]))
                if rule.dstport.exists():
                    if (len(rule.dstport.all()) > 1 or len(rule.srcport.all()) > 1):
                        cmp_rule += " -m multiport --dports " + str(
                            ','.join([dstport.port for dstport in rule.dstport.all()]))
                    else:
                        cmp_rule += " --dport " + str(','.join([dstport.port for dstport in rule.dstport.all()]))
            else:
                cmp_rule = "Error in rule no. " + str(rule.order) + ": You must set the PROTOCOL and PORT together."
                tmprule.append(cmp_rule)
                continue

            if (rule.time_start or rule.time_stop or rule.date_start or rule.date_stop or rule.week_days != '[]'):
                cmp_rule += " -m time "
                if (rule.time_start):
                    cmp_rule += " --timestart " + str(rule.time_start)
                if (rule.time_stop):
                    cmp_rule += " --timestop " + str(rule.time_stop)
                if (rule.date_start):
                    cmp_rule += " --datestart " + str(rule.date_start)
                if (rule.date_stop):
                    cmp_rule += " --datestop " + str(rule.date_stop)
                if rule.week_days != '[]':
                    weekdays = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
                    # convert into a integer list to filter the Days list
                    list_days = map(int, (str(rule.week_days).replace("u'", "").translate(None, "]['")).split(','))
                    selected_days = [weekdays[x] for x in list_days]
                    cmp_rule += " --weekdays " + (str(selected_days).translate(None, "'[]")).translate(None, " ")

            if rule.in_interface:
                if not (rule.chain.name == 'INPUT' and bool(rule.out_interface)):
                    cmp_rule += " -i " + str(rule.in_interface.device)
                else:
                    cmp_rule = "Error in rule no. " + str(
                        rule.order) + ": You cant use OUT interface together the INPUT chain"
                    tmprule.append(cmp_rule)
                    continue

            if rule.out_interface:
                if not (rule.chain.name == 'OUTPUT' and bool(rule.in_interface)):
                    cmp_rule += " -o " + str(rule.out_interface.device)
                else:
                    cmp_rule = "Error in rule no. " + str(
                        rule.order) + ": You cant use IN interface together the OUTPUT chain"
                    tmprule.append(cmp_rule)
                    continue

            if rule.conn_state != '[]':
                states = ("NEW", "RELATED", "ESTABLISHED", "INVALID", "UNTRACKED")
                # convert into a integer list to filter the STATES list
                list_states = map(int, (str(rule.conn_state).replace("u'", "").translate(None, "]['")).split(','))
                selected_states = [states[x] for x in list_states]
                cmp_rule += " -m state --state " + (str(selected_states).translate(None, "'[]")).translate(None, " ")
                # cmp_rule += " -m state --state " + str(list_states)

            if rule.adv_options:
                cmp_rule += " " + str(rule.adv_options)

            if rule.log:
                if rule.log_preffix:
                    log_rule = "iptables -A " + str(rule.chain) + " " + cmp_rule + \
                               " -j LOG --log-prefix " + str(rule.log_preffix) + \
                               " --log-level " + str(rule.log_level)
                else:
                    log_rule = "iptables -A " + str(rule.chain) + " " + cmp_rule + \
                               " -j LOG --log-level " + str(rule.log_level)
                tmprule.append(log_rule)

            cmp_rule = "iptables -A " + str(rule.chain) + " " + cmp_rule + " -j " + str(rule.action)

            tmprule.append(cmp_rule)

        return (tmprule)

    # @staticmethod
    def natRuleComposer(self):
        nats = Nat.objects.all()
        tmpnat = []

        tmpnat.append("### Building the NAT Firewall RULES")

        # Nat Rules Composer
        for nat in nats:
            cmp_rule = ""
            if nat.protocol:
                cmp_rule += " -p " + str(nat.protocol)

            if nat.source:
                cmp_rule += " -s " + str(nat.source.getFullAddress())

            if nat.srcport.exists():
                if (len(nat.dstport.all()) > 1 or len(nat.srcport.all()) > 1):
                    cmp_rule += " -m multiport --sports " + str(
                        ','.join([srcport.port for srcport in nat.srcport.all()]))
                else:
                    cmp_rule += " --sport " + str(','.join([srcport.port for srcport in nat.srcport.all()]))

            if nat.destiny:
                cmp_rule += " -d " + str(nat.destiny.getFullAddress())

            if nat.dstport.exists():
                if (len(nat.dstport.all()) > 1 or len(nat.srcport.all()) > 1):
                    cmp_rule += " -m multiport --dports " + str(
                        ','.join([dstport.port for dstport in nat.dstport.all()]))
                else:
                    cmp_rule += " --dport " + str(','.join([dstport.port for dstport in nat.dstport.all()]))

            if nat.in_interface:
                cmp_rule += " -i " + str(nat.in_interface.device)

            if nat.out_interface:
                cmp_rule += " -o " + str(nat.out_interface.device)

            '''if nat.conn_state != '[]':
                states = ("NEW", "RELATED", "ESTABLISHED", "INVALID", "UNTRACKED")
                # Convert UNICODE values into a list of strings and after this
                # convert into a integer list to filter the STATES list
                list_states = map(int, (str(nat.conn_state).replace("u'", "").translate(None, "]['")).split(','))
                selected_states = [states[x] for x in list_states]
                cmp_rule += " -m state --state " + str(selected_states).translate(None, "'[]")
                # cmp_rule += " -m state --state " + str(list_states)
            '''

            if nat.adv_options:
                cmp_rule += " " + str(nat.adv_options)

            if nat.log:
                if nat.log_preffix:
                    log_rule = "iptables -A " + str(nat.order + 100) + " " + cmp_rule + \
                               "  -j LOG --log-prefix " + str(nat.log_preffix) + \
                               " --log-level " + str(nat.log_level)
                else:
                    log_rule = "iptables -A " + str(nat.order + 100) + " " + cmp_rule + \
                               "  -j LOG --log-level " + str(nat.log_level)
                tmpnat.append(log_rule)

            if nat.action == "REDIRECT":
                cmp_rule = "iptables -t nat -A PREROUTING " + cmp_rule + " -j " + str(
                    nat.action)
            elif nat.action == "DNAT":
                cmp_rule = "iptables -t nat -A PREROUTING " + cmp_rule + " -j " + str(
                    nat.action)
            elif nat.action == "SNAT":
                cmp_rule = "iptables -t nat -A POSTROUTING " + cmp_rule + " -j " + str(
                    nat.action)
            elif nat.action == "MASQUERADE":
                cmp_rule = "iptables -t nat -A POSTROUTING " + cmp_rule + " -j " + str(
                    nat.action)

            if nat.to_ip:
                cmp_rule += " --to " + str(nat.to_ip.getFullAddress())

            if nat.to_port:
                cmp_rule += " --to-port " + str(nat.to_port)

            tmpnat.append(cmp_rule)

        return (tmpnat)

    # @staticmethod
    def shappingRuleComposer(self):
        rules = Shapping.objects.all()
        tmprule = []
        tmprule.append("iptables -F")

        # Cria a fila principal em cada Interface
        tmprule.append("### Cria a fila principal em cada Interface")
        interfaces = Interface.objects.all()
        for interface in interfaces:
            cmp_rule = "tc qdisc add dev " + interface.device + " root handle 1 htb default 12"
            tmprule.append(cmp_rule)

        # Cria as classes e qdisc's
        # tc class add dev eth192 parent 1:0 classid 1:100 htb rate 1536kbit
        # tc qdisc add dev eth192 parent 1:100 handle 100 sfq perturb 10
        tmprule.append("### Building the Classes and Qdisc")
        shappclasses = Shappclass.objects.all()
        for shappclass in shappclasses:
            class_rule = ""
            qdisc_rule = ""

            if shappclass.interface:
                class_rule += " dev " + str(shappclass.interface.device)
                qdisc_rule += " dev " + str(shappclass.interface.device)

            if shappclass.parent:
                classid = str(shappclass.parent.id) + ":" + str(shappclass.id)
                class_rule += " parent " + str(shappclass.parent.id) + ":0 classid " + classid
                qdisc_rule += " parent " + classid + " handle " + str(shappclass.id)

            if shappclass.rate:
                class_rule += " htb rate " + str(shappclass.rate) + "kbit "

            if shappclass.ceil:
                class_rule += " ceil " + str(shappclass.ceil) + "kbit "

            if shappclass.burst:
                class_rule += " burst " + str(shappclass.burst) + "kbit "

            if shappclass.prio:
                class_rule += " prio " + str(shappclass.prio)

            if shappclass.perturb:
                qdisc_rule += " sfq perturb " + str(shappclass.perturb)

            tmprule.append("tc class add " + class_rule)
            tmprule.append("tc qdisc add " + qdisc_rule)

        # Cria os filtros
        # tc filter add dev eth10 parent 1:0 protocol ip u32 match ip dst 10.1.25.18 flowid 1:101
        tmprule.append("### Building the Filters")
        shappings = Shapping.objects.all()
        for shapping in shappings:
            filter_rule = ""

            if shapping.shappclass:
                filter_rule += " add dev " + str(shapping.shappclass.interface.device)

            # if shapping.parent:
            filter_rule += " parent  " + str(shapping.shappclass.parent.id) + ":0 "
            filter_rule += " protocol ip u32 match ip "

            if shapping.source:
                filter_rule += " src " + str(shapping.source.address)

            if shapping.srcport:
                filter_rule += " srcport " + str(shapping.srcport)

            if shapping.destiny:
                filter_rule += " dst " + str(shapping.destiny)

            if shapping.dstport:
                filter_rule += " dstport " + str(shapping.dstport)

            tmprule.append("tc filter " + filter_rule)

        # Shapping Rules Composer
        return (tmprule)

    @staticmethod
    def rulecomposer():
        rules = Filter.objects.all()
        nats = Nat.objects.all()
        tmprule = []
        tmpnat = []

        # srcset = Hostset.buildSet() + " " + Netset.buildSet()

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
                cmp_rule += " -i " + str(nat.in_interface.device)

            if nat.out_interface:
                cmp_rule += " -o " + str(nat.out_interface.device)

            if nat.conn_state != '[]':
                states = ("NEW", "RELATED", "ESTABLISHED", "INVALID", "UNTRACKED")
                # Convert UNICODE values into a list of strings and after this
                # convert into a integer list to filter the STATES list
                list_states = map(int, (str(nat.conn_state).replace("u'", "").translate(None, "]['")).split(','))
                selected_states = [states[x] for x in list_states]
                cmp_rule += " -m state --state " + str(selected_states).translate(None, "'[]")
                # cmp_rule += " -m state --state " + str(list_states)

            if nat.adv_options:
                cmp_rule += " " + str(nat.adv_options)

            if nat.log:
                if nat.log_preffix:
                    log_rule = "iptables -I " + str(nat.order + 100) + " " + cmp_rule + \
                               " --log_preffix " + str(nat.log_preffix) + \
                               " --log_level " + str(nat.log_level) + " -j LOG "
                else:
                    log_rule = "iptables -I " + str(nat.order + 100) + " " + cmp_rule + \
                               " --log_level " + str(nat.log_level) + " -j LOG "
                tmpnat.append(log_rule)

            if nat.action == "DNAT" or nat.action == "MASQUERADE":
                cmp_rule = "iptables -I " + str(nat.order) + " -t nat -A POSTROUTING " + cmp_rule + " -j " + str(
                    nat.action)
            elif nat.action == "SNAT":
                cmp_rule = "iptables -I " + str(nat.order) + " -t nat -A PREROUTING " + cmp_rule + " -j " + str(
                    nat.action)

            if nat.to_ip:
                cmp_rule += " --to " + str(nat.to_ip)

            if nat.to_port:
                cmp_rule += " --to-port " + str(nat.to_port)

            tmpnat.append(cmp_rule)

        # Filter Rules Composer
        for rule in rules:
            cmp_rule = str(rule.chain)
            if rule.source.all():
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
                cmp_rule += " -i " + str(rule.in_interface.device)

            if rule.out_interface:
                cmp_rule += " -o " + str(rule.out_interface.device)

            if rule.conn_state != '[]':
                states = ("NEW", "RELATED", "ESTABLISHED", "INVALID", "UNTRACKED")
                # Convert UNICODE values into a list of strings and after this
                # convert into a integer list to filter the STATES list
                list_states = map(int, (str(rule.conn_state).replace("u'", "").translate(None, "]['")).split(','))
                selected_states = [states[x] for x in list_states]
                cmp_rule += " -m state --state " + str(selected_states).translate(None, "'[]")
                # cmp_rule += " -m state --state " + str(list_states)

            if rule.adv_options:
                cmp_rule += " " + str(rule.adv_options)

            if rule.log:
                if rule.log_preffix:
                    log_rule = "iptables -I " + str(rule.order + 100) + " " + cmp_rule + \
                               " --log_preffix " + str(rule.log_preffix) + \
                               " --log_level " + str(rule.log_level) + " -j LOG "
                else:
                    log_rule = "iptables -I " + str(rule.order + 100) + " " + cmp_rule + \
                               " --log_level " + str(rule.log_level) + " -j LOG "
                tmprule.append(log_rule)

            cmp_rule = "iptables -I " + str(rule.order + 1000) + " " + cmp_rule + " -j " + str(rule.action)

            tmprule.append(cmp_rule)

        context = {
            'rules': tmprule,
            'nats': tmpnat
        }

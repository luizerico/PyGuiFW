from guifw.models.filter import Filter
from guifw.models.nat import Nat
from guifw.models.netset import Netset
from guifw.models.hostset import Hostset
from datetime import datetime, date

class Rule:

    @staticmethod
    def writeFilter():
        rules = Rule.filterrulecomposer()
        filename = datetime.now().strftime("%Y%m%d_%H%M") + "_filter.rule"
        filterfile = open(filename,'w')
        for rule in rules:
            filterfile.writelines(rule + "\n")
        filterfile.close()


    @staticmethod
    def writeNat():
        rules = Rule.natrulecomposer()
        filename = datetime.now().strftime("%Y%m%d_%H%M") + "_nat.rule"
        natfile = open(filename,'w')
        for rule in rules:
            natfile.writelines(rule + "\n")
        natfile.close()


    @staticmethod
    def filterrulecomposer():
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
        for rule in rules:
            cmp_rule = ""
            if rule.protocol:
                cmp_rule += " -p " + str(rule.protocol)

            if rule.source.all():
                cmp_rule += " -s " + str(','.join([source.getFullAddress() for source in rule.source.all()]))

            if rule.srcset:
                cmp_rule += " -m set --set " + str(rule.srcset) + " src "

            if rule.srcport.exists():
                if (len(rule.dstport.all()) > 1 or len(rule.srcport.all()) > 1):
                    cmp_rule += " -m multiport --sports " + str(','.join([srcport.port for srcport in rule.srcport.all()]))
                else:
                    cmp_rule += " --sport " + str(','.join([srcport.port for srcport in rule.srcport.all()]))

            if rule.destiny.all():
                cmp_rule += " -d " + str(','.join([destiny.getFullAddress() for destiny in rule.destiny.all()]))

            if rule.dstset:
                cmp_rule += " -m set --set " + str(rule.dstset) + " dst "

            if rule.dstport.exists():
                if (len(rule.dstport.all()) > 1 or len(rule.srcport.all()) > 1):
                    cmp_rule += " -m multiport --dports " + str(','.join([dstport.port for dstport in rule.dstport.all()]))
                else:
                    cmp_rule += " --dport " + str(','.join([dstport.port for dstport in rule.dstport.all()]))

            if rule.in_interface:
                cmp_rule += " -i " + str(rule.in_interface.device)

            if rule.out_interface:
                cmp_rule += " -o " + str(rule.out_interface.device)

            if rule.conn_state != '[]':
                states = ("NEW","RELATED","ESTABLISHED","INVALID","UNTRACKED")
                # Convert UNICODE values into a list of strings and after this
                # convert into a integer list to filter the STATES list
                list_states = map(int, (str(rule.conn_state).replace("u'", "").translate(None, "]['")).split(','))
                selected_states = [states[x] for x in list_states]
                cmp_rule += " -m state --state " + (str(selected_states).translate(None, "'[]")).translate(None," ")
                # cmp_rule += " -m state --state " + str(list_states)

            if rule.adv_options:
                cmp_rule += " " + str(rule.adv_options)

            if rule.log:
                if rule.log_preffix:
                    log_rule = "iptables -I " + str(rule.chain) + " " + cmp_rule + \
                               " --log_preffix " + str(rule.log_preffix) + \
                               " --log_level " + str(rule.log_level) + " -j LOG "
                else:
                    log_rule = "iptables -I " + str(rule.chain) + " " + cmp_rule + \
                               " --log_level " + str(rule.log_level) + " -j LOG "
                tmprule.append(log_rule)

            cmp_rule = "iptables -I "  + str(rule.chain) + " " + cmp_rule + " -j " + str(rule.action)

            tmprule.append(cmp_rule)

        return (tmprule)


    @staticmethod
    def natrulecomposer():
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

            if nat.srcport.all():
                cmp_rule += " --sport " + str(','.join([srcport.port for srcport in nat.srcport.all()]))

            if nat.destiny:
                cmp_rule += " -d " + str(nat.destiny.getFullAddress())

            if nat.dstport.all():
                cmp_rule += " --dport " + str(','.join([dstport.port for dstport in nat.dstport.all()]))

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

            if nat.to_destiny:
                cmp_rule += " --to-destination " + str(nat.to_destiny)

            if nat.to_port:
                cmp_rule += " --to-port " + str(nat.to_port)

            tmpnat.append(cmp_rule)

        return (tmpnat)


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

            if nat.to_destiny:
                cmp_rule += " --to-destination " + str(nat.to_destiny)

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

        return (context)


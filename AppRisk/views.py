from django.shortcuts import render
from django.views import generic
from AppRisk.models.rule import Rule, RuleForm
from AppRisk.models.network import Network

# Create your views here.


def rule_view(request):
    rules = Rule.objects.all()
    context = {'rules': rules}
    return render(request, 'rulelistview.html', context)


def network_view(request):
    network = Network.objects.all()
    context = {'network': network}
    return render(request, 'networklistview.html', context)


class RuleListView(generic.ListView):
    model = Rule
    template_name = 'rulelistview.html'


class RuleEditView(generic.FormView):
    form_class = RuleForm
    template_name = 'baseformview.html'
    success_url = '/list/'
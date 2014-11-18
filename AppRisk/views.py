from django.views import generic
from AppRisk.models.rule import Rule, RuleForm

# Create your views here.


class RuleListView(generic.ListView):
    model = Rule
    template_name = 'rulelistview.html'


class RuleEditView(generic.FormView):
    form_class = RuleForm
    template_name = 'baseformview.html'
    success_url = '/list/'
from django.views import generic
from AppRisk.models.risk import Risk
from AppRisk.models.risktype import RiskType
from AppRisk.models.asset import Asset
from AppRisk.models.asset import AssetForm

# Create your views here.


class AssetListView(generic.ListView):
    model = Asset
    template_name = 'assetlistview.html'


class AssetEditView(generic.FormView):
    form_class = AssetForm
    template_name = 'baseformview.html'
    success_url = '/list/'
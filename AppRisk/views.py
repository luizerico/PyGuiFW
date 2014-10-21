from django.views import generic
from models import Asset, Risk, RiskType, AssetForm

# Create your views here.


class AssetListView(generic.ListView):
    model = Asset
    template_name = 'assetlistview.html'


class AssetEditView(generic.FormView):
    form_class = AssetForm
    template_name = 'baseformview.html'
    success_url = '/list/'
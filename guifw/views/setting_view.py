from django.views.generic import DetailView, UpdateView

from guifw.models.setting import Setting
# Create your views here.

class SettingDetail(DetailView):
    model = Setting
    template_name = 'setting_detail.html'

class SettingUpdate(UpdateView):
    model = Setting
    template_name = 'setting_form.html'
    success_url = '/guifw/setting/detail/1'


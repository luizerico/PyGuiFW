from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from AppRisk.models.netset import Netset, FormNetset
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    netsetlist=request.GET.getlist('items[]')
    if netsetlist:
        #Hostset.objects.filter(id__in=netsetlist).delete()
        print "Deleting " + str(netsetlist)

    return HttpResponseRedirect('/apprisk/netset/list')



class NetsetList(ListView):
    model = Netset
    template_name = 'netset_list.html'


class NetsetDetail(DetailView):
    model = Netset
    template_name = 'netset_detail.html'


class NetsetCreate(CreateView):
    model = Netset
    form_class = FormNetset
    template_name = 'netset_form.html'
    success_url = '/apprisk/netset/list'


class NetsetUpdate(UpdateView):
    model = Netset
    form_class = FormNetset
    template_name = 'netset_form.html'
    success_url = '/apprisk/netset/list'


class NetsetDelete(DeleteView):
    model = Netset
    success_url = '/apprisk/netset/list'
    template_name = 'netset_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(NetsetDelete, self).post(request, *args, **kwargs)
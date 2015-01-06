from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from AppRisk.models.hostset import Hostset, FormHostset
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    hostsetlist=request.GET.getlist('items[]')
    if hostsetlist:
        #Hostset.objects.filter(id__in=hostsetlist).delete()
        print "Deleting " + str(hostsetlist)

    return HttpResponseRedirect('/apprisk/hostset/list')



class HostsetList(ListView):
    model = Hostset
    template_name = 'hostset_list.html'


class HostsetDetail(DetailView):
    model = Hostset
    template_name = 'hostset_detail.html'


class HostsetCreate(CreateView):
    model = Hostset
    form_class = FormHostset
    template_name = 'hostset_form.html'
    success_url = '/apprisk/hostset/list'


class HostsetUpdate(UpdateView):
    model = Hostset
    form_class = FormHostset
    template_name = 'hostset_form.html'
    success_url = '/apprisk/hostset/list'


class HostsetDelete(DeleteView):
    model = Hostset
    success_url = '/apprisk/hostset/list'
    template_name = 'hostset_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(HostsetDelete, self).post(request, *args, **kwargs)
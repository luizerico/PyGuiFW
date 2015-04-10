from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from guifw.models.port import Port, FormPort
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    portlist=request.GET.getlist('items[]')
    if portlist:
        #Port.objects.filter(id__in=portlist).delete()
        print "Deleting " + str(portlist)

    return HttpResponseRedirect('/guifw/port/list')



class PortList(ListView):
    model = Port
    template_name = 'port_list.html'


class PortDetail(DetailView):
    model = Port
    template_name = 'port_detail.html'


class PortCreate(CreateView):
    model = Port
    form_class = FormPort
    template_name = 'port_form.html'
    success_url = '/guifw/port/list'


class PortUpdate(UpdateView):
    model = Port
    form_class = FormPort
    template_name = 'port_form.html'
    success_url = '/guifw/port/list'


class PortDelete(DeleteView):
    model = Port
    success_url = '/guifw/port/list'
    template_name = 'port_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(PortDelete, self).post(request, *args, **kwargs)
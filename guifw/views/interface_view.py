from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from guifw.models.interface import Interface, FormInterface
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    interfacelist=request.GET.getlist('items[]')
    if interfacelist:
        #Interface.objects.filter(id__in=interfacelist).delete()
        print "Deleting " + str(interfacelist)

    return HttpResponseRedirect('/guifw/interface/list')



class InterfaceList(ListView):
    model = Interface
    template_name = 'interface_list.html'


class InterfaceDetail(DetailView):
    model = Interface
    template_name = 'interface_detail.html'


class InterfaceCreate(CreateView):
    model = Interface
    form_class = FormInterface
    template_name = 'interface_form.html'
    success_url = '/guifw/interface/list'


class InterfaceUpdate(UpdateView):
    model = Interface
    form_class = FormInterface
    template_name = 'interface_form.html'
    success_url = '/guifw/interface/list'


class InterfaceDelete(DeleteView):
    model = Interface
    success_url = '/guifw/interface/list'
    template_name = 'interface_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(InterfaceDelete, self).post(request, *args, **kwargs)
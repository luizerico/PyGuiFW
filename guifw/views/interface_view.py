from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

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

def usedBy(self):
    used = []
    for use in self.filter_inin.all():
        used.append(["filter", "Interface Out", use.order, str(use.name), use.id])
    for use in self.filter_inout.all():
        used.append(["filter", "Interface In", use.order, str(use.name), use.id])
    for use in self.nat_inin.all():
        used.append(["nat", "Interface Out", use.order, str(use.name), use.id])
    for use in self.nat_inout.all():
        used.append(["nat", "Interface In", use.order, str(use.name), use.id])
    for use in self.shappclass_in.all():
        used.append(["shappclass", "Interface", "---", str(use.name), use.id])

    return used


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

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/interface/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(InterfaceDelete, self).post(request, *args, **kwargs)
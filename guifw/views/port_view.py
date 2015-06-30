from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

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

def usedBy(self):
    used = []
    for use in self.filter_srcport.all():
        used.append(["filter", "Source Port", use.order, str(use.name), use.id])
    for use in self.filter_dstport.all():
        used.append(["filter", "Destiny Port", use.order, str(use.name), use.id])
    for use in self.nat_srcport.all():
        used.append(["nat", "Source Port", use.order, str(use.name), use.id])
    for use in self.nat_dstport.all():
        used.append(["nat:", "Destiny Port", use.order, str(use.name), use.id])
    for use in self.nat_to_port.all():
        used.append(["nat", "To Port", use.order, str(use.name), use.id])
    for use in self.shapp_srcport.all():
        used.append(["shapping", "Source Port", use.order, str(use.name), use.id])
    for use in self.shapp_dstport.all():
        used.append(["shapping","Source Port", use.order, str(use.name), use.id])

    return used



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

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/port/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(PortDelete, self).post(request, *args, **kwargs)
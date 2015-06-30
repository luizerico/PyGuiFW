from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.host import Host, FormHost
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    hostlist=request.GET.getlist('hosts[]')
    if hostlist:
        #Host.objects.filter(id__in=hostlist).delete()
        print "Deleting " + str(hostlist)

    return HttpResponseRedirect('/guifw/host/list')

def usedBy(self):
    used = []
    for use in self.filter_source.all():
        used.append(["filter", "Source", use.order, str(use.name), use.id])
    for use in self.filter_destiny.all():
        used.append(["filter", "Destiny", use.order, str(use.name), use.id])
    for use in self.nat_source.all():
        used.append(["nat", "Source", use.order, str(use.name), use.id])
    for use in self.nat_destiny.all():
        used.append(["nat:", "Destiny", use.order, str(use.name), use.id])
    for use in self.nat_to_ip.all():
        used.append(["nat", "To", use.order, str(use.name), use.id])
    for use in self.shapp_source.all():
        used.append(["shapping", "Source", use.order, str(use.name), use.id])
    for use in self.hostset_address.all():
        used.append(["hostset","---", "---", str(use.name), use.id])
    return used


class HostList(ListView):
    model = Host
    template_name = 'host_list.html'


class HostDetail(DetailView):
    model = Host
    template_name = 'host_detail.html'


class HostCreate(CreateView):
    model = Host
    form_class = FormHost
    template_name = 'host_form.html'
    success_url = '/guifw/host/list'


class HostUpdate(UpdateView):
    model = Host
    form_class = FormHost
    template_name = 'host_form.html'
    success_url = '/guifw/host/list'


class HostDelete(DeleteView):
    model = Host
    success_url = '/guifw/host/list'
    template_name = 'host_delete.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/host/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(HostDelete, self).post(request, *args, **kwargs)
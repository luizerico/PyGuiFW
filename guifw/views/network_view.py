from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.network import Network, FormNetwork
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    networklist=request.GET.getlist('items[]')
    if networklist:
        #Network.objects.filter(id__in=networklist).delete()
        print "Deleting " + str(networklist)

    return HttpResponseRedirect('/guifw/network/list')

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
    for use in self.nat_toip.all():
        used.append(["nat", "To", use.order, str(use.name), use.id])
    for use in self.shapp_source.all():
        used.append(["shapping", "Source", use.order, str(use.name), use.id])
    for use in self.shapp_destiny.all():
        used.append(["shapping", "Destiny", use.order, str(use.name), use.id])
    for use in self.netset_address.all():
        used.append(["netset","---", "---", str(use.name), use.id])
    return used


class NetworkList(ListView):
    model = Network
    template_name = 'network_list.html'


class NetworkDetail(DetailView):
    model = Network
    template_name = 'network_detail.html'


class NetworkCreate(CreateView):
    model = Network
    form_class = FormNetwork
    template_name = 'network_form.html'
    success_url = '/guifw/network/list'


class NetworkUpdate(UpdateView):
    model = Network
    form_class = FormNetwork
    template_name = 'network_form.html'
    success_url = '/guifw/network/list'


class NetworkDelete(DeleteView):
    model = Network
    success_url = '/guifw/network/list'
    template_name = 'network_delete.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/network/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(NetworkDelete, self).post(request, *args, **kwargs)
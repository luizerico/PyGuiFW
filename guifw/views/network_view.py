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
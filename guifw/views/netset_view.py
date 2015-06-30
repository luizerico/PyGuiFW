from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.netset import Netset, FormNetset
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    netsetlist=request.GET.getlist('items[]')
    if netsetlist:
        #Hostset.objects.filter(id__in=netsetlist).delete()
        print "Deleting " + str(netsetlist)

    return HttpResponseRedirect('/guifw/netset/list')

def usedBy(self):
    used = []
    for use in self.filter_srcset.all():
        used.append(["filter", "Source", use.order, str(use.name), use.id])
    for use in self.filter_dstset.all():
        used.append(["filter", "Destiny", use.order, str(use.name), use.id])
    return used


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
    success_url = '/guifw/netset/list'


class NetsetUpdate(UpdateView):
    model = Netset
    form_class = FormNetset
    template_name = 'netset_form.html'
    success_url = '/guifw/netset/list'


class NetsetDelete(DeleteView):
    model = Netset
    success_url = '/guifw/netset/list'
    template_name = 'netset_delete.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/netset/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(NetsetDelete, self).post(request, *args, **kwargs)
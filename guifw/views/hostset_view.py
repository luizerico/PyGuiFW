from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.hostset import Hostset, FormHostset
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    hostsetlist=request.GET.getlist('items[]')
    if hostsetlist:
        #Hostset.objects.filter(id__in=hostsetlist).delete()
        print "Deleting " + str(hostsetlist)

    return HttpResponseRedirect('/guifw/hostset/list')

def usedBy(self):
    used = []
    for use in self.filter_srcset.all():
        used.append(["filter", "Source", use.order, str(use.name), use.id])
    for use in self.filter_dstset.all():
        used.append(["filter", "Destiny", use.order, str(use.name), use.id])
    return used

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
    success_url = '/guifw/hostset/list'


class HostsetUpdate(UpdateView):
    model = Hostset
    form_class = FormHostset
    template_name = 'hostset_form.html'
    success_url = '/guifw/hostset/list'


class HostsetDelete(DeleteView):
    model = Hostset
    success_url = '/guifw/hostset/list'
    template_name = 'hostset_delete.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/hostset/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(HostsetDelete, self).post(request, *args, **kwargs)
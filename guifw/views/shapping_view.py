from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from guifw.models.shapping import Shapping
# Create your views here.

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    shappinglist=request.GET.getlist('items[]')
    if shappinglist:
        #Shapping.objects.shapping(id__in=shappinglist).delete()
        print "Deleting " + str(shappinglist)

    return HttpResponseRedirect('/guifw/shapping/list')


class ShappingList(ListView):
    model = Shapping
    template_name = 'shapping_list.html'


class ShappingDetail(DetailView):
    model = Shapping
    template_name = 'shapping_detail.html'


class ShappingCreate(CreateView):
    model = Shapping
    #form_class = FormShapping
    template_name = 'shapping_form.html'
    success_url = '/guifw/shapping/list'


class ShappingUpdate(UpdateView):
    model = Shapping
    #form_class = FormShapping
    template_name = 'shapping_form.html'
    success_url = '/guifw/shapping/list'


class ShappingDelete(DeleteView):
    model = Shapping
    success_url = '/guifw/shapping/list'
    template_name = 'shapping_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ShappingDelete, self).post(request, *args, **kwargs)
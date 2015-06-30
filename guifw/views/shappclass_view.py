from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.shappclass import Shappclass
# Create your views here.

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    shappclasslist=request.GET.getlist('items[]')
    if shappclasslist:
        #Shappclass.objects.shappclass(id__in=shappclasslist).delete()
        print "Deleting " + str(shappclasslist)

    return HttpResponseRedirect('/guifw/shappclass/list')

def usedBy(self):
    used = []
    for use in self.shapp_class.all():
        used.append(["shappclass", "Interface", "---", str(use.name), use.id])
    return used


class ShappclassList(ListView):
    model = Shappclass
    template_name = 'shappclass_list.html'


class ShappclassDetail(DetailView):
    model = Shappclass
    template_name = 'shappclass_detail.html'


class ShappclassCreate(CreateView):
    model = Shappclass
    #form_class = FormShappclass
    template_name = 'shappclass_form.html'
    success_url = '/guifw/shappclass/list'


class ShappclassUpdate(UpdateView):
    model = Shappclass
    #form_class = FormShappclass
    template_name = 'shappclass_form.html'
    success_url = '/guifw/shappclass/list'


class ShappclassDelete(DeleteView):
    model = Shappclass
    success_url = '/guifw/shappclass/list'
    template_name = 'shappclass_delete.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/shappclass/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ShappclassDelete, self).post(request, *args, **kwargs)
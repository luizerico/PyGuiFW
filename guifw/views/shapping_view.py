from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F, Max


from guifw.models.shapping import Shapping

def ShappingReorder(request, order_id):
    Shapping.objects.Shapping(order__gte=order_id).update(order=F('order') + 1)
    return HttpResponseRedirect('/guifw/shapping/list')

def ShappingReorderUp(request, order_id):
    previous = int(order_id).__sub__(1)
    Shapping.objects.filter(order=previous).update(order='-1')
    Shapping.objects.filter(order=order_id).update(order=F('order') - 1)
    Shapping.objects.filter(order=-1).update(order=order_id)
    return HttpResponseRedirect('/guifw/shapping/list')

def ShappingReorderDown(request, order_id):
    if (int(order_id) != Shapping.objects.latest('order').order):
        previous = int(order_id).__add__(1)
        Shapping.objects.filter(order=previous).update(order='-1')
        Shapping.objects.filter(order=order_id).update(order=F('order') + 1)
        Shapping.objects.filter(order=-1).update(order=order_id)
    return HttpResponseRedirect('/guifw/shapping/list')

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
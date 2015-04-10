from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.db.models import F

from guifw.models.filter import Filter, FormFilter
# Create your views here.


def FilterReorder(request, order_id):
    Filter.objects.filter(order__gte=order_id).update(order=F('order') + 1)
    return HttpResponseRedirect('/guifw/filter/list')

def FilterReorderUp(request, order_id):
    previous = int(order_id).__sub__(1)
    Filter.objects.filter(order=previous).update(order='-1')
    Filter.objects.filter(order=order_id).update(order=F('order') - 1)
    Filter.objects.filter(order=-1).update(order=order_id)
    return HttpResponseRedirect('/guifw/filter/list')

def FilterReorderDown(request, order_id):
    previous = int(order_id).__add__(1)
    Filter.objects.filter(order=previous).update(order='-1')
    Filter.objects.filter(order=order_id).update(order=F('order') + 1)
    Filter.objects.filter(order=-1).update(order=order_id)
    return HttpResponseRedirect('/guifw/filter/list')

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    filterlist=request.GET.getlist('items[]')
    if filterlist:
        #Filter.objects.filter(id__in=filterlist).delete()
        print "Deleting " + str(filterlist)

    return HttpResponseRedirect('/guifw/filter/list')


class FilterList(ListView):
    model = Filter
    template_name = 'filter_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FilterList, self).dispatch(*args, **kwargs)


class FilterDetail(DetailView):
    model = Filter
    template_name = 'filter_detail.html'


class FilterCreate(CreateView):
    model = Filter
    form_class = FormFilter
    template_name = 'filter_form.html'
    success_url = '/guifw/filter/list'


class FilterUpdate(UpdateView):
    model = Filter
    form_class = FormFilter
    template_name = 'filter_form.html'
    success_url = '/guifw/filter/list'


class FilterDelete(DeleteView):
    model = Filter
    success_url = '/guifw/filter/list'
    template_name = 'filter_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(FilterDelete, self).post(request, *args, **kwargs)
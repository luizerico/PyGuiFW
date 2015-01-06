from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from AppRisk.models.filter import Filter, FormFilter
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    filterlist=request.GET.getlist('items[]')
    if filterlist:
        #Filter.objects.filter(id__in=filterlist).delete()
        print "Deleting " + str(filterlist)

    return HttpResponseRedirect('/apprisk/filter/list')



class FilterList(ListView):
    model = Filter
    template_name = 'filter_list.html'


class FilterDetail(DetailView):
    model = Filter
    template_name = 'filter_detail.html'


class FilterCreate(CreateView):
    model = Filter
    form_class = FormFilter
    template_name = 'filter_form.html'
    success_url = '/apprisk/filter/list'


class FilterUpdate(UpdateView):
    model = Filter
    form_class = FormFilter
    template_name = 'filter_form.html'
    success_url = '/apprisk/filter/list'


class FilterDelete(DeleteView):
    model = Filter
    success_url = '/apprisk/filter/list'
    template_name = 'filter_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(FilterDelete, self).post(request, *args, **kwargs)
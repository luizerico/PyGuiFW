from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from AppRisk.models.chain import Chain, FormChain
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    chainlist=request.GET.getlist('items[]')
    if chainlist:
        #Chain.objects.filter(id__in=chainlist).delete()
        print "Deleting " + str(chainlist)

    return HttpResponseRedirect('/apprisk/chain/list')



class ChainList(ListView):
    model = Chain
    template_name = 'chain_list.html'


class ChainDetail(DetailView):
    model = Chain
    template_name = 'chain_detail.html'


class ChainCreate(CreateView):
    model = Chain
    form_class = FormChain
    template_name = 'chain_form.html'
    success_url = '/apprisk/chain/list'


class ChainUpdate(UpdateView):
    model = Chain
    form_class = FormChain
    template_name = 'chain_form.html'
    success_url = '/apprisk/chain/list'


class ChainDelete(DeleteView):
    model = Chain
    success_url = '/apprisk/chain/list'
    template_name = 'chain_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ChainDelete, self).post(request, *args, **kwargs)
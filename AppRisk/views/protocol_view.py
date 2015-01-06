from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from AppRisk.models.protocol import Protocol, FormProtocol
# Create your views here.


def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    protocollist=request.GET.getlist('items[]')
    if protocollist:
        #Protocol.objects.filter(id__in=protocollist).delete()
        print "Deleting " + str(protocollist)

    return HttpResponseRedirect('/apprisk/protocol/list')



class ProtocolList(ListView):
    model = Protocol
    template_name = 'protocol_list.html'


class ProtocolDetail(DetailView):
    model = Protocol
    template_name = 'protocol_detail.html'


class ProtocolCreate(CreateView):
    model = Protocol
    form_class = FormProtocol
    template_name = 'protocol_form.html'
    success_url = '/apprisk/protocol/list'


class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = FormProtocol
    template_name = 'protocol_form.html'
    success_url = '/apprisk/protocol/list'


class ProtocolDelete(DeleteView):
    model = Protocol
    success_url = '/apprisk/protocol/list'
    template_name = 'protocol_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ProtocolDelete, self).post(request, *args, **kwargs)
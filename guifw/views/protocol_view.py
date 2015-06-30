from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.protocol import Protocol, FormProtocol
# Create your views here.


def multipleDelete(request):

    protocollist=request.GET.getlist('items[]')
    if protocollist:
        #Protocol.objects.filter(id__in=protocollist).delete()
        print "Deleting " + str(protocollist)

    return HttpResponseRedirect('/guifw/protocol/list')

def usedBy(self):
    used = []
    for use in self.filter_protocol.all():
        used.append(["filter", "Protocol", use.order, str(use.name), use.id])
    for use in self.nat_protocol.all():
        used.append(["nat", "Protocol", use.order, str(use.name), use.id])

    return used

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
    success_url = '/guifw/protocol/list'


class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = FormProtocol
    template_name = 'protocol_form.html'
    success_url = '/guifw/protocol/list'


class ProtocolDelete(DeleteView):
    model = Protocol
    success_url = '/guifw/protocol/list'
    template_name = 'protocol_delete.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/protocol/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ProtocolDelete, self).post(request, *args, **kwargs)
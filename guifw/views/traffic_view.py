from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from guifw.models.traffic import Traffic
# Create your views here.

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    trafficlist=request.GET.getlist('items[]')
    if trafficlist:
        #Traffic.objects.traffic(id__in=trafficlist).delete()
        print "Deleting " + str(trafficlist)

    return HttpResponseRedirect('/guifw/traffic/list')


class TrafficList(ListView):
    model = Traffic
    template_name = 'traffic_list.html'


class TrafficDetail(DetailView):
    model = Traffic
    template_name = 'traffic_detail.html'


class TrafficCreate(CreateView):
    model = Traffic
    #form_class = FormTraffic
    template_name = 'traffic_form.html'
    success_url = '/guifw/traffic/list'


class TrafficUpdate(UpdateView):
    model = Traffic
    #form_class = FormTraffic
    template_name = 'traffic_form.html'
    success_url = '/guifw/traffic/list'


class TrafficDelete(DeleteView):
    model = Traffic
    success_url = '/guifw/traffic/list'
    template_name = 'traffic_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(TrafficDelete, self).post(request, *args, **kwargs)
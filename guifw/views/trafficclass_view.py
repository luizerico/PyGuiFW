from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from guifw.models.trafficclass import Trafficclass
# Create your views here.

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    trafficclasslist=request.GET.getlist('items[]')
    if trafficclasslist:
        #Trafficclass.objects.trafficclass(id__in=trafficclasslist).delete()
        print "Deleting " + str(trafficclasslist)

    return HttpResponseRedirect('/guifw/trafficclass/list')


class TrafficclassList(ListView):
    model = Trafficclass
    template_name = 'trafficclass_list.html'


class TrafficclassDetail(DetailView):
    model = Trafficclass
    template_name = 'trafficclass_detail.html'


class TrafficclassCreate(CreateView):
    model = Trafficclass
    #form_class = FormTrafficclass
    template_name = 'trafficclass_form.html'
    success_url = '/guifw/trafficclass/list'


class TrafficclassUpdate(UpdateView):
    model = Trafficclass
    #form_class = FormTrafficclass
    template_name = 'trafficclass_form.html'
    success_url = '/guifw/trafficclass/list'


class TrafficclassDelete(DeleteView):
    model = Trafficclass
    success_url = '/guifw/trafficclass/list'
    template_name = 'trafficclass_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(TrafficclassDelete, self).post(request, *args, **kwargs)
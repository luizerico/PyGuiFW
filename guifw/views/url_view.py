from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from guifw.models.url import URL, FormURL
# Create your views here.

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms

    urllist=request.GET.getlist('items[]')
    if urllist:
        #url.objects.filter(id__in=urllist).delete()
        print "Deleting " + str(urllist)

    return HttpResponseRedirect('/guifw/url/list')



class URLList(ListView):
    model = URL
    template_name = 'url_list.html'


class URLDetail(DetailView):
    model = URL
    template_name = 'url_detail.html'


class URLCreate(CreateView):
    model = URL
    form_class = FormURL
    template_name = 'url_form.html'
    success_url = '/guifw/url/list'


class URLUpdate(UpdateView):
    model = URL
    form_class = FormURL
    template_name = 'url_form.html'
    success_url = '/guifw/url/list'


class URLDelete(DeleteView):
    model = URL
    success_url = '/guifw/url/list'
    template_name = 'url_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(URLDelete, self).post(request, *args, **kwargs)
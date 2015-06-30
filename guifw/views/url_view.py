from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from guifw.models.url import URL, FormURL

# Create your views here.

def multipleDelete(request):
    urllist=request.GET.getlist('items[]')
    if urllist:
        #url.objects.filter(id__in=urllist).delete()
        print "Deleting " + str(urllist)
    return HttpResponseRedirect('/guifw/url/list')

def usedBy(self):
    used = []
    for use in self.filter_source.all():
        used.append(["filter", "Source", use.order, str(use.name), use.id])
    for use in self.filter_destiny.all():
        used.append(["filter", "Destiny", use.order, str(use.name), use.id])
    for use in self.nat_source.all():
        used.append(["nat", "Source", use.order, str(use.name), use.id])
    for use in self.nat_destiny.all():
        used.append(["nat:", "Destiny", use.order, str(use.name), use.id])
    for use in self.nat_toip.all():
        used.append(["nat", "To", use.order, str(use.name), use.id])
    for use in self.shapp_source.all():
        used.append(["shapping", "Source", use.order, str(use.name), use.id])
    for use in self.shapp_destiny.all():
        used.append(["shapping", "Destiny", use.order, str(use.name), use.id])
    return used


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

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['used'] = usedBy(self.object)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect('/guifw/url/list')
        except ProtectedError as e:
            result = {'error': str(e)}
            return render(request,'error.html',result)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(URLDelete, self).post(request, *args, **kwargs)
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F, Max

from guifw.models.nat import Nat, FormNat

def NatReorder(request, order_id):
    Nat.objects.nat(order__gte=order_id).update(order=F('order') + 1)
    return HttpResponseRedirect('/guifw/nat/list')

def NatReorderUp(request, order_id):
    previous = int(order_id).__sub__(1)
    Nat.objects.filter(order=previous).update(order='-1')
    Nat.objects.filter(order=order_id).update(order=F('order') - 1)
    Nat.objects.filter(order=-1).update(order=order_id)
    return HttpResponseRedirect('/guifw/nat/list')

def NatReorderDown(request, order_id):
    if (int(order_id) != Nat.objects.latest('order').order):
        previous = int(order_id).__add__(1)
        Nat.objects.filter(order=previous).update(order='-1')
        Nat.objects.filter(order=order_id).update(order=F('order') + 1)
        Nat.objects.filter(order=-1).update(order=order_id)
    return HttpResponseRedirect('/guifw/nat/list')

def multipleDelete(request):
    # To implement best ways to delete multiple registers
    # To implement validation checks
    # Avoid insecures algorithms
    natlist=request.GET.getlist('items[]')
    if natlist:
        #Nat.objects.nat(id__in=natlist).delete()
        print "Deleting " + str(natlist)
    return HttpResponseRedirect('/guifw/nat/list')


class NatList(ListView):
    model = Nat
    template_name = 'nat_list.html'


class NatDetail(DetailView):
    model = Nat
    template_name = 'nat_detail.html'


class NatCreate(CreateView):
    model = Nat
    form_class = FormNat
    template_name = 'nat_form.html'
    success_url = '/guifw/nat/list'


class NatUpdate(UpdateView):
    model = Nat
    form_class = FormNat
    template_name = 'nat_form.html'
    success_url = '/guifw/nat/list'


class NatDelete(DeleteView):
    model = Nat

    success_url = '/guifw/nat/list'
    template_name = 'nat_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(NatDelete, self).post(request, *args, **kwargs)
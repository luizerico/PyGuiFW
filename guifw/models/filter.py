from django.db import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import F

from guifw.models.interface import Interface
from guifw.models.port import Port
from guifw.models.protocol import Protocol
from guifw.models.address import Address
from guifw.models.chain import Chain
from guifw.models.Ipset import Ipset

from guifw.library.sysnet import Sysnet

# Create your models here.

class Filter(models.Model):
    ACTION = (('ACCEPT','ACCEPT'),('DROP','DROP'),('REJECT','REJECT'))
    CONNECTION = ((0,'NEW'),(1, 'RELATED'),(2,'ESTABLISHED'),(3,'INVALID'),(4,'UNTRACKED'))
    LOG_LEVEL = (('debug','debug'),('info','info'),('notice','notice'),('warning','warning'),('error','error'),
                 ('crit','crit'),('alert','alert'),('emerg','emerg'))

    order = models.IntegerField()
    name = models.CharField(max_length=250)
    chain = models.ForeignKey(Chain)
    source = models.ManyToManyField(Address, blank=True, related_name='source')
    srcset = models.ForeignKey(Ipset, null=True, blank=True, related_name='src_set')
    srcport = models.ManyToManyField(Port, blank=True, related_name='srcport')
    destiny = models.ManyToManyField(Address, blank=True, related_name='destiny')
    dstset = models.ForeignKey(Ipset, null=True, blank=True, related_name='dst_set')
    dstport = models.ManyToManyField(Port, blank=True, related_name='dstport')
    protocol = models.ForeignKey(Protocol, null=True, blank=True)
    in_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='in_in')
    out_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='in_out')
    #connection = models.ForeignKey(Connection, null=True, blank=True)
    conn_state = models.CharField(max_length=150, null=True, blank=True)
    adv_options = models.CharField(max_length=250, blank=True)
    action = models.CharField(max_length=20, choices=ACTION, default='DROP')
    description = models.TextField(blank=True)
    log = models.BooleanField(default=False)
    log_level = models.CharField(max_length=20, choices=LOG_LEVEL, default='WARN')
    log_preffix = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self):
        if (Filter.objects.filter(order = self.order)):
            Filter.objects.filter(order__gte = self.order).update(order=F('order') + 1)
            print "OK"
        print self.order
        super(Filter, self).save()

    def delete(self):
        Filter.objects.filter(order__gte = self.order).update(order=F('order') - 1)
        print self.order
        super(Filter, self).delete()


class FormFilter(forms.ModelForm):
    conn_state = forms.MultipleChoiceField(required=False,
                                           widget=forms.CheckboxSelectMultiple(),
                                           choices=Filter.CONNECTION)
    source = forms.ModelMultipleChoiceField(Address.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Source', False,attrs={}))
    destiny = forms.ModelMultipleChoiceField(Address.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Destiny', False,attrs={}))
    srcport = forms.ModelMultipleChoiceField(Port.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Source Port', False,attrs={}))
    dstport = forms.ModelMultipleChoiceField(Port.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Destiny Port', False,attrs={}))

    def clean(self):
        cleaned_data = super(FormFilter, self).clean()
        if not (bool(self.cleaned_data['srcset']) !=  bool(self.cleaned_data['source'])):
            raise forms.ValidationError, 'Fill in only one of the two source fields'

        if not (bool(self.cleaned_data['dstset']) !=  bool(self.cleaned_data['destiny'])):
            raise forms.ValidationError, 'Fill in only one of the two destiny fields'

        return cleaned_data

    class Meta:
        model = Filter
        permissions = (("can_view_filter", "Can view filter"),
                       ("can_edit_filter", "Can edit filter"),)
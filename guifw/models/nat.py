from django.db import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import F
from audit_log.models.managers import AuditLog
from guifw.models.interface import Interface
from guifw.models.port import Port
from guifw.models.protocol import Protocol
from guifw.models.address import Address


class Nat(models.Model):
    ACTION = (
    ('REDIRECT', 'Redirect'), ('SNAT', 'Source NAT'), ('DNAT', 'Destination NAT'), ('MASQUERADE', 'Masquerade'))
    LOG_LEVEL = (('debug', 'debug'), ('info', 'info'), ('notice', 'notice'), ('warning', 'warning'), ('error', 'error'),
                 ('crit', 'crit'), ('alert', 'alert'), ('emerg', 'emerg'))
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    action = models.CharField(max_length=20, choices=ACTION, default='DNAT')
    source = models.ForeignKey(Address, blank=True, null=True, related_name='nat_source')
    srcport = models.ManyToManyField(Port, blank=True, related_name='nat_srcport')
    destiny = models.ForeignKey(Address, blank=True, null=True, related_name='nat_destiny')
    dstport = models.ManyToManyField(Port, blank=True, related_name='nat_dstport')
    protocol = models.ForeignKey(Protocol, null=True, blank=True, related_name="nat_protocol", on_delete=models.PROTECT)
    in_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='nat_inin', on_delete=models.PROTECT)
    out_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='nat_inout', on_delete=models.PROTECT)
    to_ip = models.ForeignKey(Address, blank=True, null=True, related_name='nat_toip')
    to_port = models.ForeignKey(Port, blank=True, null=True, related_name='nat_toport')
    adv_options = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True)
    log = models.BooleanField(default=False)
    log_level = models.CharField(max_length=20, choices=LOG_LEVEL, default='WARN')
    log_preffix = models.CharField(max_length=100, blank=True)
    audit_log = AuditLog()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self):
        if self.pk is not None:
            if (Nat.objects.filter(order=self.order)):
                orig = Nat.objects.get(pk=self.pk)
                if orig.order > self.order:
                    Nat.objects.filter(order__lt=orig.order, order__gte=self.order).update(order=F('order') + 1)
                elif orig.order < self.order:
                    Nat.objects.filter(order__lte=self.order, order__gte=orig.order).update(order=F('order') - 1)
        else:
            Nat.objects.filter(order__gte=self.order).update(order=F('order') + 1)

        super(Nat, self).save()

    def delete(self):
        Nat.objects.filter(order__gte=self.order).update(order=F('order') - 1)
        print self.order
        super(Nat, self).delete()


class FormNat(forms.ModelForm):
    # source = forms.ModelMultipleChoiceField(Address.objects.all(), required=False,
    #                                        widget=FilteredSelectMultiple('Source', False,attrs={}))
    # destiny = forms.ModelMultipleChoiceField(Address.objects.all(), required=False,
    #                                        widget=FilteredSelectMultiple('Destiny', False,attrs={}))
    srcport = forms.ModelMultipleChoiceField(Port.objects.all(), required=False,
                                             widget=FilteredSelectMultiple('Source Port', False, attrs={}))
    dstport = forms.ModelMultipleChoiceField(Port.objects.all(), required=False,
                                             widget=FilteredSelectMultiple('Destiny Port', False, attrs={}))

    def clean(self):
        cleaned_data = super(FormNat, self).clean()
        if (self.cleaned_data['action'] == 'MASQUERADE'):
            if (bool(self.cleaned_data['in_interface']) or \
                        bool(self.cleaned_data['to_ip']) or \
                        bool(self.cleaned_data['to_port'])):
                raise forms.ValidationError, 'Masquerade dont accept in_interface, to_ip or to_port.'
            if not (bool(self.cleaned_data['out_interface'])):
                raise forms.ValidationError, 'Masquerade needs out_interface option.'

        if (self.cleaned_data['action'] == 'REDIRECT'):
            if (bool(self.cleaned_data['out_interface']) or \
                        bool(self.cleaned_data['to_ip'])):
                raise forms.ValidationError, 'Redirect dont accept out_interface or to_ip.'
            if not (bool(self.cleaned_data['to_port']) or bool(self.cleaned_data['protocol'])):
                raise forms.ValidationError, 'Redirect needs protocol and to_port options.'

        if (self.cleaned_data['action'] == 'SNAT'):
            if (bool(self.cleaned_data['in_interface'])):
                raise forms.ValidationError, 'Source NAT dont accept in_interface.'
            if (not bool(self.cleaned_data['out_interface']) or \
                        not bool(self.cleaned_data['protocol'])) or \
                    not bool(self.cleaned_data['to_ip']):
                raise forms.ValidationError, 'Source NAT needs protocol, to_ip and out_interface options.'

        if (self.cleaned_data['action'] == 'DNAT'):
            if (bool(self.cleaned_data['out_interface'])):
                raise forms.ValidationError, 'Destination NAT dont accept out_interface.'
            if (not bool(self.cleaned_data['in_interface']) or \
                        not bool(self.cleaned_data['protocol'])) or \
                    not bool(self.cleaned_data['to_ip']):
                raise forms.ValidationError, 'Destination NAT needs protocol, to_ip and in_interface options.'

        return cleaned_data

    class Meta:
        model = Nat

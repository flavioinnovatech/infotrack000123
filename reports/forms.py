# -*- coding: utf-8 -*-

from django.forms import *
from django.db.models import Q
from django.contrib.admin.widgets import *
from django.core.exceptions import ObjectDoesNotExist
from itrack.equipments.models import CustomFieldName
from itrack.system.models import System
from itrack.vehicles.models import Vehicle


VEHICLE_CHOICES = (("license_plate","Placa"),("date","Data"),("type","Tipo de veículo"),("address","Endereço"),("system","Sistema"),("color","Cor"),("year","Ano"),("model","Modelo"),("manufacturer","Fabricante"),("chassi","Chassi"))

class ReportForm(Form):
    title = CharField(max_length=200,label=u"Título",required=False)
    vehicle = ChoiceField(label=u"Veículo",widget=Select(attrs={'class':'switcher'}))
    period_start = DateTimeField(widget=DateTimeInput(attrs={'class':'datepicker'}),label=u"Data inicial")
    period_end = DateTimeField(widget=DateTimeInput(attrs={'class':'datepicker'}),label=u"Data final")
    vehicle_fields = MultipleChoiceField(choices=VEHICLE_CHOICES,required=False,widget=FilteredSelectMultiple(u"Dados do veículo",False,attrs={'rows':'30'}))
    fields = ModelMultipleChoiceField(CustomFieldName.objects.all(),widget=FilteredSelectMultiple("Campos",False,attrs={'rows':'30'}),required=False)
    
    
    def __init__(self, system, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
                
        #self.fields['vehicle'].queryset = Vehicle.objects.filter(system=system)
        self.fields['vehicle_fields'].initial = ["license_plate","date","type","address","system","color","year","model","manufacturer","chassi"]
        self.fields['fields'].queryset = CustomFieldName.objects.filter(system=system).filter(custom_field__availablefields__system= system).distinct()
                
        choices = [(v.id, unicode(v)) for v in Vehicle.objects.filter(Q(equipment__system=system)&Q(erased=False))]
        choices.extend([("-1","Outro:")])
        
        try:
            if args[0].has_key('vehicle_other'):
                try:
                    v_oth = Vehicle.objects.get(pk=int(args[0]['vehicle']))
                    choices.extend([(v_oth.id,unicode(v_oth))])
                except ObjectDoesNotExist:
                    pass
        except IndexError:
            pass
        
        
        self.fields['vehicle'].choices = choices
        
        
        


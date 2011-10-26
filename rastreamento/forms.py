from itrack.vehicles.models import Vehicle
from itrack.equipments.models import CustomFieldName
from django.forms import *
from django.contrib.admin.widgets import *

class ConfigForm(Form):

    vehicles = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple("Veiculos",False,attrs={'rows':'30'}))
    custom_names = ModelMultipleChoiceField(CustomFieldName.objects.all(),widget= FilteredSelectMultiple("Campos",False,attrs={'rows':'30'}))
    

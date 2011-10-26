from itrack.equipments.models import CustomField, Equipment, Tracking,TrackingData, AvailableFields, EquipmentType, CustomFieldName
from django.contrib import admin


class AvailableAdmin(admin.ModelAdmin):
    filter_horizontal = ["custom_fields"]
    
class EquipTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ["custom_field"]
    
class CustomFieldAdmin(admin.ModelAdmin):
    list_display=['name','pk','tag','type']
    list_editable=['tag','type']
    
class CustomFieldNameAdmin(admin.ModelAdmin):
    list_display = ['id','name','custom_field','system']
    list_editable = ['name','custom_field','system']
    
class TrackingAdmin(admin.ModelAdmin):
    list_display=['eventdate','msgtype']
    
    
admin.site.register(CustomFieldName,CustomFieldNameAdmin)
admin.site.register(CustomField,CustomFieldAdmin)
admin.site.register(Tracking,TrackingAdmin)
admin.site.register(TrackingData)
admin.site.register(Equipment)
admin.site.register(EquipmentType, EquipTypeAdmin)
admin.site.register(AvailableFields,AvailableAdmin)

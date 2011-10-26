from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from django.contrib.auth.views import login,logout,logout_then_login,password_reset,password_reset_done,password_reset_complete,password_reset_confirm
from django.conf import settings
from itrack.system.forms import UserCompleteForm, SettingsForm, SystemForm, SystemWizard

from django.contrib.gis import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
url(r'^$', 'main.views.index'),
url(r'^accounts/login/$', 'accounts.views.login' ),
url(r'^accounts/logout/$', logout_then_login),
url(r'^accounts/$', 'accounts.views.index'),
url(r'^accounts/password/reset/$', password_reset, {'template_name': 'accounts/templates/password_reset_form.html','email_template_name': 'accounts/templates/password_reset_email.html','post_reset_redirect' : '/accounts/password/reset/done/'}),
url(r'^accounts/password/reset/done/$', password_reset_done, {'template_name': 'accounts/templates/password_reset_done.html'}),
url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'accounts/templates/password_reset_confirm.html','post_reset_redirect' : '/accounts/password/done/'}), 
url(r'^accounts/password/done/$',password_reset_complete, {'template_name': 'accounts/templates/password_reset_complete.html'}),

url(r'^admin/', include(admin.site.urls)),
url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
url(r'^accounts/profile/$', 'main.views.index'),
url(r'^themes/$', 'themes.views.index'),

url(r'^images/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),

url(r'^system/$','system.views.index'),
url(r'^system/create/$','system.views.create'),
url(r'^system/edit/(\d+)/$','system.views.edit'),
url(r'^system/delete/(\d+)/$','system.views.delete'),
url(r'^system/finish/$','system.views.finish'),
url(r'^system/edit/finish/$','system.views.editfinish'),
url(r'^system/delete/finish/$','system.views.deletefinish'),
url(r'^sys_not_created/$','system.views.sys_not_created'),
url(r'^system/sms_count/$','system.ajax.get_sms_count'),


url(r'^equipment/$','equipments.views.index'),
url(r'^equipment/permissions/(\d+)/$','equipments.views.permissions'),
url(r'^equipment/associations/(\d+)/$','equipments.views.associations'),
url(r'^equipment/finish/$','equipments.views.finish'),
url(r'^equipment/associations/finish/$','equipments.views.assoc_finish'),
url(r'^equipment/fieldnames/(\d+)/$','equipments.views.set_names'),

url(r'^rastreamento/veicular/$', 'rastreamento.views.index'),
url(r'^rastreamento/portatil/$', 'rastreamento.views.index'),
url(r'^rastreamento/loadData/$', 'rastreamento.views.loadData'),
url(r'^rastreamento/xhrtest/$', 'rastreamento.views.xhr_test'),



url(r'^accounts/create/(\d+)/$', 'accounts.views.create_user'),
url(r'^accounts/create/finish/$', 'accounts.views.create_finish'),

url(r'^accounts/delete/(\d+)/$','accounts.views.delete'),
url(r'^accounts/ajax/delete/$','accounts.ajax.delete'),
url(r'^accounts/edit/(\d+)/$','accounts.views.edit'),
url(r'^accounts/edit/finish/$','accounts.views.edit_finish'),
url(r'^accounts/edit/finish_firstlogin/$','accounts.views.finish_firstlogin'),



url(r'^vehicles/$', 'vehicles.views.index'),
url(r'^vehicles/create/(\d+)/$','vehicles.views.create'),
url(r'^vehicles/create/finish/$','vehicles.views.create_finish'),
url(r'^vehicles/edit/(\d+)/$','vehicles.views.edit'),
url(r'^vehicles/edit/finish/$','vehicles.views.edit_finish'),
url(r'^vehicles/delete/(\d+)/$','vehicles.views.delete'),
url(r'^vehicles/delete/finish/$','vehicles.views.delete_finish'),
url(r'^vehicles/swap/(\d+)/$','vehicles.views.swap'),
url(r'^vehicles/swap/finish/$','vehicles.views.swap_finish'),
url(r'vehicles/edit_equip/(\d+)/$','vehicles.ajax.edit_equipment'),
url(r'vehicles/delete_equip/$','vehicles.ajax.delete_equipment'),

url(r'^commands/$', 'command.views.index'),
# url(r'^commands/test/$', 'command.views.test277'), # used to test MaxTrack MTC 400 State
url(r'^commands/test/$', 'command.views.test278'), # used to test Quanta Tetrus State
url(r'^commands/create/(\d+)/$','command.views.create'),
url(r'^commands/load/$','command.ajax.load'),
url(r'^commands/check/$','command.ajax.check'),
url(r'^commands/create/(\d+)/(\d+)/$','command.views.create'),
url(r'^commands/create/finish/$','command.views.create_finish'),
url(r'^commands/delete/(\d+)/$','command.views.delete'),
url(r'^commands/delete/finish/$','command.views.delete_finish'),
url(r'^commands/loadavailable/$','command.views.loadavailable'),

url(r'^drivers/$', 'drivers.views.index'),
url(r'^drivers/create/$','drivers.views.create'),
url(r'^drivers/create/finish/$','drivers.views.create_finish'),
url(r'^drivers/edit/(\d+)/$','drivers.views.edit'),
url(r'^drivers/edit/finish/$','drivers.views.edit_finish'),
url(r'^drivers/delete/(\d+)/$','drivers.views.delete'),
url(r'^drivers/delete/finish/$','drivers.views.delete_finish'),
url(r'^drivers/profile/(\d+)/$','drivers.views.profile'),

url(r'^alerts/$', 'alerts.views.index'),
url(r'^alerts/create/(\d+)/$','alerts.views.create'),
url(r'^alerts/create/finish/$','alerts.views.create_finish'),
url(r'^alerts/edit/(\d+)/$','alerts.views.edit'),
url(r'^alerts/edit/finish/$','alerts.views.edit_finish'),
url(r'^alerts/delete/(\d+)/$','alerts.views.delete'),
url(r'^alerts/delete/finish/$','alerts.views.delete_finish'),
url(r'^alerts/status/$','alerts.ajax.status'),
url(r'^alerts/load/$','alerts.ajax.load'),

url(r'^geofence/$','geofence.views.index'),
url(r'^geofence/create/$','geofence.views.create'),
url(r'^geofence/create2/(\d+)/(\d+)/$','geofence.views.create2'),
#url(r'^geofence/create/$','geofence.views.create'),
url(r'^geofence/create/finish/$','geofence.views.create_finish'),
url(r'^geofence/geocode/$','geofence.ajax.geocoder'),
url(r'^geofence/route/$','geofence.ajax.route_calculator'),
url(r'^geofence/save/$','geofence.views.saveGeofencev2'),
url(r'^geofence/load/$','geofence.views.loadGeofences'),
url(r'^geofence/edit/(\d+)/$','geofence.views.edit'),
url(r'^geofence/edit2/(\d+)/(\d+)/(\d+)/$','geofence.views.edit2'),
url(r'^geofence/edit/finish/$','geofence.views.edit_finish'),
url(r'^geofence/delete/(\d+)/$','geofence.views.delete'),
url(r'^geofence/delete/finish/$','geofence.views.delete_finish'),

url(r'^paths/$','paths.views.index'),
url(r'^paths/load/$','paths.ajax.load'),

url(r'maplink/$','main.views.multispectral'),
url(r'openlayers/$','main.views.openlayers'),

url(r'reports/(\d+)/$','reports.views.report'),
url(r'^reports/checkready','reports.views.checkready'),


(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),


)

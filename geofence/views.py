# -*- coding:utf8 -*-
from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from itrack.geofence.models import Geofence
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos.linestring import LineString
from django.contrib.gis.geos import Polygon,MultiPolygon,MultiPoint
from querystring_parser import parser
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.gis import geos
from itrack.system.tools import findChild
from django.template.context import RequestContext
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str

def systemGeofenceDetails(sysid):
    lines = []
    system = System.objects.get(pk=sysid)
    geofences = Geofence.objects.filter(system=system)
    if system.parent == None:
        childof = None
    else:
        childof = system.parent.id
    lines.append({  'id':system.id,
                    'childof':childof,
                    'sysname':system.name,
                    'sysid':system.id
                })
    for geofence in geofences:
        
        if geofence.type == 'C':
            type = 'Círculo'
        elif geofence.type == 'P':
            type = 'Polígono'
        elif geofence.type == 'R':
            type = 'Rota'
        
        lines.append({  'id':geofence.id,
                        'childof':system.id,
                        'geofence':geofence.name,
                        'type':type,
                    })
    
    if geofences: 
        print lines
        return lines    
    else: 
        return []

def mountGeofenceTree(list_of_childs,parent):
    table = []
    
    if type(list_of_childs).__name__ == 'list':
        if(len(list_of_childs) > 0):
            prev = list_of_childs[0]
            if type(prev).__name__ != 'list':
                lines = systemGeofenceDetails(prev)
                for line in lines:
                    table.append(line)
            else:
                pass
                
            for el in list_of_childs[1:]:
                
                if type(el).__name__ == 'list':
                    lines = mountGeofenceTree(el,prev)
                else:
                    lines = mountGeofenceTree(el,parent)
                
                for line in lines:
                    table.append(line)
                    
                prev = el
    
        return table
           
    else:
        return systemGeofenceDetails(list_of_childs)
    

def index(request):
    system_id = request.session['system']
        
    childs = findChild(system_id)
    geofence_tree = mountGeofenceTree([system_id,childs],system_id)
    
    return render_to_response("geofence/templates/index.html",locals())

def create(request):
    system = System.objects.filter(administrator__username=request.user.username)
    
    g = False
    step = 1

    return render_to_response("geofence/templates/create.html",locals())

def create2(request,offset,offset2):
    system = System.objects.filter(administrator__username=request.user.username)
    
    g = False
    step = 2

    return render_to_response("geofence/templates/create.html",locals())

def saveGeofencev2(request):
  
  if request.method == "POST":
    parsed_dict = parser.parse(request.POST.urlencode())
    
    parsed_dict['name'] = smart_str(parsed_dict['name'], encoding='utf-8', strings_only=False, errors='strict')
    
    if parsed_dict['type'] == 'circle':
      
      system = System.objects.get(pk=request.session['system'])
      wkt = (parsed_dict['coords'])
          
      p = wkt
            
      if (parsed_dict['id'] != ""):
          g = Geofence.objects.get(pk=parsed_dict['id'])
          g.name = parsed_dict['name']
          g.type = 'C'
          g.polygon = p
          g.save()
          
          return HttpResponse('edit_finish')
                                      
      else:
          g = Geofence(name=parsed_dict['name'],system=system,type='C',polygon=p)
          g.save()    
          
          return HttpResponse('create_finish')
          
      return HttpResponse('fail')
      
    if parsed_dict['type'] == 'polygon':

      system = System.objects.get(pk=request.session['system'])
      wkt = (parsed_dict['coords'])

      if (parsed_dict['id'] != ""):
          g = Geofence.objects.get(pk=parsed_dict['id'])
          g.name = parsed_dict['name']
          g.type = 'P'
          g.polygon = wkt
          g.save()
          
          return HttpResponse('edit_finish')
                                      
      else:
          p = wkt
          print p
          g = Geofence(name=parsed_dict['name'],system=system,type='P',polygon=p)
          g.save()
          
          return HttpResponse("create_finish")

      return HttpResponse('fail')
    
    if parsed_dict['type'] == 'route':

      system = System.objects.get(pk=request.session['system'])
      wkt = (parsed_dict['coords'])

      if (parsed_dict['id'] != ""):
          g = Geofence.objects.get(pk=parsed_dict['id'])
          g.name = parsed_dict['name']
          g.type = 'R'
          g.polygon = wkt
          g.save()
          
          return HttpResponse('edit_finish')
          
      else:
          p = wkt
          t =  parsed_dict['tolerance']
          g = Geofence(name=parsed_dict['name'],system=system,type='R',linestring=p,tolerance=t)
          g.save()
          
          return HttpResponse("create_finish")
    
      
    else:
      pass
      
  else:
    pass

def create_finish(request):
  return render_to_response("geofence/templates/create_finish.html",locals())
  
def edit_finish(request):
  return render_to_response("geofence/templates/edit_finish.html",locals())
   
def loadGeofences(request):
  system = request.session["system"]
  geofence = Geofence.objects.filter(system=system)
  
  data = []
  
  for g in geofence:
    if g.type != 'R':
      data.append({"name":g.name,"id":g.id,"type":g.type,"polygon":str(g.polygon)})
    elif g.type == 'R':
      data.append({"name":g.name,"id":g.id,"type":g.type,"route":str(g.linestring)})
    
  print data
  json = simplejson.dumps(data)
  
  return HttpResponse(json, mimetype='application/json')
  
def delete(request,offset):
  g = Geofence.objects.get(pk=int(offset))
  if request.method == 'POST':
    
    g.delete()
    
    return HttpResponseRedirect("/geofence/delete/finish")
    
  else:
      return render_to_response("geofence/templates/delete.html",locals(),context_instance=RequestContext(request))

  
def delete_finish(request):
    return render_to_response("geofence/templates/delete_finish.html",locals())

def edit(request,offset):
    try:         
            g = Geofence.objects.get(pk=int(offset))
            
            step = 1
            
            type = g.type
                
            return render_to_response("geofence/templates/create.html",locals(),context_instance=RequestContext(request))
                    
#                form = DriverForm(instance=d)
                
#            if form.is_valid():
#                driver = form.save(commit = False)
#                system = System.objects.get(pk=request.session['system'])
#                driver.system = system
#                driver.save()
#                
#                vehicles = form.cleaned_data['vehicle']
#                for v in vehicles:
#                    driver.vehicle.add(v)
#                driver.save()
#                return HttpResponseRedirect("/drivers/edit/finish")
    
        # else:
            # ret urn HttpResponseForbidden(u"O seu sistema não pode editar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("A cerca eletrônica solicitado não existe.") 

def edit2(request,offset,offset2,g):
         
    step = 2
    
    a = g
    g={}
    g['id'] = a 
            
    return render_to_response("geofence/templates/create.html",locals(),context_instance=RequestContext(request))

    

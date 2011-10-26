var route;
var points;
var mapa;
//TODO: make the line more thin or fat
//TODO: make the option for the user remove a address field
//TODO: make the map visible only when the submit is submited and for paths too
//TODO: make the name and area fields visible when the above is done
$(document).ready(function(){

	loadmap();
	mapa = new MMap2(document.getElementById('map2'));
	
	$("#addpointroute").click(function(){
    var i = $("input[id^=routeinput]").size() + 1;
    
    var content =  ($("#routeinputs ol li").html());
    
    $("<li>"+content+"</li>").appendTo('#routeinputs ol');
    i++;
  });
  
  $("#step1route").submit(function(){
  	
  	openloading();
  	  	
  	vlayer3.destroyFeatures();
  	routeaddresses = [];
  	routepoints = [];
  	var wait = 1;
  	
  	tolerance = $("#routetolerance").val();
  	
	if(tolerance == '') {
		jQuery("#generaldialog").html("");
		jQuery("#generaldialog").attr("title", "Faltando campo Tolerância");
		$("#generaldialog").append("Por favor preencha o campo tolerância");
		jQuery("#generaldialog").dialog({
			show : "blind",
			modal : true
		});
	}

	else {
	  	//For each address do the Geocode, get the coordinates and mount an array
	  	$("#routeinputs ol li").each(function(){
	    	
	    	address =  $(".routeinput", this).val();
	    	number =  $(".routenumber", this).val();
	    	city =  $(".routecity", this).val();
	    	state =  $(".routestate", this).val();
	    		    	    	
	    	if(address != '' && number != '' && city != '' && state != '') {

	 			data = {};
	 			data['address'] = address;
	 			data['number'] = number;
	 			data['city'] = city;
	 			data['state'] = state;
	 			
	 			routeaddresses.push(data);	
	 		} else {
		  		jQuery("#generaldialog").html("");
	        	jQuery("#generaldialog").attr("title","Endereço(s) incorreto(s)");
	        	$("#generaldialog").append("Por favor preencha todos os campos para cada endereço.");
	        	jQuery("#generaldialog").dialog({show: "blind",modal:true});
		  	}
	    	
	  	});
	  	
	  	//TODO: validate the addresses
	  	if (routeaddresses[0]) {
	  		//Post only one time an array of addresses
	  		
	  		//Commented the part below because Maplink isn't helping me
			$.post("/geofence/geocode/", {
				addresses : routeaddresses
			}, function(data) {
				
				points = data;
				
				// alert(points.toSource());
				
				// $.post("/geofence/route/", {
					// points : points,
					// tolerance:tolerance
				// }, function(data) {
					//Now we're in a presence of an kludge-oriented programming
					
					var rd = new MRouteDetails();
			        rd.optimizeRoute = false;
			        rd.routeType = 0;                       /*by car */
			        var ve = new MVehicle();
			        ve.tankCapacity = 64;                   /*capacidade do tanque */
			        ve.averageConsumption = 10;             /*média de consumo em litros */
			        ve.fuelPrice = 2.15;                    /*preço do litro do combustível */
			        ve.averageSpeed = 70;                   /*velocidade média */
			        ve.tollFeeCat = 2;                      /*Categoria de pedágio: automóvel */
			 
			        /* define a base para gerar a rota */
			        var ro = new MRouteOptions();
			        ro.language = "portugues";
			        ro.vehicle = ve;
			        ro.routeDetails = rd;
								
					var rs = [];
					var rp = [];
					//We have to adapt the points of the route to this new kludge
					$.each(points, function(key, value) {
						var r = new MRouteStop();
						var point = new MPoint();
						point.x = parseFloat(value['lng']);
						point.y = parseFloat(value['lat']);
						r.description = "Endereço "+key;
						r.point = point;
						rs.push(r);
						
						routePointAux = new MRoutePoint();
						routePointAux.routeStop = r;
						rp.push(routePointAux);
					});
					//alert(rp.toSource());
					//Thank god I think it's over. Now we're gonna finally calculate the route.
					
					rm = new MRouteMannager(mapa);
					
					
					//rc1 = new MRouteControl(mapa, rs, ro, "#FF5555", function(result) {
					rm.createRoute(rp, ro, null, function(result){
						setTimeout("drawRoute()",3000);
					});

	
				// },'json');
				
			}, 'json');
		
		}

	}
  	
  	closeloading(4000);
  	
  	return false;
  });
  
  jQuery("#routesave").click(function(){
  	var id="";
  	tolerance = $("#routetolerance").val();
  	
  	if(g) {
  		id = g['id'];
  	}  
    
   geofencename = $("#circlename").val();
    if(!geofencename) { 
      	jQuery("#generaldialog").html("");
	    jQuery("#generaldialog").attr("title", "Faltando campo");
		$("#generaldialog").append("Por favor digite um nome para a cerca eletrônica.");
		jQuery("#generaldialog").dialog({
			show : "blind",
			modal : true
		});
    }
    else if(!route) { 
      	jQuery("#generaldialog").html("");
		jQuery("#generaldialog").attr("title", "Faltando cerca eletrônica");
		$("#generaldialog").append("Por favor selecione uma cerca eletrônica.");
		jQuery("#generaldialog").dialog({
			show : "blind",
			modal : true
		});
    }
    else if (!tolerance){
    	jQuery("#generaldialog").html("");
		jQuery("#generaldialog").attr("title", "Faltando campo Tolerância");
		$("#generaldialog").append("Por favor digite uma tolerância.");
		jQuery("#generaldialog").dialog({
			show : "blind",
			modal : true
		});
    }
    else {
      // Save geofence
      
      $.post(
        "/geofence/save/",
        {name:geofencename,type:'route', coords: route,id:id,tolerance:tolerance},
        function (data) {
          if (data == 'create_finish') {
            location.href = "/geofence/create/finish";
          }
          else if (data == 'edit_finish') {
            location.href = "/geofence/edit/finish";
          }
          else {
            alert ('Erro na criação de cerca eletrônica.')
          }
          
        }
      );
      
    }
  
  });
    
});

var vlayer3;
var temp;
function loadmap(){
	
  var options = {
  	units: 'm'
  };
	
  multispectral1 = new OpenLayers.Map('map1',options);
  
  var dm_wms1 = load_wms();

  //TODO: add support to editables routes

	vlayer3 = new OpenLayers.Layer.Vector("Editable", {
		onFeatureInsert : function(feature) {
			if (offset == 1) {
				if (temp)
					vlayer3.destroyFeatures(temp);
				temp = feature;
				var geometry = feature.geometry.clone();
				geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
				circle = (geometry.toString());
				area = (feature.geometry.getArea() / 1000).toFixed(3);
				jQuery("#circlearea").html(area + " km²");
			}
			
			if (offset == 2) {
				if (temp)
					vlayer3.destroyFeatures(temp);
				temp = feature;
				var geometry = feature.geometry.clone();
				geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
				polygon = (geometry.toString());
				area = (feature.geometry.getArea() / 1000).toFixed(3);
				jQuery("#circlearea").html(area + " km²");
			}
			
			if (offset == 3) {
				if (temp)
					vlayer3.destroyFeatures(temp);
				temp = feature;	
				var geometry = feature.geometry.clone();
				geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
				route = (geometry.toString());
				area = (feature.geometry.getLength() / 1000).toFixed(3);
				jQuery("#circlearea").html(area + " km");
			}
		}

	});

  
  if(offset ==  2) {
  	  vlayer3.events.on({"afterfeaturemodified": function(feature){
	        temp = feature;
			var geometry = feature.geometry.clone();
			geometry.transform(multispectral1.getProjectionObject(), new OpenLayers.Projection("EPSG:4326"));
			polygon = (geometry.toString());
			area = (feature.geometry.getArea() / 1000).toFixed(3);
			jQuery("#circlearea").html(area + " km²");
	  }});
  }

  markers = new OpenLayers.Layer.Markers( "Markers" );


  multispectral1.addLayer(dm_wms1);
  
  multispectral1.addLayer(vlayer3);
  
  multispectral1.addLayer(markers);
  
  multispectral1.setCenter(new OpenLayers.LonLat(-49.47,-16.40).transform(
        new OpenLayers.Projection("EPSG:4326"),
        multispectral1.getProjectionObject()
    ), 4);
  
  // multispectral1.setCenter(new OpenLayers.LonLat(-49.47,-16.40),0); 
  
  //Control Panel
  if (offset2 == 1 && offset == 1) {
	  //Control Panel
	  panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
	  var nav = new OpenLayers.Control.Navigation();
	  polyOptions = {sides: 40};
	  draw_ctl = new OpenLayers.Control.DrawFeature(vlayer3, OpenLayers.Handler.RegularPolygon, {'displayClass': 'olControlDrawFeaturePolygon',handlerOptions: polyOptions});
	  controls = [nav, draw_ctl];
	  panel.addControls(controls);
	  multispectral1.addControl(panel);
  }
  else if (offset == 2 && offset == 2) {
   panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
   var nav = new OpenLayers.Control.Navigation();
   draw_ctl = new OpenLayers.Control.DrawFeature(vlayer3, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'});
   var mod = new OpenLayers.Control.ModifyFeature(vlayer3, {'displayClass': 'olControlModifyFeature'});
   controls = [nav, draw_ctl,mod];
   panel.addControls(controls);
   multispectral1.addControl(panel);
   multispectral1.addControl(new OpenLayers.Control.MousePosition());
  }
  else {
  	panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
  	var nav = new OpenLayers.Control.Navigation();
  	controls = [nav]
  	panel.addControls(controls);
	multispectral1.addControl(panel);
	multispectral1.addControl(new OpenLayers.Control.MousePosition());
  }  
 
	
}


function drawRoute() {

	var poly = new MPolyline(rm.routeControl.routeCoords.points, "#003355", 3, .5);
        mapa.addOverlay(poly);

	var data = [];
	var p = {};

	var i = 0;
	$.each(rm.routeControl.routeCoords.points, function(key, value) {
		p = new Object;
		p['lng'] = value['x'];
		p['lat'] = value['y'];
		data.push(p);

	});
	multiline = [];
	test = [];
	markers.clearMarkers();
	for(var i in data) {
		var pnt = new OpenLayers.Geometry.Point(data[i]['lng'], data[i]['lat']);
		test.push(pnt);
		pnt2 = pnt.transform(new OpenLayers.Projection("EPSG:4326"), multispectral1.getProjectionObject());
		multiline.push(pnt2);

	}

	for(var i in points) {
		j = parseInt(i) + parseInt(1);
		var c = new OpenLayers.LonLat(points[i]["lng"], points[i]["lat"]);
		var ct = c.transform(new OpenLayers.Projection("EPSG:4326"), multispectral1.getProjectionObject());

		var size = new OpenLayers.Size(21, 25);
		var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
		var icon = new OpenLayers.Icon('/media/img/marker-blue-' + j + '.png', size, offset);
		marker = new OpenLayers.Marker(ct, icon.clone())
		markers.addMarker(marker, icon.clone());
	}
	testline = new OpenLayers.Geometry.LineString(test);
	test = new OpenLayers.Feature.Vector(testline, null);
	wkt = new OpenLayers.Format.WKT();

	// alert(wkt.write(test));

	multiline2 = new OpenLayers.Geometry.LineString(multiline);
	// alert(multiline2.getVertices());

	var style_green = {
		strokeColor : "#00FF00",
		strokeOpacity : 0.7,
		strokeWidth : 6,
		pointRadius : 6,
		pointerEvents : "visiblePainted"
	};
	polygonFeature = new OpenLayers.Feature.Vector(multiline2, null, style_green);

	vlayer3.addFeatures([polygonFeature]);
	multispectral1.zoomToExtent(markers.getDataExtent(), 1);
}

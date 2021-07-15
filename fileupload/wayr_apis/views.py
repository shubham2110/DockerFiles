from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TripSerializer, UserSerializer , VendorSerializer
from .models import *
from rest_framework import generics
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import datetime
User = Vendors

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .serializers import FileSerializer
from . import helper
getitem = helper.getitem
getjson = helper.getjson


from django.core import serializers

def obj_to_dict(model_instance):
    serial_obj = serializers.serialize('json', [model_instance])
    obj_as_dict = json.loads(serial_obj)[0]['fields']
    obj_as_dict['pk'] = model_instance.pk
    return obj_as_dict
#from django.contrib.auth.models import User


try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

try:
    from html import unescape  # python 3.4+
except ImportError:
    try:
        from html.parser import HTMLParser  # python 3.x (<3.4)
    except ImportError:
        from HTMLParser import HTMLParser  # python 2.x
    unescape = HTMLParser().unescape


api_urls = {
            'apiList' : '/apiList/',
            'Trip List' : '/tripList/',
            'Trip Detail' : '/tripDetail/<str:pk>',
            'Add Trip' : '/createTrip/',
            'Update Trip' : '/updateTrip/<str:pk>',
            'Delete Trip' : '/deleteTrip/<str:pk>',
}

def getsessionuser(request):
    if 'sessionid1' in request.COOKIES.keys():
        user = validatesession(request.COOKIES['sessionid1'])
        if user:
            return user
        else:
            return None
            
def validatesession(sessionid):
    try: 
        sessionid = Sessions.objects.get(key= sessionid)
    except ObjectDoesNotExist:
        sessionid=None
    if sessionid:
        try:
            v=Vendors.objects.get(mobile=sessionid.username)
        except ObjectDoesNotExist:
            v=None
        return v
        


##################################################################
#         ACTUAL VIEWS
##############################################################


class apiList(APIView):
    def get(self, request):
        return Response(api_urls)

@csrf_exempt
@api_view(['POST'])
def bookRide(request):
    return


class booktrip(APIView):
    def post(self,request):
        user=getsessionuser(request)
        if not user:
            return Response({"api": "booktrip", "status" : "false", "info" : "no user session found"})
        values=getjson(request)
        #print("Json values:", values)
        tripID = getitem(values,"tripID")
        driver = getitem(values,"driver")
        vehicle = getitem(values,"vehicle")
        vendor  = user.mobile
        
        #print("Input values:", tripID, driver, vehicle, vendor)

        try:
            TRIP=Trips.objects.get(tripID =tripID)
            DRIVER=Drivers.objects.get(licenseno = driver)
            VEHICLE=Vehicles.objects.get(rcnumber=vehicle)
            #print("Input values:", tripID, driver, vehicle, vendor)
            if (not TRIP.isBooked) and DRIVER.isActive and VEHICLE.isActive:
                data={"tripID" : tripID , "isBooked" : True , "driver" : driver , "vehicle" : vehicle }
                TRIP.isBooked = True
                TRIP.driver = driver
                TRIP.vehicle = vehicle
                TRIP.vendor = vendor
                TRIP.save()
                trip=Trips.objects.get(tripID=tripID )
                serializer= TripSerializer(trip)
                return Response({"api": "booktrip", "status" : "true", "info" : serializer.data })
            elif TRIP.isBooked and TRIP.driver == driver and TRIP.vehicle == vehicle and TRIP.vendor == vendor:
                trip=Trips.objects.get(tripID=tripID )
                serializer= TripSerializer(trip)
                return Response({"api": "booktrip", "status" : "true", "info" : serializer.data })
            else:
                return Response({"api": "booktrip", "status" : "false", "info" : "Either Driver or Vehicle is not activated Yet." })
                
        except (ObjectDoesNotExist , Exception) as e:
            return Response({"api": "booktrip", "status" : "false", "info" : str(e)})
    
@csrf_exempt
@api_view(['GET','POST'])
def tripList(request):
    user=getsessionuser(request)
    if not user:
        return Response({"api": "triplist", "status" : "false", "info" : "no user session found"})
    hours=12
    trips=[]
    filters={}
    print("Going to get json")
    f=getjson(request)
    filters={}
    items=["tripID","clientName","clientContact","clientSource","clientDestination","clientPrice","cartype","carModel","driver","vehicle","vendor","datetime","datetime__gte","datetime__lte","isBooked","isActive","isDeleted"]
    for each in f.keys():
        if each not in items:
            pass
        else:
            filters[each]=f[each]
    
    if user.is_staff and not ( "datetime__gte" in filters.keys() or  "datetime__lte" in filters.keys()):
        hours=12
        thetime= datetime.datetime.now() - datetime.timedelta(hours = hours)
        today=thetime.strftime("%Y%m%d%H%M")
        filters["datetime__gte"] = today  
    else:
        if "datetime__gte" in filters.keys() or "datetime__lte" in filters.keys():
            pass
        else:
            hours=4
            thetime= datetime.datetime.now() - datetime.timedelta(hours = hours)
            today=thetime.strftime("%Y%m%d%H%M")
            filters["datetime__gte"] = today
        filters["isActive"] = True   
    trips=Trips.objects.filter(**filters )
    serializer= TripSerializer(trips, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET','POST'])
def myTripList(request):
    user=getsessionuser(request)
    if not user:
        return Response({"api": "triplist", "status" : "false", "info" : "no user session found"})
    trips=[]
    filters={}
    f=getjson(request)
    filters={}
    items=["tripID","clientName","clientContact","clientSource","clientDestination","clientPrice","cartype","carModel","driver","vehicle","vendor","datetime","isBooked","isActive","isDeleted"]
    for each in f.keys():
        if each not in items:
            pass
        else:
            filters[each]=f[each]
    
    filters["isBooked"] = True   
    filters["vendor"] = user.mobile
    try:
        trips=Trips.objects.filter(**filters )
        serializer= TripSerializer(trips, many=True)
        return Response(serializer.data)
    except:
        return Response({"api": "triplist", "status" : "false", "info" : "no trips found"})



@csrf_exempt
@api_view(['POST'])
def createtrip(request):
    user = getsessionuser(request)
    if (not user) or not user.is_staff:
        return Response({"api": "createtrip","status": "false", "info": "no permission"})
    #json=getjson(request)
    #print(request.data)
    serializer = TripSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"api": "createtrip","status": "false", "info": "Data not valid"})
    return Response({"api": "createtrip", "status": "true", "info": serializer.data})



class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
def FileGetView(request, pk):
    file=pk
    filename=""
    def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    if RepresentsInt(file):
        try: 
            f=File.objects.get(id=int(file))
            filename=str(f.file)
        except ObjectDoesNotExist :
            filename=file
    else:
        filename=file
    
    return HttpResponseRedirect('/mediafiles/'+filename)






@csrf_exempt
@require_http_methods(["GET", "POST"])
def index(request):
    return HttpResponseRedirect('/mediafiles/index.html')
    content="<html><table>"
    for each in api_urls.keys():
        content+="<tr><td>"+escape(each)+"</td><td><a href="+escape(api_urls[each])+">"+escape(api_urls[each])+"</a></td></tr>"
    return  HttpResponse(content)

# @csrf_exempt
# @require_http_methods(["GET"])
# def getCities(request):
    # content={"cities": ["Agra","Delhi","Mumbai","Kolkata"]}
    # return  JsonResponse(content)


################################################################################
#@api_view(['POST'])
#def updateTrip(request, pk):
#	task = Trips.objects.get(tripID=pk)
#	serializer = TripSerializer(instance=task, data=request.data)
#	if serializer.is_valid():
#		serializer.save()
#	return Response(serializer.data)


#@api_view(['DELETE'])
#def deleteTrip(request, pk):
#	task = Trips.objects.get(tripID=pk)
#	task.delete()
#	return Response('Item succsesfully delete!')

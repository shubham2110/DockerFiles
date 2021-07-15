from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from .. import helper
from ..serializers import *
from rest_framework import generics
from django.contrib.auth import get_user_model
User = Vendors
import json
#from django.contrib.auth.models import User

getitem = helper.getitem

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

##########################
### APis List
#########################

class GetJson():
    def getjson(self,request):
        finaldict={}
        bodyhaskeys=False
        if request.body:
            try:
                json.loads(request.body)
                bodyhaskeys=True
            except: 
                print("Could not load Json from body: ", request.body)
        try:
            if bodyhaskeys:
                json1= json.loads(request.body)
                for each in json1.keys():
                    finaldict[each] = json1[each]
            if len(request.POST.keys()):
                for each in request.POST.keys():
                    finaldict[each] = request.POST[each]
            return finaldict
        except Exception as e:
            print("Error while Getting json: ", e)
        return finaldict

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

def checkuser(username):
    v=None
    try:
        v=Vendors.objects.get(mobile=username)
    except ObjectDoesNotExist:
        v=None
    return v  

class listDrivers(APIView): 
    def get(self, request):
        user=getsessionuser(request)
        jsondata=GetJson().getjson(request)
        if not user:
            return Response({"api":"listdrivers","status":"false","info":"No User session was found"})
        else:
            filters={}
            filters["owner"] = user.mobile
            drivers=Drivers.objects.filter(**filters )
            serializer= DriverSerializer(drivers, many=True)
            return Response(serializer.data)

class listAllDrivers(APIView): 
    def get(self, request):
        user=getsessionuser(request)
        jsondata=GetJson().getjson(request)
        if not user:
            return Response({"api":"listalldrivers","status":"false","info":"No User session was found"})
        elif user.is_staff :
            filters={}
            if("owner" in jsondata.keys()):
                filters["owner"] = jsondata["owner"]
            drivers=Drivers.objects.filter(**filters )
            serializer= DriverSerializer(drivers, many=True)
            return Response(serializer.data)
        else:
            return Response({"api":"listalldrivers","status":"false","info":"User is not staff"})

class listVehicles(APIView): 
    def get(self, request):
        user=getsessionuser(request)
        jsondata=GetJson().getjson(request)
        if not user:
            return Response({"api":"listvehicles","status":"false","info":"No User session was found"})
        else:
            filters={}
            filters["owner"] = user.mobile
            vehicles=Vehicles.objects.filter(**filters )
            serializer= VehicleSerializer(vehicles, many=True)
            return Response(serializer.data)

class listAllVehicles(APIView): 
    def get(self, request):
        user=getsessionuser(request)
        jsondata=GetJson().getjson(request)
        if not user:
            return Response({"api":"listallvehicles","status":"false","info":"No User session was found"})
        elif user.is_staff :
            filters={}
            if("owner" in jsondata.keys()):
                filters["owner"] = jsondata["owner"]
            vehicles=Vehicles.objects.filter(**filters )
            serializer= VehicleSerializer(vehicles, many=True)
            return Response(serializer.data)
        else:
            return Response({"api":"listallvehicles","status":"false","info":"User is not staff"})


@api_view(['POST'])
def deleteDriver(request):
    print("hello")
    user=getsessionuser(request)
    
    jsondata=GetJson().getjson(request)
    
    if not user:
        return Response({"api":"deletedriver","status":"false","info":"No User session was found"})
    
    ln = getitem(jsondata, "licenseno")
    if not ln:
        return Response({"api":"deletedriver","status":"false","info":"No Driver found or No licenseno privided"})
    try:
        driver = Drivers.objects.get(licenseno=ln)
        if user.is_staff or driver.owner == user.mobile:
            driver.delete()
        else:
            return Response({"api":"deletedriver","status":"true","info":"Driver already deleted."})
    except ObjectDoesNotExist:
        return Response({"api":"deletedriver","status":"true","info":"Driver already deleted."})
    return Response({"api":"deletedriver","status":"true","info":"Driver Deleted"})

@api_view(['POST'])
def deleteVehicle(request):
    user=getsessionuser(request)
    jsondata=GetJson().getjson(request)
    if not user:
        return Response({"api":"deletevehicle","status":"false","info":"No User session was found"})
    
    rc = getitem(jsondata, "rcnumber")
    if not rc:
        return Response({"api":"deletevehicle","status":"false","info":"No Car found or No RCnumber privided"})
    try:
        vehicle = Vehicles.objects.get(rcnumber=rc)
        vehicle.delete()
    except ObjectDoesNotExist:
        return Response({"api":"deletevehicle","status":"true","info":"Vehicle already deleted."})
    return Response({"api":"deletevehicle","status":"true","info":"vehicle Deleted"})



class addDriver(APIView): 
    def post(self, request):
        user=getsessionuser(request)
        jsondata=GetJson().getjson(request)
        if not user:
            return Response({"api":"adddriver","status":"false","info":"No User session was found"})
        else:
            try:
                licenseno   = getitem(jsondata,     "licenseno"                  )  
                owner       = getitem(jsondata,     "owner"                      )
                aadharno    = getitem(jsondata,     "aadharno"                   )
                licensefile = getitem(jsondata,     "licensefile"                )
                aadharfile  = getitem(jsondata,     "aadharfile"                 )
                name        = getitem(jsondata,     "name"                       )
                pancard     = getitem(jsondata,     "pancard"                    )
                nickname    = getitem(jsondata,     "nickname"                   )
                photourl    = getitem(jsondata,     "photourl"                   )
                number      = getitem(jsondata,     "number"                     )
                if ( user.is_staff ) and checkuser(owner):
                    pass
                else:
                    owner = user.mobile

                try:
                    driver=Drivers.objects.get(licenseno=licenseno)
                except ObjectDoesNotExist:
                    driver=Drivers()
                #driver= Drivers(
                if not licenseno:
                    return Response({"api":"adddriver","status":"false","info":"licenseno field is mendatory"})
                driver.licenseno   = licenseno  # ,
                if owner:
                    driver.owner       = owner      # ,
                if aadharno:
                    driver.aadharno    = aadharno   # ,
                if licensefile:
                    driver.licensefile = licensefile# ,
                if aadharfile:
                    driver.aadharfile  = aadharfile # ,
                if name:
                    driver.name        = name       # ,
                if pancard:
                    driver.pancard     = pancard    # ,
                if nickname:
                    driver.nickname    = nickname   # ,
                if photourl:
                    driver.photourl    = photourl   # ,
                if number:
                    driver.number      = number     # ,
                #)                
                if user.is_staff:
                    isActive=getitem(jsondata, "isActive")
                    if isActive.lower() == "true":
                        driver.isActive = True
                driver.save()
                return Response({"api":"adddriver","status":"true","info":"Driver updated."})
            except Exception as e:
                return Response({"api":"adddriver","status":"false","info":str(e)})


class addVehicle(APIView):
    def post(self, request):
        user=getsessionuser(request)
        jsondata=GetJson().getjson(request)
        types=["Hatchback","Sedan","SUV","MPV", "VAN"]
        if not user:
            return Response({"api":"addVehicle","status":"false","info":"No User session was found"})
        else:
            try:
                rcnumber    = getitem(jsondata,      "rcnumber"         )
                vtype       = getitem(jsondata,      "vtype"            )
                model       = getitem(jsondata,      "model"            )
                insuranceno = getitem(jsondata,      "insuranceno"      )
                permitno    = getitem(jsondata,      "permitno"         )
                permitdate  = getitem(jsondata,      "permitdate"       )
                insdate     = getitem(jsondata,      "insdate"          )
                nickname    = getitem(jsondata,      "nickname"         )
                photo       = getitem(jsondata,      "photo"            )
                nameofrc    = getitem(jsondata,      "nameofrc"         )
                owner       = getitem(jsondata,      "owner"            )
                
                if vtype and (vtype not in types):
                    return Response({"api":"addVehicle","status":"false","info":"Please enter valid vehicle types, ", "vehicles": ["Hatchback","Sedan","SUV","MPV", "VAN"] })            
                if ( user.is_staff ) and checkuser(owner):
                    pass
                else:
                    owner = user.mobile
                if not rcnumber:
                    return Response({"api":"addVehicle","status":"false","info":"RC Number is mendatory field."})
                try:
                    vehicle = Vehicles.objects.get(rcnumber = rcnumber)
                except ObjectDoesNotExist:
                    vehicle=Vehicles()
                
                #vehicle= Vehicles(
                vehicle.rcnumber    = rcnumber    #,
                if vtype:
                    vehicle.vtype       = vtype       #,
                if model:
                    vehicle.model       = model       #,
                if insuranceno:
                    vehicle.insuranceno = insuranceno #,
                if permitno:
                    vehicle.permitno    = permitno    #,
                if permitdate:
                    vehicle.permitdate  = permitdate  #,
                if insdate:
                    vehicle.insdate     = insdate     #,
                if nickname:
                    vehicle.nickname    = nickname    #,
                if photo:
                    vehicle.photo       = photo       #,
                if nameofrc:
                    vehicle.nameofrc    = nameofrc    #,
                if owner:
                    vehicle.owner       =  owner     #
                #)
                if user.is_staff:
                    isActive=getitem(jsondata, "isActive")
                    if isActive.lower() == "true":
                        vehicle.isActive = True
                vehicle.save()
                return Response({"api":"addvehicle","status":"true","info":"Vehicle updated."})
            except Exception as e:
                return Response({"api":"addvehicle","status":"false","info":str(e)})


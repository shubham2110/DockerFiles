from django.core.exceptions import ObjectDoesNotExist
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
from django.contrib.auth import get_user_model
from .otpview import sendotp
User = Vendors
from . import helper
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
    
        if bodyhaskeys:
            json1= json.loads(request.body)
            for each in json1.keys():
                finaldict[each] = json1[each]
        if len(request.POST.keys()):
            for each in request.POST.keys():
                finaldict[each] = request.POST[each]
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


#Authentication Functions

class setprofile(APIView):
    def post(self, request):
        user=getsessionuser(request)
        if not user:
            return Response({"api":"setprofile","status":"false","info":"No User session was found"})
        jsondata=GetJson().getjson(request)
        useritems=["name", "email", "password", "address", "pan", "panfile"]
        staffitems=["is_active","is_staff", "role"]
        cuser="sasadagfdyagdjgajdgajhgdjaghdja"
        if "mobile" in jsondata.keys():
            cuser=jsondata["mobile"]
        if user.is_staff and checkuser(cuser):
            mobile=cuser
        else:
            mobile=  user.mobile
        
        v=checkuser(mobile)
        if not v:
            return Response({"api":"setprofile","status":"false","info":"No User session was found"})
        
        for each in jsondata.keys():
            if each in useritems:
                setattr(v,each,jsondata[each])
            elif each in staffitems:
                if not user.is_staff:
                    continue
                else:
                    setattr(v, each,jsondata[each])
        v.save()
        
        return Response({"api":"setprofile","status":"true","info":"user updated."})    

class getprofile(APIView):
    def post(self, request):
        user=getsessionuser(request)
        if not user:
            return Response({"api":"setprofile","status":"false","info":"No User session was found"})
        jsondata=GetJson().getjson(request)
        cuser="sasadagfdyagdjgajdgajhgdjaghdja"
        if "mobile" in jsondata.keys():
            cuser=jsondata["mobile"]
        if user.is_staff and checkuser(cuser):
            mobile=cuser
        else:
            mobile=  user.mobile
        vendor=Vendors.objects.get(mobile=mobile )
        serializer= VendorSerializer(vendor)
        return Response(serializer.data)         

class logout(APIView):
    def post(self, request):
        if 'sessionid1' not in request.COOKIES.keys():
            return Response({"api":"logout", "success": "true"})
        try: 
            sessionid = Sessions.objects.get(key= request.COOKIES['sessionid1'])
        except ObjectDoesNotExist:
            sessionid=None
        if sessionid:
            try:
                wl = Sessions.objects.filter( key=request.COOKIES['sessionid1']  )#username= sessionid.username)
                wl.delete()
            except ObjectDoesNotExist:
                pass
        return Response({"api":"logout", "success": "true"})
        

class login(APIView):
  
    def getsessionuser(self, request):
        if 'sessionid1' in request.COOKIES.keys():
            user = self.validatesession(request.COOKIES['sessionid1'])
            if user:
                return user
            else:
                return None

    def successLogin(self, user, request):
        response =  Response({"api": "login", "success": "true"})
        response.set_cookie('sessionid1', self.generateSession(user, request))
        return response

    def generateSession(self,user, request):
        user1=None
        if 'sessionid1' in request.COOKIES.keys():
            user1 = self.validatesession(request.COOKIES['sessionid1'])
        if user1:
            return request.COOKIES['sessionid1']
        else:
            print("Setting new cookie")
        import uuid
        sessionid = str(uuid.uuid4())
        so = Sessions()
        so.key=sessionid
        so.username= user.mobile
        so.save()
        return sessionid

    def error(self, message, request):
        res= Response({"error" : message } )
        user1=None
        if 'sessionid1' in request.COOKIES.keys():
            user1 = self.validatesession(request.COOKIES['sessionid1'])
        if user1:
            res.set_cookie('sessionid1', request.COOKIES['sessionid1'])
        else:
            print("Not setting cookie")
        return res
         


    def validatesession(self,sessionid):
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
    

    def post(self,request):
        jsondata=GetJson().getjson(request)
        max_age = 365 * 24 * 60 * 60
        import datetime
        expires = datetime.datetime.strftime(
            datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        if 'sessionid1' in request.COOKIES.keys():
            user = self.validatesession(request.COOKIES['sessionid1'])
            if user:
                print("Success due to valid session. Session ID:", request.COOKIES['sessionid1'])
                res=self.successLogin(user, request)
                return res
            else:
                print("Lets check the username and password provided")
        user=None
        password=None
        otp=None
        error_text=""
        if "username" in jsondata.keys():
            try:
                user= Vendors.objects.get(mobile=jsondata["username"])
            except ObjectDoesNotExist:
                user=None
                #Also check for Signup case
                if "otp" in jsondata.keys():
                    if sendotp().verifyotp(jsondata["username"],jsondata["otp"]):
                        user=Vendors(mobile=jsondata["username"])
                        user.save()
                        #user= Vendors.objects.get(mobile=jsondata["username"])
                        res=self.successLogin(user, request)
                        return res
        else:
            error_text+="Username not provided."
        if not user:
            res=self.error("User Not Found", request)
            return res

        if "password" in jsondata.keys():
            try:
                passwordx= Vendors.objects.get(mobile=user.mobile).password
            except ObjectDoesNotExist:
                passwordx=None
            if passwordx == jsondata["password"]:
                res=self.successLogin(user, request)
                return res
            else:
                error_text+="Password did not match."

        if "otp" in jsondata.keys():
            if sendotp().verifyotp(user.mobile,jsondata["otp"]):
                res=self.successLogin(user, request)
                return res
            else:
                error_text += " OTP did not match. "
        res=self.error(error_text, request)
        return res













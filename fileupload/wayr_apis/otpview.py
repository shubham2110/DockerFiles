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
User = Vendors
import json
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

#Authentication Functions



class sendotp(APIView):
    otplength=4

    def triggerotp(self, username, otp):
        import requests
        sessionkey="351290AmQLDe6R5ff73247P1"
        #x=requests.get("https://api.msg91.com/api/sendhttp.php?authkey="+sessionkey+"&mobiles="+username+"&country=91&message=Your OTP to login into Wayr is: "+otp+"&sender=dmdsms&route=4")
        return "sent-"+otp
        return x


    def generatenumber(self,x):
        return "1234"

    def generateotp(self, username):
        otp = self.generatenumber(self.otplength)
        otp=str(otp)
        import datetime
        time=str(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(minutes=5)))
        otp=otp+"_"+time
        try:
            alreadyotp = OTP.objects.get(username=username)
        except ObjectDoesNotExist:
            alreadyotp=None
        if not alreadyotp:
            newotp=OTP()
            newotp.username=username
            newotp.otp=str(otp)
            newotp.save()
        else:
            l=alreadyotp.otp.split(",")
            l.append(otp)
            alreadyotp.otp=",".join(l)
            alreadyotp.save()
        return otp[:self.otplength]

    def error(self, message):
        return Response({"log" : message})

    def post(self,request):
        jsondata=GetJson().getjson(request)
        if "username" not in jsondata.keys():
            return self.error("No User sent")
        
        username = jsondata["username"]
        otp= self.generateotp(username)
        x= self.triggerotp(username, otp)   
        return self.error(x)
    
    def verifyotp(self, username, otp):
        try:
            alreadyotp = OTP.objects.get(username=username)
        except ObjectDoesNotExist:
            alreadyotp=None
        if not alreadyotp:
            return False
        otps=alreadyotp.otp.split(",")
        newotps=[]
        verified=False
        print(otps)
        for each in otps:
            if not each:
                continue
            aotp=each[:self.otplength]
            time1=each[self.otplength+1:]
            import datetime
            time2=str(datetime.datetime.timestamp(datetime.datetime.now()))
            if float(time1) > float(time2):
                if str(aotp) ==  str(otp):
                    verified=True
                else:
                    newotps.append(each)
        if not newotps:
            alreadyotp.delete()
        else:
            alreadyotp.otp=",".join(newotps)
            alreadyotp.save()
        return verified
             
            

        

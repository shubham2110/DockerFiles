from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
#from .models import *
from rest_framework import generics
from django.contrib.auth import get_user_model
#from .otpview import sendotp
#User = Vendors
import json
import csv
import os.path
from fuzzywuzzy import fuzz
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

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



class getcities(APIView):
    def post(self, request):
        jsondata=GetJson().getjson(request)
        if "hint" in jsondata.keys():
            hint=jsondata['hint']
            f=open(PROJECT_ROOT+'/../static/cities.csv', 'r')
            lines = f.read().splitlines()
            header=lines[0].split(",")
            newlines=lines[1:]
            newlist=sorted(newlines, key=lambda x : fuzz.ratio(x.split(",")[0].lower(),hint.lower()), reverse=True)[:10]
            reader=[ x.split(",") for x in newlist]
            reader.insert(0,header)
        else:
            f=open(PROJECT_ROOT+'/../static/cities.csv', 'r')
            reader = csv.reader(f)
        lists=[]
        keys=[]
        for rows in reader:
            if not keys:
                keys=rows
            else:
                dict={ keys[i] : rows[i] for i in range(len(keys))  }
                lists.append(dict)
        print(lists)
        return Response(lists)













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

espace=escape
unescape=unescape
import json

def getitem(dict,key):
    if key in dict.keys():
        return dict[key]
    else:
        return ""

def getjson(request):
    finaldict={}
    bodyhaskeys=False
    if request.body:
        try:
            s=request.body
            json.loads(s)
            bodyhaskeys=True
        except Exception as e: 
            print("Could not load Json from body: ", request.body, e)

    if bodyhaskeys:
        json1= json.loads(request.body)
        for each in json1.keys():
            finaldict[each] = json1[each]
    if len(request.POST.keys()):
        for each in request.POST.keys():
            finaldict[each] = request.POST[each]
    return finaldict
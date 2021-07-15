from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
import datetime


def getDefaultRole():
    types=["vendor","admin","superadmin","user","driver"]
    return types[0]
def getDefaultCar():
    types=["Hatchback","Sedan","SUV","MPV", "VAN"]
    return types[0]
##

#from django.db import models
#from .models import File

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name

class Vendors(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(verbose_name='mobile',max_length=12,primary_key=True)
    name = models.CharField(max_length=255,default="",null=True)
    email = models.EmailField( verbose_name='email address', max_length=255, unique=False,blank=True,null=True)
    password = models.CharField(max_length=255,default="ThisIsRootPassword")
    role = models.CharField(max_length=255,default=getDefaultRole)
    address = models.CharField(max_length=255,default="")
    pan = models.CharField(max_length=255,default="")
    panfile = models.CharField(max_length=255,default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.mobile
    

####
class Trips(models.Model):
    tripID              =  models.AutoField(primary_key=True)
    clientName          = models.CharField(max_length=80)
    clientContact       = models.CharField(max_length=80)
    clientSource        = models.CharField(max_length=80)
    clientDestination   = models.CharField(max_length=80, blank=True, default="")
    clientPrice         = models.CharField(max_length=80, default="500")
    cartype             = models.CharField(max_length=20, default=getDefaultCar)
    carModel            = models.CharField(max_length=80, blank=True , default="")
    driver              = models.CharField(max_length=20, blank=True, default="")
    vehicle             = models.CharField(max_length=20, blank=True, default="")
    vendor              = models.CharField(max_length=12, default="", verbose_name='mobilenumber')
    datetime                = models.CharField(max_length=15, default=datetime.datetime.now().strftime("%Y%m%d%H%M"), verbose_name="trip date time")  
    isBooked            = models.BooleanField(default=False)
    isActive            = models.BooleanField(default=True)
    isDeleted           = models.BooleanField(default=False)
     
    def __str__(self):
        return self.tripID

class Sessions(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(verbose_name='mobilenumber', max_length=12)
    def __str__(self):
        return self.key

class OTP(models.Model):
    username = models.CharField(verbose_name='mobilenumber', max_length=12, primary_key=True)
    otp = models.CharField(max_length=255) 

class Drivers(models.Model):
    licenseno   =models.CharField(max_length=255, primary_key=True)
    owner       =models.CharField(max_length=12, verbose_name='mobilenumber')
    aadharno    =models.CharField(max_length=25, default="")
    licensefile =models.CharField(max_length=25, default="")
    aadharfile  =models.CharField(max_length=25, default="")
    name        =models.CharField(max_length=25, default="")
    pancard     =models.CharField(max_length=25, default="")
    nickname    =models.CharField(max_length=25, default="")
    photourl    =models.CharField(max_length=25, default="")
    number      =models.CharField(max_length=25, default="")
    isActive    =models.BooleanField(default=False)

class Vehicles(models.Model):
    rcnumber    = models.CharField(max_length=255, primary_key=True)
    vtype        = models.CharField(max_length=20, default=getDefaultCar)
    model       = models.CharField(max_length=40, default="") 
    insuranceno = models.CharField(max_length=40, default="") 
    permitno    = models.CharField(max_length=40, default="") 
    permitdate  = models.CharField(max_length=8, default="99991231", verbose_name="insurace date") 
    insdate     = models.CharField(max_length=40, default="", verbose_name="insurance date") 
    nickname    = models.CharField(max_length=40, default="") 
    photo       = models.CharField(max_length=40, default="") 
    nameofrc    = models.CharField(max_length=40, default="",verbose_name="nameofrc") 
    isActive    =models.BooleanField(default=False)
    owner       = models.CharField(max_length=12, verbose_name="mobilenumber") 



# API List

1.Login
=============

##### Request URL: [/login/](/login/)

##### Request Type: POST (application/json)

##### Request Data: 
```
{
	"username" : "9599239456",
	"password" : "1234",
	"otp" 	   : "1234",
}
```
##### Response Data: 
```
{
	"api" : "login",
	"status" : "true",
	"info" : "User <user> logged in."
}
```
---------------------------------------------

[========]


2.Logout
=============

##### Request URL: [/logout/](/logout/)

##### Request Type: POST (application/json)

##### Request Data: 
```
{

}
```
##### Response Data: 
```
{
	"api" : "logout",
	"status" : "true",
	"info" : "User <user> logged in."
}
```

-----------------------------------------------

[========]


3.Get City List
=============

##### Request URL: [/getcities/](/getcities/)

##### Request Type: POST (application/json)

##### Request Data: 
```
{
"hint" : "Agra"
}
```
##### Response Data: 
```
[
	{
		"City":"Agra",
		"State":"Uttar Pradesh",
		"District":"Agra"
	},
	{
		"City":"Ara",
		"State":"Jharkhand",
		"District":"Hazaribag"
	}
]
```

-----------------------------------------------

[========]


4.Send OTP
==========

##### Request URL: [/sendotp/](/sendotp/)

##### Request Type: POST (application/json)

##### Request Data: 

```json
{
	"username" : "9599239456"
}
```

##### Response Data: 
```
{
	"api" : "sendotp",
	"status" : "true",
	"info" : "sent-<otp>"
}
```

---------------------------------------------

[========]



5.Upload File
==========

##### Request URL: [/uploadfiles/](/uploadfiles/)

##### Request Type: POST (multipart/form-data)

##### Request Data: 

```
	"file" : "<filename>"
```

##### Response Data: 
```
{
    "id": 4<id of file>,
    "file": "/mediafiles/newphoto.jpg<URL of file>"
}
```


---------------------------------------------------------------

[========]



6.Get File
================
##### Request URL: [/getfile/<id or filename>](/getfile/<id_or_filename>)

##### Request Type: GET


##### Response Data: 
Actual File gets download as reponse. 

-------------------------------------------------------------------------------


[========]



7.Add Driver or Update Driver
=============

##### Request URL : [/adddriver/](/adddriver/)

##### Prerequisite: i) Valid Session

##### Request Type: POST

##### Request data: 

```json
{
    "licenseno" : "12345",  
	"owner" : ""     ,
	"aadharno" : ""  ,
	"licensefile" : "",
	"aadharfile"  : "",
	"name"   : ""    ,
	"pancard"  : ""  ,
	"nickname" : ""  ,
	"photourl"  : "" ,
	"number"   : ""  ,
    "isActive"  : "false" 
}
```

##### Response: 

```json
{
    "api": "adddriver",
    "status": "true",
    "info": "Driver updated."
}
```

----------------------------------------------------

[========]



8.Add Vehicle or Update Vehicle 
====================

##### Request URL : [/addvehicle/](/addvehicle/)

##### Prerequisite: i) Valid Session

##### Request Type: POST

##### Request data: 

```json
{
"rcnumber" : "HR26BN7992",    
"vtype"    : "Hatchback"    ,
"model"    : ""   ,
"insuranceno"  : "",
"permitno"    : "",
"permitdate"  : "" , 
"insdate"   : ""  ,
"nickname"  : "",  
"photo"       : "",
"nameofrc"  : "",  
"owner"     : ""  

}
```

##### Response: 

```json
{
    "api": "addvehicle",
    "status": "true",
    "info": "Vehicle updated."
}
```



----------------------------------------------------------


[========]



9.Add Trip
=======================


##### Request URL : [/createtrip/](/createtrip/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin

##### Request Type: POST

##### Request data: 

```json
 {        
 "clientName"		 : "Rahul"            ,
 "clientContact"     : "9599239456"       ,
 "clientSource"      : "Delhi"            ,
 "clientDestination" : "Mumbai"           ,
 "clientPrice"       : "1200"             ,
 "cartype"           : "SUV"        ,
 "carModel"          : ""                 ,
 "datetime"              : "202101151839"         ,
 "time"              : "17:43"           
}
```

##### Response: 

```json
{
    "api": "createtrip",
    "status": "true",
    "info": {
        "tripID": 3,
        "clientName": "Rahul",
        "clientContact": "9599239456",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "clientPrice": "1200",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151838",
        "isBooked": false,
        "isActive": true,
        "isDeleted": false
    }
}
```

-------------------------------------------


[========]


10.List Trips
=======================


##### Request URL : [/triplist/](/triplist/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST/GET

##### Request data: 

```json
{
}
```

In case you want to apply some filter on request. Send data in following format. Use any of below options. 

```json
 {        
        "tripID": 1,
        "clientName": "Rahul",
        "clientContact": "9699333232",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151815",    
}
```

##### Response: 

Response is list of all trips as per your filter. 

```json
[
    {
        "tripID": 1,
        "clientName": "Rahul",
        "clientContact": "9699333232",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "clientPrice": "1200",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151815",
        "isBooked": false,
        "isActive": true,
        "isDeleted": false
    },
    {
        "tripID": 2,
        "clientName": "Rahul",
        "clientContact": "9699333232",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "clientPrice": "1200",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151815",
        "isBooked": false,
        "isActive": true,
        "isDeleted": false
    }
]
```
---------------------------

[========]


11.List Drivers 
=======================


##### Request URL : [/listdrivers/](/listdrivers/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: GET

##### Request data:  None


##### Response: 



```json
[
    {
        "licenseno": "12345",
        "owner": "9599239456",
        "aadharno": "22121",
        "licensefile": "2121",
        "aadharfile": "",
        "name": "",
        "pancard": "",
        "nickname": "",
        "photourl": "",
        "number": "",
        "isActive": false
    },
    {
        "licenseno": "",
        "owner": "9599239456",
        "aadharno": "",
        "licensefile": "",
        "aadharfile": "",
        "name": "",
        "pancard": "",
        "nickname": "",
        "photourl": "",
        "number": "",
        "isActive": false
    }
]
```
---------------------------------------

[========]


12.List Vehicles 
=======================


##### Request URL : [/listvehicles/](/listvehicles/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: GET

##### Request data:  None


##### Response: 



```json
[
    {
        "rcnumber": "HR26BN7992",
        "vtype": "Hatchback",
        "model": "",
        "insuranceno": "",
        "permitno": "",
        "permitdate": "",
        "insdate": "",
        "nickname": "",
        "photo": "",
        "nameofrc": "",
        "isActive": false,
        "owner": "9599239456"
    },
    {
        "rcnumber": "HR26BN7992",
        "vtype": "Hatchback",
        "model": "",
        "insuranceno": "",
        "permitno": "",
        "permitdate": "",
        "insdate": "",
        "nickname": "",
        "photo": "",
        "nameofrc": "",
        "isActive": false,
        "owner": "9599239456"
    }
]

```
-----------------------

[========]


13.Book Trips
=======================


##### Request URL : [/booktrip/](/booktrip/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST

##### Request data: 

```json
{
"tripID" : "7",
"driver" : "12345",
"vehicle" : "HR26BN7992"	
}
```

##### Response: 

Response is list of all trips as per your filter. 

```json
{
    "api": "booktrip",
    "status": "true",
    "info": [
        {
            "tripID": 7,
            "clientName": "Rahul",
            "clientContact": "9599239456",
            "clientSource": "Delhi",
            "clientDestination": "Mumbai",
            "clientPrice": "1200",
            "cartype": "SUV",
            "carModel": "",
            "driver": "12345",
            "vehicle": "HR26BN7992",
            "vendor": "",
            "datetime": "202201151839",
            "isBooked": true,
            "isActive": true,
            "isDeleted": false
        }
    ]
}
```

------------------------------

[========]


14.Delete Driver
=======================


##### Request URL : [/deletedriver/](/deletedriver/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST

##### Request data: 

```json
{
	"licenseno" : "12345"	
}
```

##### Response: 


```json
{
    "api": "deletedriver",
    "status": "true",
    "info": "Driver Deleted"
}
```
----------------------------------

[========]


15.Delete Vehicle
=======================


##### Request URL : [/deletevehicle/](/deletevehicle/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST

##### Request data: 

```json
{
	"rcnumber" : "HR26BN7993"
}
```

##### Response: 


```json
{
    "api": "deletevehicle",
    "status": "true",
    "info": "Vehicle deleted."
}
```

-----------------------

[========]


16.My Trips
=======================


##### Request URL : [/mytriplist/](/mytriplist/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST/GET

##### Request data: 

```json
{
}
```

In case you want to apply some filter on request. Send data in following format. Use any of below options. 

```json
 {        
        "tripID": 1,
        "clientName": "Rahul",
        "clientContact": "9699333232",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151815",    
}
```

##### Response: 

Response is list of all trips as per your filter. 

```json
[
    {
        "tripID": 1,
        "clientName": "Rahul",
        "clientContact": "9699333232",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "clientPrice": "1200",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151815",
        "isBooked": false,
        "isActive": true,
        "isDeleted": false
    },
    {
        "tripID": 2,
        "clientName": "Rahul",
        "clientContact": "9699333232",
        "clientSource": "Delhi",
        "clientDestination": "Mumbai",
        "clientPrice": "1200",
        "cartype": "Hatchback",
        "carModel": "",
        "driver": "",
        "vehicle": "",
        "vendor": "",
        "datetime": "202101151815",
        "isBooked": false,
        "isActive": true,
        "isDeleted": false
    }
]
```


-----------------------------

[========]


17.Get Profile
=======================


##### Request URL : [/getprofile/](/getprofile/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST

##### Request data: 

```json
{

}
```
If you are administrator, you can access profile of other users too. 
```json
{
	"mobile" : "9999999999"
}
```


##### Response: 


```json
{
    "mobile": "9999999999",
    "last_login": null,
    "is_superuser": false,
    "name": "",
    "email": null,
    "password": "ThisIsRootPassword",
    "role": "vendor",
    "address": "",
    "pan": "",
    "panfile": "",
    "is_active": true,
    "is_staff": false,
    "date_joined": "2021-01-19T19:59:44.808097+05:30",
    "groups": [],
    "user_permissions": []
}
```

-------------------------------

[========]


18.Set Profile
=======================


##### Request URL : [/setprofile/](/setprofile/)

##### Prerequisite: i) Valid Session    ii) Session from  Admin or Vendor

##### Request Type: POST

##### Request data: 

```json
{
    "name": "SASa",
    "email": "aa@bb.cc",
    "password": "Pass",
    "role": "vendor",
    "address": "sasa",
    "pan": "sasa",
    "panfile": ""
}
```

If you are administrator, you can set profile for other users too using following payload. 
```json
{
    "mobile": "9999999999",
    "last_login": null,
    "is_superuser": false,
    "name": "",
    "email": null,
    "password": "pass",
    "role": "admin",
    "address": "",
    "pan": "",
    "panfile": "",
    "is_active": true,
    "is_staff": false,
    "date_joined": "2021-01-19T19:59:44.808097+05:30",
    "groups": [],
    "user_permissions": []
}
```

##### Response: 


```json
{
    "api": "setprofile",
    "status": "true",
    "info": "user updated."
}
```

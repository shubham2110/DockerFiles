from . import views
from . import selfviews
from . import otpview
from django.contrib import admin
from django.urls import path, include
from .location import citiesview
from .userviews import uviews

urlpatterns = [
    path('',views.index,name= 'index'),
]

urlpatterns += [
]

urlpatterns += [
    path('uploadfiles/', views.FileUploadView.as_view()),
    path('getfile/<str:pk>',views.FileGetView, name='Get file with ID or name'),
]

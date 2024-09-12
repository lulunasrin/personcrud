from django.contrib import admin
from django.urls import path,include
from myapp.views import person,PersonView,index

from rest_framework.routers import DefaultRouter
from .views import PersonViewSet

router = DefaultRouter()
router.register(r'persons', PersonViewSet)  # Register the viewset with a router


urlpatterns = [
    path("data/",index),


    path('person/', person, name='person'),



    path('persons/', PersonView.as_view(), name='person'),
]+router.urls

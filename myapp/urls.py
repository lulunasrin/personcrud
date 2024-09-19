from django.contrib import admin
from django.urls import path,include
from myapp.views import person,PersonView,index,RegisterUserNewAPI,LoginAPI

from rest_framework.routers import DefaultRouter
from .views import PersonViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'persons', PersonViewSet)  # Register the viewset with a router


urlpatterns = [
    path("data/",index),


    path('person/', person, name='person'),



    path('persons/', PersonView.as_view(), name='person'),

    path('register/', RegisterUserNewAPI.as_view(), name='register'),  # Route for user registration
    path('login/', LoginAPI.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+router.urls

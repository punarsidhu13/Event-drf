"""
URL configuration for Events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Accounts.views import CreateNewUser, LoginUser, LogoutUser, EventRegister, SearchEvents,ChangePASS
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'RegisterEvents', EventRegister, basename='RegisterEvents')
router.register(r'SearchEvents', SearchEvents, basename='search')

urlpatterns = [

    path('admin/', admin.site.urls),
    path('CreateUser', CreateNewUser.as_view()),
    path('LogInUser', LoginUser.as_view()),
    path('LogOutUser', LogoutUser.as_view()),
    path('ChangePASS', ChangePASS.as_view()),
    path('ForgotPassword_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]

urlpatterns += router.urls

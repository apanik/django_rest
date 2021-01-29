
from django.urls import path
from .views import user,register,login,logout,AuthenticatedUser

urlpatterns = [
    path('', user,name="hello"),
    path('register', register,name="register"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
    path('check',AuthenticatedUser.as_view(),name="authencated")

]

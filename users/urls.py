from django.urls import path
from .views import user,register,login,logout,AuthenticatedUser,Permisson,RolesSet,UserGenericView

urlpatterns = [
    path('permissons', Permisson.as_view(),name="Permissons"),
    path('register', register,name="register"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
    path('check',AuthenticatedUser.as_view(),name="authencated"),
    path('roles',RolesSet.as_view({
        'get':'list',
        'post':'create'
    })),
    path('roles/<str:pk>',RolesSet.as_view({
        'put':'update',
        'get':'retrive',
        'delete':'destroy'
    })),
    path('users',UserGenericView.as_view(),name='user'),
    path('user/<int:pk>',UserGenericView.as_view(),name='users')


]

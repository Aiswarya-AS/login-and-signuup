from django.urls import path
from . import views
urlpatterns = [

    path('',views.login_user,name='login'),
    path('home/',views.home_user,name='home'),
    path('signup/',views.signup_user,name='signup'),
    path('logout/',views.logout_user,name='logout'),








    
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.logout_admin,name='admin_logout'),


    path('delete/<int:id>/',views.admin_delete,name='delete'),


    
    path('insert/',views.insert_user,name='insert'),
    path('<int:id>/',views.insert_user,name='update'),
    path('search',views.search,name='search')
    
]

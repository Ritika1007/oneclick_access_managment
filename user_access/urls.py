from django.contrib import admin
from django.urls import path, include, re_path
from . import views
#from rest_auth.registration.views import VerifyEmailView, RegisterView

urlpatterns = [
    path('home', views.home, name="home"),
    # path('user_details', views.user_details, name="user_details"),
    path('server', views.request_server_access, name="server"),
    path('approve_request/<request_id>/', views.approve_request, name='approve_request'),
    path('deny_request/<request_id>/', views.deny_request, name='deny_request'),
    path('databag',views.vault_databag_access,name='databag'),
    path('database',views.vault_database_access,name='database'),
    path('jenkins',views.jenkins_job_access,name='jenkins')
]
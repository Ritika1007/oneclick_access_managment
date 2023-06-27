from django.urls import path
from django.views.generic import RedirectView
from ldap_login.views import login,logout

urlpatterns = [
    path('', RedirectView.as_view(url='login/')),  # Redirect the base URL to the login page
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    #To add logout
    # Other URL patterns
]
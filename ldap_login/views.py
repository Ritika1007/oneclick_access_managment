from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import auth
import sweetify
from ldap_login.tasks import *

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                sweetify.success(request, 'Logged in Successfully!')
                # TASK TO ADD USER TO USER_DEFINITTION TABLE
                add_user_info_db.delay(username)
                return redirect("/home")
                
                # return render(request, 'user_access/base.html') # Replace with the desired URL after login
            else:
                sweetify.warning(request, 'Account is inactive.')
                return redirect("/login")
        else:
            sweetify.error(request, 'Invalid login credentials.')
            return redirect("/login")
    else:
        return render(request, 'login/login.html')
    
def logout(request):
    # if request.method == "POST":
        auth.logout(request)
        sweetify.success(request, 'Logged Out Successfully!')
        return redirect('/login')

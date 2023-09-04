from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserDefinition, ServerDefinition, AccessDefinition
from django.contrib import messages
from user_access.modules.IPA_module import ipa
# from user_access.modules.ssh_paramiko import create_user
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from user_access.tasks import *
import sweetify
import ast
from django.contrib.auth.decorators import login_required
# import json

# Create your views here.
@login_required(login_url='/login')
def home(requests):
    username = requests.user.username
    top_requests = AccessDefinition.objects.filter(emp_user_id=username).order_by('-request_date')[:5]
    logged_in_user = get_object_or_404(UserDefinition, emp_user_id=username)
    manager = logged_in_user.emp_reporting_manager
    return render(requests, 'user_access/home.html',{'username': username, 'manager': manager, 'top_requests': top_requests})


###################
def create_access_definition_object(requests,ac_details,ac_type):
    # print("you got here")

    #creating access request for logged in user name.
    empID = get_object_or_404(UserDefinition, emp_user_id = requests.user.username)
    # print(empID.emp_reporting_manager)

    approval_request = AccessDefinition.objects.create(
        emp_user_id = empID,
        access_details = ac_details,
        approver_mail = empID.emp_reporting_manager,
        access_granted = "Pending",
        manager_approval = "Pending",
        access_type = ac_type
        )
    # print("Nopsi")
    return approval_request


def delay_tasks(requests,approval_request):
    username = requests.user.username

    logged_in_user = get_object_or_404(UserDefinition, emp_user_id=username)
    recipient=logged_in_user.emp_reporting_manager
    send_mail_for_approval.delay(approval_request.request_id,recipient)

    context = {'user':username,'rep_mgr': recipient,'request_details':approval_request.access_details,'request_id':approval_request.request_id}
    # print(approval_request.jira_id)
    send_request_details_to_requester.delay(context,username)

    #mail to notify requester -> request sent for approval
    mail_sent_notification(requests,approval_request.request_id)


###################server access
@login_required(login_url='/login')
def request_server_access(requests):
    username = requests.user.username
    if requests.method == 'POST':
        request_data = str(requests.POST['serverip'])
        sshkeycheckbox = requests.POST.get('sshkeycheckbox')
        sshkey = requests.POST.get('sshkey') if sshkeycheckbox == 'on' else None
        if sshkey is not None:
            user_ssh = get_object_or_404(UserDefinition, emp_user_id=username)
            user_ssh.emp_ssh_key = sshkey
            user_ssh.save()
        approval_request = create_access_definition_object(requests,request_data,'Server')
        
        delay_tasks(requests,approval_request)

        return redirect("/home")
        
    elif requests.method == 'GET':
        # username = requests.user.username
        return render(requests, 'user_access/request_server_access_form.html',{'username': username})
    
    else:
        return HttpResponse("An Exception Occoured!") 

@login_required(login_url='/login')
def vault_database_access(requests):
    if requests.method == 'POST':

        request_data = str(requests.POST['db_name'])
        approval_request = create_access_definition_object(requests,request_data,'Vault Database')       
        
        delay_tasks(requests,approval_request)

        return redirect("/home")
        
    elif requests.method == 'GET':
        username = requests.user.username
        return render(requests, 'user_access/vault_database_access.html',{'username': username})
    
    else:
        return HttpResponse("An Exception Occoured!") 
    

@login_required(login_url='/login')
def vault_databag_access(requests):
    if requests.method == 'POST':

        request_data = str(requests.POST['dataurl']+':'+requests.POST['prod'])
        # product = str(requests.POST['prod'])
        approval_request = create_access_definition_object(requests,request_data,'Vault Databag')
        delay_tasks(requests,approval_request)

        return redirect("/home")
        
    elif requests.method == 'GET':
        username = requests.user.username
        return render(requests, 'user_access/vault_databag_access.html',{'username': username})
    
    else:
        return HttpResponse("An Exception Occoured!") 

@login_required(login_url='/login')
def jenkins_job_access(requests):

    if requests.method == 'POST':

        request_data = str(requests.POST['job_name'])
        approval_request = create_access_definition_object(requests,request_data,'Jenkins Job')        
        delay_tasks(requests,approval_request)

        return redirect("/home")
        
    elif requests.method == 'GET':
        username = requests.user.username
        return render(requests, 'user_access/jenkins_job_access.html',{'username': username})
    
    else:
        return HttpResponse("An Exception Occoured!") 


###################
#what will happen after approval
def approve_request(requests, request_id):
    approval_request = get_object_or_404(AccessDefinition, request_id=request_id)
    #one thing to add -> send mail to requester after access granted.
    
    if approval_request.manager_approval == "Pending":
        
        approval_request.manager_approval = "approved"
        approval_request.save()
        provide_access.delay(request_id,approval_request.access_type)

        # return HttpResponse("approved")
        return render(requests, 'user_access/approved_thanks_page.html')
    elif approval_request.manager_approval=="denied":
        return HttpResponse("Request is already denied, Please create a new request")
    elif approval_request.manager_approval=="approved":
        return HttpResponse("Request is already approved")

    return HttpResponse("Oops! Not able to process")


###################
def deny_request(requests, request_id):
    deny_request = get_object_or_404(AccessDefinition, request_id=request_id)
    if deny_request.manager_approval == "Pending":
        deny_request.manager_approval = "denied"
        deny_request.save()
        return HttpResponse("denied",request_id)
    elif deny_request.manager_approval=="denied":
        return HttpResponse("Request is already denied")
    elif deny_request.manager_approval=="approved":
        return HttpResponse("Request is already approved")
    
###################
def mail_sent_notification(requests,request_id):
    message = f"Request ID:  {request_id}"
    sweetify.info(requests,
    title='Approval Decision Sent',
    text=message,
    timer=None,
    button='Ok'
    )
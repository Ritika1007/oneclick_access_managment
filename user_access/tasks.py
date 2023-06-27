from celery import shared_task
from .models import UserDefinition, ServerDefinition, AccessDefinition
# from user_access.modules.ssh_paramiko import create_user
from django.shortcuts import render, get_object_or_404
from user_access.modules.IPA_module import ipa
from user_access.modules.callJenkinsJob import *
from user_access.modules.vault import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

@shared_task
def provide_access(request_id,access_type):

    server_url = settings.JENKINS_URL
    username = settings.JENKINS_USER
    password = settings.JENKINS_PASSOWRD
    approval_request = get_object_or_404(AccessDefinition, request_id=request_id)
    obj = approval_request.emp_user_id
    emp_display_name = getattr(obj, "emp_display_name")
    emp_mail_id = str(getattr(obj, "emp_user_id"))+"@freecharge.com"


    #for server access
    if access_type == 'Server':
        #JENKINS JOB CLIENT
        # jenkins_client = build_jenkins_client(server_url, username, password)

        emp_user_id = getattr(obj, "emp_user_id")
        # emp_display_name = getattr(obj, "emp_display_name")

        obj_ip = approval_request.access_details

        NoServer=len(obj_ip.split(','))
        count=0
        ad_grp = []
        for ip in obj_ip.split(','):
            server = ServerDefinition.objects.get(ip_address = ip)
            if server.is_managed_ad == "Yes":
                print(ip, server.server_ad_grp)
                if server.server_ad_grp not in ad_grp:
                    ad_grp.append(server.server_ad_grp)
                #call jenkins job to add user to ad grp
            else:
                print(ip, server.server_key)

                job_name = "ServerAccessJob_clone_test"
                parameters = {
                    'IP_ADDRESS': ip,
                    'username': emp_user_id, 
                    'rsa_key': emp_sshkey,
                    'PEM_KEY': server.server_key+".pem"
                }
                build_status = run_jenkins_job(server_url, username, password, job_name,parameters)


                # result = create_user(ip,emp_user_id,emp_sshkey,server.server_key)

                # print(result)
                if build_status == "SUCCESS":
                    count+=1
        if len(ad_grp)>0:
            string = " ".join(ad_grp)
            print(string)
            job_name = 'Add_user_into_ipa_AD_group'
            parameters = {
                    'username': emp_display_name,
                    'adgroup': string
                }
            build_status = run_jenkins_job(server_url, username, password, job_name,parameters)
            # build_status = 'SUCCESS'
            print(build_status)
            if build_status == "SUCCESS":
                    count+=len(ad_grp)


            
        if count == NoServer:
            approval_request.access_granted = "Yes"
            send_mail_to_requester(request_id,emp_mail_id,emp_display_name,obj_ip)
            
        else:
            approval_request.access_granted = "No"

        approval_request.save()

    #for Vault Databag access
    if access_type == 'Vault Databag':
        emp_display_name = getattr(obj, "emp_display_name")
        obj = approval_request.access_details
        product = obj.split(':')[-1]
        obj_ip = obj.split(':')[0]
        # print(product,obj_ip)



        keyword=[]

        for URL in obj_ip.split(','):
            URL=URL.split('/')
            if URL[-1]=="":
                key=URL[-2]
                env=URL[-3]
            else:
                key=URL[-1]
                env=URL[-2]
            keyword.append(key+'_'+env)

            if key.count('-')==2:
                key1=key.split('-')[-2]+'-'+key.split('-')[-1]
                key2=key.split('-')[-3]+key.split('-')[-2]
                key3=key.split('-')[-2]

                keyword.extend([key1+'_'+env,key2+'_'+env,key3+'_'+env])
            
            if key.count('-')==1 and key.split('-')[-1]=="service":
                key3=key.split('-')[0]
                keyword.append(key3+'_'+env)
            
            if key.count('-')==1 and key.split('-')[-1]!="service":
                key4=key.split('-')[1]
                keyword.append(key4+'_'+env)

        print(keyword)
        ad_grp = fetch_databag_ldap_grp(settings.VAULT_URL,settings.VAULT_USER,settings.VAULT_PASSWORD,keyword,product)
        # print(ad_grp)

        if len(ad_grp)>0:
            string = " ".join(ad_grp)
            print(string)
            job_name = 'Add_user_into_ipa_AD_group'
            parameters = {
                    'username': emp_display_name,
                    'adgroup': string
                }
            build_status = run_jenkins_job(server_url, username, password, job_name,parameters)
            # build_status = 'SUCCESS'
            print(build_status)
            if build_status == "SUCCESS":
                approval_request.access_granted = "Yes"
                send_mail_to_requester(request_id,emp_mail_id,emp_display_name,obj_ip,'Vault Databag')
            
            else:
                approval_request.access_granted = "No"

        approval_request.save()

    #for Vault database access
    if access_type == 'Vault Database':
        emp_user_id = getattr(obj, "emp_user_id")
        database = approval_request.access_details
        print(database, emp_user_id)

        build_status = fetch_database_config(settings.VAULT_URL,settings.VAULT_USER,settings.VAULT_PASSWORD,database,emp_user_id)
        print(build_status)
        if build_status == "SUCCESS":
                approval_request.access_granted = "Yes"
                send_mail_to_requester(request_id,emp_mail_id,emp_display_name,database, 'Vault Database')
            
        else:
                approval_request.access_granted = "No"

        approval_request.save()
    
    #for Jenkins Job access
    if access_type == 'Jenkins Job':
        emp_display_name = getattr(obj, "emp_display_name")
        job_name = approval_request.access_details

        ad_grp = get_config_jenkins_job(server_url, username, password, job_name)

        if len(ad_grp)>0:
            string = " ".join(ad_grp)
            print(string)
            jenkins_job_name = 'Add_user_into_ipa_AD_group'
            parameters = {
                    'username': emp_display_name,
                    'adgroup': string
                }
            build_status = run_jenkins_job(server_url, username, password, jenkins_job_name, parameters)
            # build_status = 'SUCCESS'
            print(build_status)
            if build_status == "SUCCESS":
                approval_request.access_granted = "Yes"
                send_mail_to_requester(request_id,emp_mail_id,emp_display_name,job_name,'Jenkins Job')
            
            else:
                approval_request.access_granted = "No"

        approval_request.save()



def send_mail_to_requester(request_id,recipient,emp_display_name,access_details,requested_for):
    from_email = "sre@freecharge.com"
    recipient_list = [recipient]
    subject = 'Access Granted Notification'

    context = {'user': emp_display_name, 'request_details' : access_details, 'request_id':request_id, 'requested_for':requested_for}
    
    message = render_to_string('user_access/approval_notification_send.html', context)

    send_mail(
        subject,
        '',
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=False,
    )


@shared_task
def send_mail_for_approval(request_id, recipient):

    approval_request = get_object_or_404(AccessDefinition, request_id=request_id)

    request_id=approval_request.request_id
    access_details = approval_request.access_details
    emp_display_name = approval_request.emp_user_id.emp_user_id
    ac_type = approval_request.access_type


    #reverse-URL
    allow_url = reverse("approve_request", args=[request_id])
    deny_url = reverse("deny_request", args=[request_id])
    allow_link = f"{settings.BASE_URL}{allow_url}"
    deny_link = f"{settings.BASE_URL}{deny_url}"
    subject=''


    # render the email template with the request object
    if ac_type=='Server':
        subject = "Server Access Request"
    elif ac_type == "Vault Databag":
        subject = "Vault Databag Access Request"
    elif ac_type == "Vault Database":
        subject = "Vault Database Access Request"
    elif ac_type == "Jenkins Job":
        subject = "Jenkins Job Access Request"

    context = {'request_header': ac_type,'employee_name': emp_display_name, 'request_details' : access_details, 'approve_url': allow_link, 'deny_url': deny_link}
    
    message = render_to_string('user_access/approval_request_email.html', context)
    #text_content = strip_tags(message)

    from_email = "sre@freecharge.com"
    recipient_list = [recipient]
    # subject = "Access Granted Notification"

    send_mail(
        subject,
        '',
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=False,
    )


@shared_task
def send_request_details_to_requester(context,username):
    from_email = "sre@freecharge.com"
    recipient = username+"@freecharge.com"
    # print(recipient)
    recipient_list = [recipient]
    message = render_to_string('user_access/approval_decision_sent.html', context)
    subject = "Access Request for "+ context['request_details']

    send_mail(
        subject,
        '',
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=False,
    )
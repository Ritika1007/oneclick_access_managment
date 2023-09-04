from celery import shared_task
from user_access.models import UserDefinition
from django.shortcuts import render, get_object_or_404
from user_access.modules.IPA_module import ipa
from oneclick.settings import IPA_URL,IPA_USER,IPA_PASSWORD

@shared_task
def add_user_info_db(username):
    if not (UserDefinition.objects.filter(emp_user_id = username).exists()):
        ipa_obj=ipa(IPA_URL)
        print(IPA_URL)
        ipa_obj.login(IPA_USER,IPA_PASSWORD)
        abc=ipa_obj.user_show(username)
        DisName = abc['result']['result']['gecos'][0]
        AD_grp = ",".join(abc['result']['result']['memberof_group'])
        email_id = username+"@example.com"
        emp_reporting_manager = "abc@example.com"
        user_add = UserDefinition(emp_user_id = username, emp_display_name = DisName, email_mail_id = email_id, initial_ad_grps = AD_grp, emp_reporting_manager = emp_reporting_manager)
        user_add.save()


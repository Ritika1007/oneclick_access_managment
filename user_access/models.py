from django.db import models
import uuid

class VarCharForeignKey(models.ForeignKey):
    def db_type(self, connection):
        return 'varchar(50)'

class UserDefinition(models.Model):
    emp_user_id = models.CharField(primary_key=True, max_length=50, default="abc")
    emp_mail_id = models.CharField(max_length=50, null=False)
    emp_display_name = models.CharField(max_length=50,null=True)
    emp_reporting_manager = models.CharField(max_length=50, null=False)
    initial_ad_grps = models.TextField(null=True,blank=True)
    servers = models.TextField(null=True,blank=True)
    jenkins_job = models.TextField(null=True,blank=True)
    databags = models.TextField(null=True,blank=True)
    database = models.TextField(null=True,blank=True)
    emp_ssh_key = models.TextField(null=True,blank=True)
    objects = models.Manager()

class ServerDefinition(models.Model):
    ip_address = models.CharField(max_length=30, primary_key=True, null=False)
    server_name = models.CharField(max_length=100, null=False)
    server_ad_grp = models.CharField(max_length=50, null=True)
    server_key = models.CharField(max_length=50, null=False)
    aws_account = models.CharField(max_length=50, null=False, default="Cigar")
    is_pci = models.CharField(max_length=5, null=False)
    is_infra = models.CharField(max_length=5, null=False)
    is_db = models.CharField(max_length=5, null=False)
    is_managed_ad = models.CharField(max_length=5, null=False)
    objects = models.Manager()

class AccessDefinition(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_user_id = VarCharForeignKey(UserDefinition, on_delete=models.DO_NOTHING, to_field='emp_user_id', default="abc")
    access_details = models.TextField(null=False)
    access_type = approver_mail= models.CharField(max_length=50, null=False, default="Test")
    request_date = models.DateTimeField(auto_now_add=True,null=False)
    approver_mail= models.CharField(max_length=50, null=False, editable=False)
    approval_date = models.DateTimeField(auto_now=True)
    manager_approval= models.CharField(max_length=50, null=False, default="Pending")
    access_granted = models.CharField(max_length=50, null=False, default="Pending")
    jira_id = models.CharField(max_length=50, null=True)
    objects = models.Manager()
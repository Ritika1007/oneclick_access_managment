import sys
import boto3
from user_access.modules.IPA_module import ipa
# from IPA_module import ipa
from django.conf import settings

ip_range = {
    "ip" : ["aws_profile","ap-south-1"],
    "ip" : ["aws_profile","us-west-2"],
    
}

def fetch_aws_info(ip):

    ip_check = ip.split('.')[1]
    server_add = ""
    # server_add_dict = {}

    if ip_check in ip_range:
        profile,region = ip_range[ip_check]
        session = boto3.Session(profile_name=profile, region_name=region)
        filters = [
            {
                'Name': 'private-ip-address',
                'Values': [ip]
            }
        ]
        ec2_client = session.client('ec2')
        instances = ec2_client.describe_instances(Filters=filters)
        if len(instances['Reservations']) == 0:
            sys.exit(404)

        #ssh keyName
        keyName=instances['Reservations'][0]['Instances'][0]['KeyName']

        key_to_find = 'Name'
        for item in instances['Reservations'][0]['Instances'][0]['Tags']:
            if item['Key'] == key_to_find:
                value = item['Value']
                # print(f"The value of '{key_to_find}' is '{value}'")
                break
        

        # server_add += f"ip_address = '{ip}', server_key = '{keyName}', aws_account = '{profile}', "
        server_add_dict = {
            'ip_address': ip,
            'server_key': keyName,
            'aws_account': profile
        }

        if profile in ['klickpay', 'supernova']:
            # server_add += "is_pci = 'Yes', "
            server_add_dict['is_pci'] = 'Yes'

        else:
            # server_add += "is_pci = 'No', "
            server_add_dict['is_pci'] = 'No'

        if ip_check == "241":
            # server_add += "is_infra = 'Yes', "
            server_add_dict['is_infra'] = 'Yes'
        else:
            # server_add += "is_infra = 'No', "
            server_add_dict['is_infra'] = 'No'

        
        if "-db-" in value:
            # server_add += "is_db = 'Yes', "
            server_add_dict['is_db'] = 'Yes'

        else:
            # server_add += "is_db = 'No', "
            server_add_dict['is_db'] = 'No'



        
        abc = ipa(settings.IPA_URL)
        abc.login(settings.IPA_USER,settings.IPA_PASSWORD)
        xyz=abc.host_find(value)
        # print(xyz)
        if len(xyz['result']['result']) == 0:
            # tmp = f"server_name = '{value}', server_ad_grp = 'null',  is_managed_ad = 'No'"
            tmp_dict = {
                'server_name': value,
                'server_ad_grp' : 'null',
                'is_managed_ad': 'No'   
            }
            

        else:
            # ad_grp = ",".join(xyz['result']['result'][0]['memberof_hostgroup'])
            ad_grp = xyz['result']['result'][0]['memberof_hostgroup'][0]
            fqdn  = xyz['result']['result'][0]['cn'][0]
            # tmp = f"server_name = '{fqdn}', server_ad_grp = '{ad_grp}',  is_managed_ad = 'Yes'"
            tmp_dict = {
                'server_name': fqdn,
                'server_ad_grp' : ad_grp,
                'is_managed_ad': 'Yes'   
            }
        
        # server_add += tmp
        server_add_dict.update(tmp_dict)
        # print(server_add_dict)
        return server_add_dict

# ip = sys.argv[1]
# fetch_aws_info(ip)
import hvac
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize the hvac client

def vault_client(vault_server,username,password):

    client = hvac.Client(url=vault_server, verify=False)
    client.auth.ldap.login(
        username=username,
        password=password,
        mount_point="ldap"
    )
    return client

def compare_substrings_with_strings(substrings, strings):
    return [string for string in strings if any(substring in string for substring in substrings)]


def fetch_databag_ldap_grp(vault_server,username,password,keyword,product):
    client = vault_client(vault_server,username,password)
    groups = client.auth.ldap.list_groups()
    # if groups:
    #     grps = groups['data']['keys']
    #     matched_strings=compare_substrings_with_strings(keyword,grps)
    # return matched_strings

    if groups:

        grps = groups['data']['keys']
        # # print(grps)
        matched_strings=[]
        for key in keyword:
            matched  = list(filter(lambda s: key in s, grps))
            if len(matched)>1:
                sub = list(filter(lambda s: product.lower() in s.split('_')[0], matched))
                matched_strings.extend(sub)
                # print(sub)
            else:
                matched_strings.extend(matched)
                # print (matched)


            # print (matched_strings)
        matched_strings=list(set(matched_strings))
        return matched_strings


def get_user_policy(client,uname):
    # client = vault_client(vault_server,username,password)
    ldap_users = client.ldap.list_users()

    for user in ldap_users['data']['keys']:

        if uname == user:
            # print(user)
            response=client.ldap.read_user(
            username=uname
            )
            existing_policies=response['data']['policies']
            return existing_policies
    return 'None'

def set_user_policy(client,uname,policies_arr):
    response = client.ldap.create_or_update_user(
        username=uname,
        policies=policies_arr,
    )
    # print(response)
    if response :
        return "SUCCESS"
    else:
        return "Failure"


def fetch_database_config(vault_server,username,password,database,uname):

    if 'prod' in database:
        print("Oopsi we can't give u prod db access")
    else:
        config=[]
        client = vault_client(vault_server,username,password)
        print(database)
        #get db policies
        for db in database.split(','):
            response = client.secrets.database.read_connection(
                name=db
            )
            config.extend(response['data']['allowed_roles'])

        existing_policies = get_user_policy(client,uname)
        print(uname)
        print("existing_policies",existing_policies)
        if existing_policies != 'None':
            config.extend(existing_policies)
        config = list(set(config))
        print("New Policies", config)
        status = set_user_policy(client,uname,config)
        return status
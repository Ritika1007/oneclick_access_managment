# import the installed Jira library
from jira import JIRA
from django.conf import settings



JIRA_URL = 'https://example.atlassian.net'
JIRA_USER =  "User"
JIRA_TOKEN = 'API token'

jiraOptions = {'server': JIRA_URL}
  

jira = JIRA(options=jiraOptions, basic_auth=(
   JIRA_USER , JIRA_TOKEN))


def user_account_id(email):
    user = jira.search_users(query=email)
    # print (users)
    if user:
        user = user[0]
        return user.accountId

def create_issue(summary,description,issue_type,user):
    env = 'Production'
    id = user_account_id(user+"@example.com")
    # Create the issue
    if 'Jenkins' in summary:
        issue_dict = {
            "project": {"key": "Test"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
            "customfield_00000": {'value': env},
            "reporter" : {'id': id},
        }
    elif 'Server' in summary:
        customfield_14373_value = "Permanent"
        if ".cn" in user:
            customfield_14373_value = "Contract"
        print(customfield_14373_value)
        issue_dict = {
            "project": {"key": "SP"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
            "reporter" : {'id': id},
            "customfield_00000": {"value": "Read"},
            "customfield_00000": {"value": "Old"},
            "customfield_00000": {"value": customfield_14373_value},
            "customfield_00000": {"value": "No"}, 
            "customfield_00000": "NA", #
            "customfield_00000": "Server Access", #
            "customfield_00000": {"value": env},
            "customfield_00000": "EC2", #
            "customfield_00000": "NA" #
        }
    elif 'Vault' in summary:
        issue_dict = {
            "project": {"key": "SP"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Tools Access Request"}
        }
    else:
        raise ValueError("Invalid keyword provided")
        
    new_issue = jira.create_issue(fields=issue_dict)
    new_issue.update({"assignee" : {'accountId': id}})
    return new_issue.key


def add_comment(issue_key,comment):
    issue = jira.issue(issue_key)
    jira.add_comment(issue, comment)

def status_transition(issue_key):

    issue = jira.issue(issue_key)
    transitions = jira.transitions(issue)
    # print(transitions)
    for transition in transitions:
        if  transition['name'] == "Peer Review":
            
            transition_id = transition['id']
            print(transition_id)

    jira.transition_issue(issue, transition_id)

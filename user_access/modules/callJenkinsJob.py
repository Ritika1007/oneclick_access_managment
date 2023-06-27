import jenkins
import time
import os
import xmltodict

os.environ["PYTHONHTTPSVERIFY"] = "0"



def run_jenkins_job(jenkins_url, username, password, job_name, parameters):
    # Connect to the Jenkins server
    server = jenkins.Jenkins(jenkins_url, username=username, password=password)

    # Trigger the job
    server.build_job(job_name,parameters)
    time.sleep(10)

    last_build_number=0
    count=0
    # # Wait for the job to complete
    while True:
        job_info = server.get_job_info(job_name)
        last_build_number=job_info['lastBuild']['number']
        print(last_build_number)
        # if job_info['inQueue'] or job_info['lastBuild']['number']!=job_info['lastCompletedBuild']['number'] or count <=5:
        if job_info['lastBuild']['number']!=job_info['lastCompletedBuild']['number'] and count <=6:
            count+=1
            time.sleep(5)
        else:
            break

    # Get the output of the build
    build_info = server.get_build_info(job_name, last_build_number)
    # print(build_info['result'])
    return build_info['result']


def get_config_jenkins_job(jenkins_url, username, password, job_name):
    # Connect to the Jenkins server
    server = jenkins.Jenkins(jenkins_url, username=username, password=password)

    # Retrieve job configuration
    ad_grp=[]
    for job in job_name.split(','):
        job_configuration = server.get_job_config(job)
        config_dict = xmltodict.parse(job_configuration)
        data=config_dict['flow-definition']['properties']['hudson.security.AuthorizationMatrixProperty']['permission']
        # ad_grp=[]
        for i in data:
            if 'GROUP:com.cloudbees.plugins.credentials.CredentialsProvider.View' in i:
                ad_grp.append(i.split(':'[-1])[-1])
    return(list(set(ad_grp)))
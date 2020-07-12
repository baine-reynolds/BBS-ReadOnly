import requests
import getpass
import json
from resources.init import Init
from resources.api import Api

url = input("Please enter the Source instance's Base URL (i.e. https://bitbucket.mycompany.com (Server)):\n")
admin_user = input("Please enter the Admin username for your source environment:\n")
admin_password = getpass.getpass("Please enter the Admin password for your source environment:\n")

session = requests.Session()
session.auth = (admin_user, admin_password)

'''
    Utilizes https://docs.atlassian.com/bitbucket-server/rest/7.4.0/bitbucket-ref-restriction-rest.html#idp1
'''

def update_revert_data(repo, permission_id, revert_data):
    # Adds project if it doesn't already exist
    if repo['project']['key'] not in revert_data.keys():
        revert_data[repo['project']['key']] = {}
    # Adds the repo slug to the appropreiate project and sets the value of the permission id of the restriction created
    revert_data[repo['project']['key']][repo['slug']] = permission_id
    return revert_data

def write_revert_file(revert_data):
    with open('revert_file.json', 'w') as revert_file:
        json.dump(revert_data, revert_file)

def read_revert_file():
    with open('revert_file.json', 'r') as revert_file:
        revert_data = json.load(revert_file)
    return revert_data

def main():
    options, args = Init.parse_options()

    if options.revert == False:
        revert_data = {}
        for project in Api.read_serv_projects(url, session):
            for repo in Api.read_serv_repos(url, session, project):
                permission_id = Api.write_serv_repos_readonly(url, session, project, repo)
                revert_data = update_revert_data(repo, permission_id, revert_data)

        write_revert_file(revert_data)
    else:
        revert_data = read_revert_file()
        for project_key in revert_data.keys():
            for repo_slug, permission_id in revert_data[project_key].items():
                Api.revert_repo(url, session, project_key, repo_slug, permission_id)

if __name__ == '__main__':
    main()
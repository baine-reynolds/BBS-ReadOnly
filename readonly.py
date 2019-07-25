import requests
import getpass
import json

url = input("Please enter the Source instance's Base URL (i.e. https://bitbucket.mycompany.com (Server)):\n")
admin_user = input("Please enter the Admin username for your source environment:\n")
admin_password = getpass.getpass("Please enter the Admin password for your source environment:\n")

session = requests.Session()
session.auth = (admin_user, admin_password)


def read_serv_projects(proj_start=None, proj_limit=None):
	while True:
		proj_params = {'start': proj_start, 'limit': proj_limit}
		p = session.get(url + '/rest/api/1.0/projects', params=proj_params)
		p_data = p.json()
		for project_json in p_data['values']:
			yield project_json
		if p_data['isLastPage'] == True:
			return
		proj_start = p_data['nextPageStart']


def read_serv_repos(project_json, repo_start=None, repo_limit=None):
	while True:
		repo_params = {'start': repo_start, 'limit': repo_limit}
		r = session.get(url + '/rest/api/1.0/projects/' + project_json['key'] + '/repos', params=repo_params)
		r_data = r.json()
		for repo_json in r_data['values']:
			yield repo_json
		if r_data['isLastPage'] == True:
			return
		repo_start = r_data['nextPageStart']

def write_serv_repos_readonly(project_json, repo_json):
	headers = {'X-Atlassian-Token': 'nocheck'}
	payload = {"type": "read-only", "matcher": { "id": "*", "displayId": "*", "type": { "id": "PATTERN", "name": "Pattern"}, "active": True }}
	print("setting Read-Only on repo " + repo_json['slug'])
	r = session.post(url + "/rest/branch-permissions/latest/projects/" + project_json['key'] + "/repos/" + repo_json['slug'] + "/restrictions", json=payload, headers=headers)

if url:
	r = session.get(url + '/status')
	status = str(r.status_code)
	if status == "200":
		for project_json in read_serv_projects():
			for repo_json in read_serv_repos(project_json):
				write_serv_repos_readonly(project_json, repo_json)
	else:
		print("Server not Reachable")

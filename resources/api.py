import requests
import json

class Api():
    def read_serv_projects(url, session, proj_start=None, proj_limit=None):
        while True:
            proj_params = {'start': proj_start, 'limit': proj_limit}
            p = session.get(f"{url}/rest/api/1.0/projects", params=proj_params)
            p_data = p.json()
            for project_json in p_data['values']:
                yield project_json
            if p_data['isLastPage'] == True:
                return
            proj_start = p_data['nextPageStart']

    def read_serv_repos(url, session, project_json, repo_start=None, repo_limit=None):
        while True:
            repo_params = {'start': repo_start, 'limit': repo_limit}
            r = session.get(f"{url}/rest/api/1.0/projects/{project_json['key']}/repos", params=repo_params)
            r_data = r.json()
            for repo_json in r_data['values']:
                yield repo_json
            if r_data['isLastPage'] == True:
                return
            repo_start = r_data['nextPageStart']

    def write_serv_repos_readonly(url, session, project_json, repo_json):
        headers = {'X-Atlassian-Token': 'nocheck'}
        payload = {"type": "read-only", "matcher": { "id": "*", "displayId": "*", "type": { "id": "PATTERN", "name": "Pattern"}, "active": True }}
        print("setting Read-Only on repo " + repo_json['slug'])
        r = session.post(f"{url}/rest/branch-permissions/latest/projects/{project_json['key']}/repos/{repo_json['slug']}/restrictions", json=payload, headers=headers)
        r_data = r.json()
        return r_data['id']

    def revert_repo(url, session, project_key, repo_slug, permission_id):
        print(f"Removing Read-Only branch permission from Repo: {repo_slug} with the id: {permission_id}")
        r = session.delete(f"{url}/rest/branch-permissions/latest/projects/{project_key}/repos/{repo_slug}/restrictions/{permission_id}")
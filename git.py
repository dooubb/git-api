import requests
import json

org_url = ''
git_token = ''
owner = ''
collaborator_user_data = {}
user_name = ''
headers = {}
repo_list = []
user_list = []
# 创建hook所需参数字典
data = {
    "name": "web",
    "active": True,
    "events": [
        "push"
    ],
    "config": {
        "url": "https://change/github-webhook/",
        "content_type": "json",
        "insecure_ssl": "0"
    }
}


def get_branches():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/branches"
        resp = requests.get(url, headers=headers)
        branch_list = resp.json()
        print(f"当前仓库-->> {repo}")
        for branch in branch_list:
            name = branch["name"]
            protected = branch["protected"]
            print(f"分支名字-->> {name}\t是否为保护分支-->> {protected}")


def get_hooks(repo):
    url = f"{org_url}/repos/{owner}/{repo}/hooks"
    resp = requests.get(url, headers=headers)
    hook_list = resp.json()
    if len(hook_list) == 0:
        print(f"当前{repo}仓库的没有hook")
    else:
        for hook_json in hook_list:
            hook_id = hook_json["id"]
            print(f"获取当前{repo}仓库的hook信息\thook id 为 {hook_id}")
            return hook_id


def create_hooks():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/hooks"
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        if resp.status_code == 201:
            print(f"创建当前{repo}仓库的hook...")
            hook_json = resp.json()
            hook_info(hook_json)
        else:
            print(f"hook创建失败 {resp.text}")


def delete_hooks():
    for repo in repo_list:
        hook_id = get_hooks(repo)
        url = f"{org_url}/repos/{owner}/{repo}/hooks/{hook_id}"
        resp = requests.delete(url, headers=headers)
        if resp.status_code == 204:
            print("删除hook成功！！！")
        else:
            print(f"删除失败 {resp.text}")


def hook_info(hook_json):
    hook_id = hook_json["id"]
    hook_type = hook_json["type"]
    hook_last_response = hook_json["last_response"]
    hook_config = hook_json["config"]
    print(f"hook id -->>{hook_id} hook名字-->>{hook_config} hook类型-->>{hook_type} hook状态-->>{hook_last_response}")


def get_collaborators():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/collaborators"
        resp = requests.get(url, headers=headers)
        print(resp.text)


def delete_collaborators():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user_name}"
        resp = requests.delete(url, headers=headers)
        if resp.status_code == 204:
            print(f"删除{repo}的成员-->>{user_name} 成功！！！")
        else:
            print(f"删除{repo}的成员-->>{user_name} 失败 {resp.text}")


def add_collaborators():
    for repo in repo_list:
        for user in user_list:
            url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user}"
            resp = requests.put(url, data=json.dumps(collaborator_user_data), headers=headers)
            if resp.status_code == 204:
                print(f"添加{repo}的成员-->>{user} 成功！！！")
            else:
                print(f"添加{repo}的成员-->>{user} 失败 {resp.text}")


def check_collaborators():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user_name}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 204:
            print(f"{user_name}是{repo}的成员！！！")
        else:
            print(f"{user_name}不是{repo}的成员")


def get_collaborators_permission():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user_name}/permission"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            user_info(resp.json())
        else:
            print(f"{user_name}不是{repo}的成员")


def user_info(user_json):
    permission = user_json["permission"]
    name = user_json["user"]["login"]
    role_name = user_json["role_name"]
    print(f"用户名字 -->>{name} \npermission-->>{permission} \n权限-->>{role_name}")


def get_tags():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/tags"
        resp = requests.get(url, headers=headers)
        print(f"当前仓库-->> {repo}")
        if resp.status_code == 200:
            for tag in resp.json():
                tag_name = tag["name"]
                print(f"tag名字-->> {tag_name}")

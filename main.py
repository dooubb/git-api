import requests;
import json

# https://docs.github.com/cn/rest/webhooks/repos

# 公司组织的url 默认值为api.github.com
org_url = 'https://api.github.com'
# 访问git的token
git_token = 'access_token'
# git仓库的组织名字
owner = 'org_name'
# 删除hook时使用的id 通过get_hook方法获取
hook_id = 'hook_id'
# 仓库列表，可以批量执行
repo_list = ['repo_name']
# 仓库名字
repo = ''
# git的用户名
user_name = ''
# permission 支持常用权限 读pull 写push 管理员admin
collaborator_user_data = {"permission": "push"}
# 创建hook所需参数字典
data = {
    "name": "web",
    "active": True,
    "events": [
        "push"
    ],
    "config": {
        "url": "webhook_url",
        "content_type": "json",
        "insecure_ssl": "0"
    }
}

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "token " + git_token + ""
}


def get_branch():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/branches"
        resp = requests.get(url, headers=headers)
        branch_list = resp.json()
        print(repo)
        for branch in branch_list:
            name = branch["name"]
            protected = branch["protected"]
            print(f"分支名字-->>{name} 是否为保护分支-->>{protected}")


def get_hooks():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/hooks"
        resp = requests.get(url, headers=headers)
        hook_list = resp.json()
        print(repo)
        for hook_json in hook_list:
            hook_info(hook_json)


def create_hooks():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/hooks"
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        if resp.status_code == 201:
            print("hook创建成功！！！")
            hook_json = resp.json()
            print(repo)
            hook_info(hook_json)
        else:
            print(f"hook创建失败 {resp.text}")


def delete_hooks():
    for repo in repo_list:
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


def delete_hook():
    url = f"{org_url}/repos/{owner}/{repo}/hooks/{hook_id}"
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 204:
        print(f"删除{repo}的hook成功！！！")
    else:
        print(f"删除失败 {resp.text}")


def get_collaborators():
    url = f"{org_url}/repos/{owner}/{repo}/collaborators"
    resp = requests.get(url, headers=headers)
    print(resp.text)


def delete_collaborators():
    url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user_name}"
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 204:
        print(f"删除{repo}的成员-->>{user_name} 成功！！！")
    else:
        print(f"删除{repo}的成员-->>{user_name} 失败 {resp.text}")


def add_collaborators():
    url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user_name}"
    resp = requests.put(url, data=json.dumps(collaborator_user_data), headers=headers)
    if resp.status_code == 204:
        print(f"添加{repo}的成员-->>{user_name} 成功！！！")
    else:
        print(f"添加{repo}的成员-->>{user_name} 失败 {resp.text}")


def check_collaborators():
    url = f"{org_url}/repos/{owner}/{repo}/collaborators/{user_name}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 204:
        print(f"{user_name}是{repo}的成员！！！")
    else:
        print(f"{user_name}不是{repo}的成员")


def get_collaborators_permission():
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


if __name__ == '__main__':
    get_hooks()

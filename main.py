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
hook_id='hook_id'
# 仓库列表，可以批量执行
repo_list = ['repo_name']
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
        if resp.status_code==201:
            print("hook创建成功！！！")
            hook_json = resp.json()
            print(repo)
            hook_info(hook_json)
        else:
            print(f"hook创建失败 {resp.text}")



def delete_hooks():
    for repo in repo_list:
        url = f"{org_url}/repos/{owner}/{repo}/hooks/{hook_id}"
        resp = requests.delete(url,headers=headers)
        if resp.status_code==204:
            print("删除hook成功！！！")
        else:
            print(f"删除失败 {resp.text}")

def hook_info(hook_json):
    hook_id = hook_json["id"]
    hook_type = hook_json["type"]
    hook_last_response = hook_json["last_response"]
    hook_config = hook_json["config"]
    print(f"hook id -->>{hook_id} hook名字-->>{hook_config} hook类型-->>{hook_type} hook状态-->>{hook_last_response}")

if __name__ == '__main__':
    get_hooks()

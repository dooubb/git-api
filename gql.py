import requests

headers = {}
owner = ""
repo_list = ""
org_url = ""
org_graphql_url = ""
client = ""


def get_repo_id(repo):
    url = f"{org_url}/repos/{owner}/{repo}"
    resp = requests.get(url, headers=headers)
    return resp.json()["node_id"]


def get_branch_protection_info():
    for repo in repo_list:
        query = '{repository(owner:"' + owner + '",name:"' + repo + '"){branchProtectionRules(last: 1){nodes{id,pattern,}}}}'
        resp = client.execute(query=query)
        node = resp["data"]["repository"]["branchProtectionRules"]["nodes"]
        if len(node) == 0:
            print(f"当前仓库{repo}没有分支保护")
        else:
            branch_protection_rule_id = node[0]["id"]
            print(f"查询{repo}的分支保护-->>分支保护id为: {branch_protection_rule_id}")
            return branch_protection_rule_id


def create_branch_protection(pattern):
    for repo in repo_list:
        repo_id = get_repo_id(repo)
        print(f"准备创建{repo}的分支保护-->>仓库id为: {repo_id}")
        create = 'mutation CreateBranchProtectionRule { createBranchProtectionRule(input:{repositoryId:"' + repo_id + '",pattern:"' + pattern + '",requiresApprovingReviews: true, requiredApprovingReviewCount: 1}){ clientMutationId,branchProtectionRule{databaseId,pattern,creator{login}} } }'
        resp = client.execute(query=create)
        print(resp)


def delete_branch_protection():
    for repo in repo_list:
        branch_protection_rule_id = get_branch_protection_info()
        print(f"准备删除{repo}的分支保护-->>分支保护id为: {branch_protection_rule_id}")
        delete = 'mutation DeleteBranchProtectionRuleInput { deleteBranchProtectionRule(input:{branchProtectionRuleId:"' + branch_protection_rule_id + '"}){ clientMutationId}}'
        resp = client.execute(query=delete)
        print(resp)


def update_branch_protection():
    for repo in repo_list:
        branch_protection_rule_id = get_branch_protection_info(repo)
        print(f"准备更新{repo}的分支保护-->>分支保护id为: {branch_protection_rule_id}")
        update = 'mutation UpdateBranchProtectionRule { updateBranchProtectionRule(input:{pattern:"' + pattern + '",requiresApprovingReviews: true, requiredApprovingReviewCount: 1,branchProtectionRuleId:"' + branch_protection_rule_id + '"}){ clientMutationId } }'
        resp = client.execute(query=update)
        print(resp)


from reader import init_config
import git
import gql

if __name__ == '__main__':

    init_config()
    # gql.create_branch_protection(gql.pattern)
    # gql.get_branch_protection_info()

    git.get_hooks('git-api')
    # git.create_hooks()
    # git.delete_hooks()
    # git.get_branches()
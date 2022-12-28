from configparser import ConfigParser, NoSectionError, NoOptionError
from python_graphql_client import GraphqlClient
from dotenv import load_dotenv
import os
import git
import gql

# 如果存在环境变量的文件，则加载配置到环境变量
if os.path.exists("settings.env"):
    load_dotenv("settings.env")

os_env = os.environ


def read_config(filename: str) -> ConfigParser:
    """
    从文件中读取配置信息

    Parameters
    ----------
    filename : str, 配置文件
    """
    # 实例化对象
    config = ConfigParser()
    if not os.path.exists(filename):
        raise FileNotFoundError(f"配置文件 {filename} 不存在")
    config.read(filename, encoding="utf-8")
    return config


def get_config(config: ConfigParser, section: str, key: str):
    """
    根据指定section和key获取value

    Parameters
    ----------
    config:  ConfigParser(), 配置实例对象
    section: str, 配置文件中的区域
    key:     str, 配置的参数名
    """
    # 优先从环境变量中获取配置参数, 没有的话再从配置文件中获取
    value = os_env.get(key, "")
    if not value:
        try:
            value = config.get(section, key)
        except (NoOptionError, NoSectionError):
            # 没有的话就返回None
            value = None
    return value


def init_config():
    # 初始化配置文件中的参数
    config = read_config("config.ini")
    git.org_url = get_config(config, "config", "org_url")
    git.git_token = get_config(config, "config", "git_token")
    git.owner = get_config(config, "config", "owner")
    git.collaborator_user_data = eval(get_config(config, "config", "collaborator_user_data"))
    git.user_name = get_config(config, "config", "user_name")
    git.branch = get_config(config, "config", "branch")
    git.headers = eval(get_config(config, "config", "headers"))
    git.user_list = (get_config(config, "config", "user_list").strip(',').split(','))
    git.repo_list = (get_config(config, "config", "repo_list").strip(',').split(','))

    gql.owner = get_config(config, "config", "owner")
    gql.org_url = get_config(config, "config", "org_url")
    gql.pattern = get_config(config, "config", "pattern")
    gql.headers = eval(get_config(config, "config", "headers"))
    gql.org_graphql_url = get_config(config, "config", "org_graphql_url")
    gql.repo_list = (get_config(config, "config", "repo_list").strip(',').split(','))

    # 初始化GraphqlClient
    gql.client = GraphqlClient(endpoint=gql.org_graphql_url, headers=gql.headers)

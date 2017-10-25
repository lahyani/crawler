# pylint: disable=invalid-name
# -*- coding: utf-8 -*-
"""
Helpers
"""

STANDARD_TIMESTAMP_LENGTH = 13

def get_arguments():
    """
    Retrieve arguments passed to the command line
    :return: sum
    :rtype: dict
    """
    import sys
    import argparse
    parser = argparse.ArgumentParser(
        description='Crawl some page to extract useful data'
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--plateforme',
        help='One of the social media site: facebook, twitter, instagram'
    )
    parser.add_argument('--uri', help='Key for data to extract')
    parser.add_argument('--page_id', help='Page id')
    arguments = {}
    if len(sys.argv[1:]) >= 1:
        arguments = parser.parse_args()
    else:
        parser.print_help()
    return arguments

def get_timestamp():
    """

    Return time as a timestamp

    Args:
        None

    Returns:
        string : timestamp as formated string
    """
    import time
    nowStr = str(time.time())
    nowStr = nowStr.replace('.', '')
    floating = STANDARD_TIMESTAMP_LENGTH - len(nowStr)
    return nowStr + ('0' * floating)

def read_yaml_file(path):
    """ dd"""
    import os.path
    import yaml
    config = None
    if os.path.isfile(path) and os.access(path, os.R_OK):
        with open(path) as f:
            config = yaml.safe_load(f)
    return config

def get_database_config(path):
    """ dd"""
    return read_yaml_file(path)

def get_task_config(path):
    """ dd"""
    return read_yaml_file(path)

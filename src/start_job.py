#!/usr/bin/python
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# -*- coding: utf-8 -*-
"""
Start point for the crawler
"""

from parta import utils
from parta.models import Entity, Component
from parta import jobs

# Define config files paths
config_file = {
    "database" : "./config/config.yaml",
    "jobs" : [
        "./job/bunch_001.yaml",
        "./job/bunch_002.yaml",
    ],
}
# Load database configuration
database_config = utils.get_database_config(config_file["database"])
if database_config:
    # Load scheduled tasks
    for tasks_path in config_file["jobs"]:
        job_config = utils.get_task_config(tasks_path)
        if job_config:
            # For each task execute the corresponding task
            for task in job_config["tasks"]:
                params = task['arguments']
                arguments = {
                    "params" : params,
                    "db" : {
                        "config" : database_config,
                    },
                    "plateforme" : task['plateforme'],
                }
                # Right now only Facebook and fans count (likes) and visitors count (visits) are supported
                if task['plateforme'] == Entity.TYPE_FACEBOOK:
                    if params['component'] == Component.TYPE_FANS_COUNT:
                        jobs.fans_count(arguments)
                    if params['component'] == Component.TYPE_VISITORS_COUNT:
                        jobs.visitors_count(arguments)

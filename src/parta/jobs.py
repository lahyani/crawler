"""
d
"""

from parta.tasks import BaseTask, FacebookTask
from parta.models import FansCountComponent, Entity

def process(args):
    """Common function process"""
    import time
    if args.has_key("target") and isinstance(args["target"], BaseTask):
        task = args["target"]
        loop = args["params"]["loop"]
        delay = args["params"]["delay"]
        i = 0
        while i < loop:
            i = i+1
            task.run()
            if loop > i:
                time.sleep(delay)

def fans_count(args):
    """fans_count"""
    from threading import Thread
    page_id = args["params"]["page_id"]
    task = FacebookTask(
        page_id.lower(),
        args["params"]["component"],
        args["db"]["config"],
    )
    args["target"] = task
    Thread(
        target=process,
        args=[args]
    ).start()

def visitors_count(args):
    """visitors_count"""
    from threading import Thread
    page_id = args["params"]["page_id"]
    task = FacebookTask(
        page_id.lower(),
        args["params"]["component"],
        args["db"]["config"],
    )
    args["target"] = task
    Thread(
        target=process,
        args=[args]
    ).start()

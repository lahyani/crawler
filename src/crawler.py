#!/usr/bin/python
# pylint: disable=invalid-name
# pylint: disable=C0412
# -*- coding: utf-8 -*-

"""
app
"""

from parta import utils

arguments = utils.get_arguments()
if arguments:
    import os.path
    import yaml
    from parta.models import Compaign, FacebookEntity, FansCountComponent, Element
    from parta.exceptions import PartaException
    from parta.db import Firebase as PartaFirebase
    from parta.facebookcrawler import FacebookCrawler, Parser

    CONFIG_FILE_PATH = "./config/config.yaml"

    config = None
    if not os.path.isfile(CONFIG_FILE_PATH) and not os.access(CONFIG_FILE_PATH, os.R_OK):
        print "Error when accessing config file."\
        " Please check if either the file exists or is readable!"
        exit(1)

    with open(CONFIG_FILE_PATH) as f:
        # use safe_load instead load
        config = yaml.safe_load(f)
    if config:
        fbase = PartaFirebase(config)
        page_id = None
        uri = None
        plateforme = None

        if arguments.page_id:
            page_id = arguments.page_id
        if arguments.uri:
            uri = arguments.uri
        if arguments.plateforme:
            plateforme = arguments.plateforme
        if plateforme and page_id and uri:
            # TODO Move the code to a module
            if plateforme.lower() == 'facebook':
                if uri.lower() == FacebookCrawler.CRAWLER_FANS_COUNT:
                    compaign = Compaign(page_id)
                    fb_entity = FacebookEntity(compaign, page_id)
                    fb_fanscount = FansCountComponent(fb_entity)
                    try:
                        fb_entity.register_children(fb_fanscount)
                        compaign.register_children(fb_entity)
                        last_count = Element('last_fans_count', fb_fanscount)
                        """
                        Instanciate the crawler and the parser for the specific uri
                        """
                        fc = FacebookCrawler(fb_entity)
                        fc.add_parser(Parser.FACEBOOK_FANS_COUNT)
                        data = fc.parse(Parser.FACEBOOK_FANS_COUNT)

                        if data:
                            timestamp = utils.get_timestamp()
                            data['timestamp'] = timestamp
                            last_count.data = data
                            # TODO Add Event class and dispatch save_element_after
                            fbase.write(last_count)
                            stats = Element('stats', fb_fanscount)
                            stats.data = {
                                "count": data["count"]
                            }
                            fbase.push(timestamp, stats)
                    except PartaException as e:
                        print e

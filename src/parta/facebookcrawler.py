"""
FacebookCrawler
"""
import sys
import time
import re
import requests

import justext

from parta.exceptions import PartaException
from parta.crawlers import Crawler
from parta.parsers import Parser

class FanCountParser(Parser):
    """
    FanCountParser
    """
    def run(self):
        """run."""
        return self.fetch()

    def fetch(self):
        """fetch."""
        data = {}
        url = self._entity.page_url
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            text = paragraph.text.encode('utf-8')
            results = re.search(r'^([0-9,]{6,})(\s?likes?)$', text)
            if results:
                likes = results.group(1)
                likes = int(likes.replace(',', ''))
                data["count"] = likes
        return data

class FacebookCrawler(Crawler):
    """
    FacebookCrawler
    """
    def add_parser(self, parser_type):
        """add_parser."""
        if parser_type == Parser.FACEBOOK_FANS_COUNT:
            parser = FanCountParser(self._entity, Parser.FACEBOOK_FANS_COUNT)
            self.register_parsers(parser)
        if parser_type == Parser.FACEBOOK_VISITORS_COUNT:
            parser = VisitorsCountParser(self._entity, Parser.FACEBOOK_VISITORS_COUNT)
            self.register_parsers(parser)

    def parse(self, parser_type):
        """parse."""
        data = self.execute(parser_type)
        return data

class VisitorsCountParser(Parser):
    """
    VisitorsCountParser
    """
    def run(self):
        """run."""
        return self.fetch()

    def fetch(self):
        """fetch."""
        data = {}
        url = self._entity.page_url
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            text = paragraph.text.encode('utf-8')
            results = re.search(r'^([0-9,]{6,})(\s?visits?)$', text)
            if results:
                likes = results.group(1)
                likes = int(likes.replace(',', ''))
                data["count"] = likes
        return data

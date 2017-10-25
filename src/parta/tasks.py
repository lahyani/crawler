# pylint: disable=invalid-name
"""
Module tasks
"""
from parta.models import Compaign, FacebookEntity, Component
from parta.events import Event

class BaseTask(object):
    """
    BaseTask
    """
    pass

class FacebookTask(BaseTask):
    """
    FacebookTask
    """
    def __init__(self, page_id, component_type, db_config):
        self.__compaign = Compaign(page_id)
        self.__entity = FacebookEntity(self.__compaign, page_id)
        self.__db_config = db_config
        self.__component = None
        self.__component_type = component_type
        self.__commands = {
            Component.TYPE_FANS_COUNT: self.__fans_count,
            Component.TYPE_VISITORS_COUNT: self.__visitors_count,
        }

    def run(self):
        """
        run
        """
        if self.__commands.has_key(self.__component_type):
            self.__commands[self.__component_type]()

    def _override_data(self, args):
        """_override_data"""
        if args["data"].has_key("count"):
            args["data"]["stats/title"] = "Last Fans Count"

    def __fans_count(self):
        """__fans_count"""
        from parta.models import FansCountComponent
        self.__component = FansCountComponent(self.__entity, "Fans Count", self.__db_config)
        event = Event()
        event.register('before_write_facebook_fans_count_stats', self._override_data)
        self.__component.event = event
        self.__component.parse()


    def __visitors_count(self):
        """__visitors_count"""
        from parta.models import VisitorsCountComponent
        self.__component = VisitorsCountComponent(self.__entity, "Visitors Count", self.__db_config)
        event = Event()
        event.register('before_write_facebook_visitors_count_stats', self._override_data)
        self.__component.event = event
        self.__component.parse()        

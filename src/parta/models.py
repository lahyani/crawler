"""
Module models
"""
from parta.exceptions import PartaException
from parta import utils

class Collection(object):
    """Collection"""

    def __init__(self):
        self._children = []

    @property
    def children(self):
        """entities."""
        return self._children

    def register_children(self, *args):
        """register_children."""
        raise NotImplementedError("Subclasses should implement this!")

class BaseClass(object):
    """BaseClass"""

    def __init__(self, path, title=None):
        self._path = path
        self._title = title
        self._type = None
        self._db = None
        self._name = None
        self._parent = None
        self._event = None

    @property
    def title(self):
        """title."""
        return self._title

    @property
    def class_type(self):
        """typclass_typee."""
        return self._type

    @class_type.setter
    def class_type(self, _type):
        """type."""
        self._type = _type

    @property
    def name(self):
        """ Return Name """
        return self._name

    @property
    def path(self):
        """ Return Firebase path """
        return self._path

    @property
    def absolute_path(self):
        """absolute_path."""
        if self._parent:
            return self._parent.absolute_path + "/" + self._path
        else:
            return self._path

    @property
    def parent(self):
        """parent."""
        return self._parent

    def init_db(self, config):
        """data"""
        from parta.db import Firebase as Partafirebase
        self._db = Partafirebase(config)

    @property
    def event(self):
        """event"""
        return self._event

    @event.setter
    def event(self, event):
        """event"""
        self._event = event

    @property
    def database(self):
        """database"""
        return self._db

    @database.setter
    def database(self, database):
        """database"""
        self._db = database

class Entity(BaseClass, Collection):
    """Entity"""

    TYPE_FACEBOOK = "facebook"
    TYPE_TWITTER = "twiiter"

    def __init__(self, path, compaign, page_id, title=None):
        if isinstance(compaign, Compaign):
            BaseClass.__init__(self, path, title)
            Collection.__init__(self)
        else:
            raise PartaException("Argument 2 must to be instance of Compaign")
        self._parent = compaign
        self._page_id = page_id
        self._type = None
        self._name = None
        self._url = None

    @property
    def page_id(self):
        """page_id."""
        return self._page_id

    @property
    def url(self):
        """url."""
        return "http://" + self._url

    @property
    def secure_url(self):
        """secure_url."""
        return "https://" +  self._url

    @property
    def page_url(self):
        """page_url."""
        return self.url + "/" + self._page_id

    @property
    def secure_page_url(self):
        """secure_page_url."""
        return self.secure_url + "/" + self._page_id

    @property
    def components(self):
        """components."""
        return self._children

    def register_children(self, *args):
        """register_children."""
        for component in args:
            if isinstance(component, Component):
                if component.parent == self:
                    self._children.append(component)
                else:
                    message = "The given instance of Component did'nt belong"\
                     "to the current Entity instance!."
                    raise PartaException(message)
            else:
                message = "Unsupported Object! Arguments must to be instance of Component."
                raise PartaException(message)


class Component(BaseClass, Collection):
    """
    Component Class
    """
    TYPE_FANS_COUNT = "fans_count"
    TYPE_VISITORS_COUNT = "visitors_count"

    def __init__(self, path, entity, title=None):
        if isinstance(entity, Entity):
            path = "components/" + path
            BaseClass.__init__(self, path, title)
            Collection.__init__(self)
        else:
            raise PartaException("Argument 2 must to be instance of Entity")
        self._parent = entity
        self._elements = []

    @property
    def elements(self):
        """elements."""
        return self._children

    def register_children(self, *args):
        """register_children."""
        for element in args:
            if isinstance(element, Element):
                if element.parent == self:
                    self._children.append(element)
                else:
                    message = "The given instance of Element did'nt belong"\
                     "to the current Component instance!."
                    raise PartaException(message)
            else:
                message = "Unsupported Object! Arguments must to be instance of Element."
                raise PartaException(message)

    @property
    def event(self):
        """event"""
        return self._event

    @event.setter
    def event(self, event):
        """event"""
        self._event = event
        for child in self._children:
            child.event = self._event

class Element(BaseClass):
    """
    Element Class
    """
    TYPE_LAST_FANS_COUNT = "last_fans_count"
    TYPE_FANS_STATS = "stats"
    TYPE_VISITORS_STATS ="stats"
    TYPE_LAST_VISITORS_COUNT = "last_visitors_count"

    def __init__(self, path, component, title=None):
        if isinstance(component, Component):
            path = "elements/" + path
            super(Element, self).__init__(path, title)
        else:
            raise PartaException("Argument 2 must to be instance of Component")
        self._parent = component
        self._data = None
        self._event_type = None

    @property
    def event_type(self):
        """event_type"""
        return self._event_type

    @event_type.setter
    def event_type(self, _event_type):
        """event_type"""
        self._event_type = _event_type

    @property
    def data(self):
        """data"""
        return self._data

    @data.setter
    def data(self, data):
        """data"""
        self._data = data

    def write(self, data):
        """write"""
        if self._db:
            listener_data = {
                "target" : self,
                "type" : None,
                "args" : data,
            }
            if self._event:
                event_type = "before_write" + self._event_type
                listener_data["type"] = event_type
                self._event.fire(event_type, listener_data)
            self._db.write(listener_data)
            if self._event:
                event_type = "after_write" + self._event_type
                listener_data["type"] = event_type
                self._event.fire(event_type, listener_data)

    def push(self, key, arg):
        """push"""
        if self._db:
            arg["key"] = key
            listener_data = {
                "target" : self,
                "type" : None,
                "args" : arg
            }
            if self._event:
                event_type = "before_push" + self._event_type
                listener_data["type"] = event_type
                self._event.fire(event_type, listener_data)
            self._db.push(listener_data)
            if self._event:
                event_type = "after_push" + self._event_type
                listener_data["type"] = event_type
                self._event.fire(event_type, listener_data)

class Compaign(BaseClass, Collection):
    """
    Compaign Class
    """
    def __init__(self, path, title=None):
        path = "compaigns/" + path
        BaseClass.__init__(self, path, title)
        Collection.__init__(self)
        self._name = "compaign"

    def register_children(self, *args):
        """register_children."""
        for entity in args:
            if isinstance(entity, Entity):
                if entity.parent == self:
                    self._children.append(entity)
                else:
                    message = "The given instance of Entity did'nt belong"\
                     "to the current Compaign instance!."
                    raise PartaException(message)
            else:
                message = "Unsupported Object! Argument 1 must to be instance of Entity."
                raise PartaException(message)

class FacebookEntity(Entity):
    """
    Facebook
    """""
    def __init__(self, compaign, page_id, title=None):
        path = "entities/facebook"
        super(FacebookEntity, self).__init__(path, compaign, page_id, title)
        self._url = "www.facebook.com"
        self._page_id = page_id
        self._name = "facebook"
        self._type = Entity.TYPE_FACEBOOK

"""
Twitter Class
"""
class TwitterEntity(Entity):
    """
    Twitter
    """""
    def __init__(self, compaign, page_id, title=None):
        path = "entities/twitter"
        super(TwitterEntity, self).__init__(path, compaign, page_id, title)
        self._url = "www.twitter.com"
        self._page_id = page_id
        self._name = "twitter"
        self._type = Entity.TYPE_TWITTER

class FansCountComponent(Component):
    """
    FansCountComponent
    """
    def __init__(self, entity, title=None, db_config=None):
        from parta.facebookcrawler import FacebookCrawler
        path = "fans_count"
        super(FansCountComponent, self).__init__(path, entity, title)
        self._name = "fans_count"
        self.class_type = Component.TYPE_FANS_COUNT
        self._crawler = FacebookCrawler(self.parent)
        self._last_fans_count = Element('last_fans_count', self)
        self._last_fans_count.class_type = Element.TYPE_LAST_FANS_COUNT
        self._last_fans_count.event_type = '_facebook_fans_count_last_fans_count'
        self._stats = Element('stats', self)
        self._stats.class_type = Element.TYPE_FANS_STATS
        self._stats.event_type = '_facebook_fans_count_stats'
        self.register_children(self._last_fans_count, self._stats)
        if db_config:
            self.init_db(db_config)
            self._last_fans_count.database = self.database
            self._stats.database = self.database

    def parse(self):
        """parse"""
        from parta.facebookcrawler import Parser
        self._crawler.add_parser(Parser.FACEBOOK_FANS_COUNT)
        data = self._crawler.parse(Parser.FACEBOOK_FANS_COUNT)

        timestamp = utils.get_timestamp()
        data["timestamp"] = timestamp
        count = data["count"]
        node = {
            "absolute_path" : self.absolute_path,
            "path" : self._last_fans_count.path,
            "data" : {
                "count" : count,
                "timestamp" : timestamp,
            }
        }
        self._last_fans_count.write(node)
        node = {
            "absolute_path" : self.absolute_path,
            "path" : self._stats.path,
            "data" : {
                "count" : count,
            }
        }
        self._stats.push(timestamp, node)


class VisitorsCountComponent(Component):
    """
    VisitorsCountComponent
    """
    def __init__(self, entity, title=None, db_config=None):
        from parta.facebookcrawler import FacebookCrawler
        path = "visitors_count"
        super(VisitorsCountComponent, self).__init__(path, entity, title)
        self._name = "fans_count"
        self.class_type = Component.TYPE_FANS_COUNT
        self._crawler = FacebookCrawler(self.parent)
        self._last_fans_count = Element('last_visitors_count', self)
        self._last_fans_count.class_type = Element.TYPE_LAST_VISITORS_COUNT
        self._last_fans_count.event_type = '_facebook_visitors_count_last_visitors_count'
        self._stats = Element('stats', self)
        self._stats.class_type = Element.TYPE_VISITORS_STATS
        self._stats.event_type = '_facebook_visitors_count_stats'
        self.register_children(self._last_fans_count, self._stats)
        if db_config:
            self.init_db(db_config)
            self._last_fans_count.database = self.database
            self._stats.database = self.database

    def parse(self):
        """parse"""
        from parta.facebookcrawler import Parser
        self._crawler.add_parser(Parser.FACEBOOK_VISITORS_COUNT)
        data = self._crawler.parse(Parser.FACEBOOK_VISITORS_COUNT)

        timestamp = utils.get_timestamp()
        data["timestamp"] = timestamp
        count = data["count"]
        node = {
            "absolute_path" : self.absolute_path,
            "path" : self._last_fans_count.path,
            "data" : {
                "count" : count,
                "timestamp" : timestamp,
            }
        }
        self._last_fans_count.write(node)
        node = {
            "absolute_path" : self.absolute_path,
            "path" : self._stats.path,
            "data" : {
                "count" : count,
            }
        }
        self._stats.push(timestamp, node)

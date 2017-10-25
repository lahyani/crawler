"""
e
"""

class Event(object):
    """
    Event
    """
    TYPE_FACEBOOK_LAST_FANS_COUNT = "facebook_last_fans_count"
    TYPE_FACEBOOK_FANS_STATS = "facebook_fans_stats"

    def __init__(self):
        self.__events = {}

    def fire(self, event_type, data):
        """c"""
        if self.__events:
            if self.__events.has_key(event_type):
                for event in self.__events[event_type]:
                    event(data)

    def register(self, event_type, callback):
        """c"""
        if self.__events:
            if self.__events.has_key(event_type):
                self.__events[event_type].append(callback)
            else:                
                self.__events[event_type] = []
                self.__events[event_type].append(callback)
        else:
            self.__events[event_type] = []
            self.__events[event_type].append(callback)

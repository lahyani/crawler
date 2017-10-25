"""
Parsers
"""

class Parser(object):
    """
    Parser
    """
    FACEBOOK_FANS_COUNT = "facebook_fans_count"
    FACEBOOK_VISITORS_COUNT = "facebook_visitors_count"

    def __init__(self, entity, parser_type):
        """constructor."""
        self._type = parser_type
        self._entity = entity

    def run(self):
        """run."""
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def type(self):
        """type."""
        return self._type

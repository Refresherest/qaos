"""
QAOS Briefing Manager
"""

from .briefing import Briefing


class BriefingManager:

    def create(self, objective):

        return Briefing(objective)


briefing_manager = BriefingManager()
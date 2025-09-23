

from src.dao.badge_dao import BadgeDAO

class BadgeService:
    dao = BadgeDAO()

    @classmethod
    def create(cls, name: str, description: str, aura_color: str, vibe_level: int):
        return cls.dao.create(name, description, aura_color, vibe_level)

    @classmethod
    def list(cls):
        return cls.dao.list()

from src.dao.soul_link_dao import SoulLinkDAO

class SoulLinkService:
    dao = SoulLinkDAO()

    @classmethod
    def create(cls, viber_id: int, friend_id: int):
        return cls.dao.create(viber_id, friend_id)

    @classmethod
    def update_status(cls, link_id: int, status: str):
        return cls.dao.update_status(link_id, status)
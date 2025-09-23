

from src.dao.reverberation_dao import ReverberationDAO

class ReverberationService:
    dao = ReverberationDAO()

    @classmethod
    def create(cls, thought_id: int, viber_id: int, content: str):
        return cls.dao.create(thought_id, viber_id, content)

    @classmethod
    def list(cls, thought_id: int):
        return cls.dao.list_by_thought(thought_id)
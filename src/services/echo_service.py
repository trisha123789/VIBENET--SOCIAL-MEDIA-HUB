

from src.dao.echo_dao import EchoDAO

class EchoService:
    dao = EchoDAO()

    @classmethod
    def react(cls, thought_id: int, viber_id: int, emotion: str):
        return cls.dao.react(thought_id, viber_id, emotion)
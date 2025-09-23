from typing import Dict, List, Optional
from src.dao.thought_dao import ThoughtDAO

class ThoughtService:
    dao = ThoughtDAO()

    @classmethod
    def create(cls, viber_id: int, content: str, emotion_tag: str) -> Dict:
        return cls.dao.create(viber_id, content, emotion_tag)

    @classmethod
    def get(cls, thought_id: int) -> Optional[Dict]:
        return cls.dao.get_by_id(thought_id)

    @classmethod
    def list_recent(cls, limit: int = 10) -> List[Dict]:
        return cls.dao.list_recent(limit)

    @classmethod
    def update(cls, thought_id: int, updates: Dict) -> Optional[Dict]:
        return cls.dao.update(thought_id, updates)

    @classmethod
    def delete(cls, thought_id: int) -> bool:
        return cls.dao.delete(thought_id)

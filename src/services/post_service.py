

from typing import Dict, List, Optional
from src.dao.post_dao import PostDAO

class PostService:
    dao = PostDAO()

    @classmethod
    def create(cls, user_id: int, content: str) -> Dict:
        return cls.dao.create(user_id, content)

    @classmethod
    def get(cls, post_id: int) -> Optional[Dict]:
        return cls.dao.get_by_id(post_id)

    @classmethod
    def list_recent(cls, limit: int = 10) -> List[Dict]:
        return cls.dao.list_recent(limit)

    @classmethod
    def update(cls, post_id: int, updates: Dict) -> Optional[Dict]:
        return cls.dao.update(post_id, updates)

    @classmethod
    def delete(cls, post_id: int) -> bool:
        return cls.dao.delete(post_id)

    @classmethod
    def like(cls, post_id: int) -> Optional[Dict]:
        return cls.dao.like(post_id)

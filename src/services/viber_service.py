  
from typing import Dict, List, Optional
from src.dao.viber_dao import ViberDAO

class ViberService:
    dao = ViberDAO()

    @classmethod
    def register(cls, username: str, email: str, password: str, aura_color: str = "Neutral") -> Dict:
        if cls.dao.get_by_username(username):
            raise ValueError(f"Username '{username}' already exists.")
        return cls.dao.create(username, email, password, aura_color)

    @classmethod
    def get(cls, viber_id: int) -> Optional[Dict]:
        return cls.dao.get_by_id(viber_id)

    @classmethod
    def list(cls) -> List[Dict]:
        return cls.dao.list_all()

    @classmethod
    def update(cls, viber_id: int, updates: Dict) -> Optional[Dict]:
        return cls.dao.update(viber_id, updates)

    @classmethod
    def delete(cls, viber_id: int) -> bool:
        return cls.dao.delete(viber_id)

from typing import Dict, Optional, List
from src.config import get_supabase

class ViberDAO:
    def __init__(self):
        self._db = get_supabase()

    def create(self, username: str, email: str, password: str, aura_color: str = "Neutral") -> Optional[Dict]:
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "aura_color": aura_color,
            "vibe_level": 1,
            "badges": []
        }
        self._db.table("vibers").insert(payload).execute()
        return self.get_by_username(username)

    def get_by_id(self, viber_id: int) -> Optional[Dict]:
        resp = self._db.table("vibers").select("*").eq("viber_id", viber_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_username(self, username: str) -> Optional[Dict]:
        resp = self._db.table("vibers").select("*").eq("username", username).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_all(self, limit: int = 100) -> List[Dict]:
        resp = self._db.table("vibers").select("*").limit(limit).execute()
        return resp.data or []

    def update(self, viber_id: int, updates: Dict) -> Optional[Dict]:
        self._db.table("vibers").update(updates).eq("viber_id", viber_id).execute()
        return self.get_by_id(viber_id)

    def delete(self, viber_id: int) -> bool:
        self._db.table("vibers").delete().eq("viber_id", viber_id).execute()
        return True

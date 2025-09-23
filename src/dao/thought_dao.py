from typing import Dict, Optional, List
from src.config import get_supabase

class ThoughtDAO:
    def __init__(self):
        self._db = get_supabase()

    def create(self, viber_id: int, content: str, emotion_tag: str) -> Optional[Dict]:
        payload = {"viber_id": viber_id, "content": content, "emotion_tag": emotion_tag}
        self._db.table("thoughts").insert(payload).execute()
        return self.list_recent(1)[0] if self.list_recent(1) else None

    def get_by_id(self, thought_id: int) -> Optional[Dict]:
        resp = self._db.table("thoughts").select("*").eq("thought_id", thought_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_recent(self, limit: int = 10) -> List[Dict]:
        resp = self._db.table("thoughts").select("*").order("created_at", desc=True).limit(limit).execute()
        return resp.data or []

    def update(self, thought_id: int, updates: Dict) -> Optional[Dict]:
        self._db.table("thoughts").update(updates).eq("thought_id", thought_id).execute()
        return self.get_by_id(thought_id)

    def delete(self, thought_id: int) -> bool:
        self._db.table("thoughts").delete().eq("thought_id", thought_id).execute()
        return True

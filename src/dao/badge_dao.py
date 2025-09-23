

from src.config import get_supabase

class BadgeDAO:
    def __init__(self):
        self._db = get_supabase()

    def create(self, name: str, description: str, aura_color: str, vibe_level: int):
        resp = self._db.table("badges").insert({
            "name": name,
            "description": description,
            "aura_color": aura_color,
            "vibe_level_required": vibe_level
        }).execute()
        return resp.data

    def list(self):
        return self._db.table("badges").select("*").execute().data

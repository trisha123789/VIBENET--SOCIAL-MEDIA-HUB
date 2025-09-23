from src.config import get_supabase

class ReverberationDAO:
    def __init__(self):
        self._db = get_supabase()

    def create(self, thought_id: int, viber_id: int, content: str):
        resp = self._db.table("reverberations").insert({
            "thought_id": thought_id,
            "viber_id": viber_id,
            "content": content
        }).execute()
        return resp.data

    def list_by_thought(self, thought_id: int):
        resp = self._db.table("reverberations").select("*").eq("thought_id", thought_id).execute()
        return resp.data

from src.config import get_supabase

class SoulLinkDAO:
    def __init__(self):
        self._db = get_supabase()

    def create(self, viber_id: int, friend_id: int):
        resp = self._db.table("soul_links").insert({
            "viber_id": viber_id,
            "friend_id": friend_id
        }).execute()
        return resp.data

    def update_status(self, link_id: int, status: str):
        resp = self._db.table("soul_links").update({"status": status}).eq("link_id", link_id).execute()
        return resp.data
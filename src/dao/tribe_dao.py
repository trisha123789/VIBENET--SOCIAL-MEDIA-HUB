from src.config import get_supabase

class TribeDAO:
    def __init__(self):
        self._db = get_supabase()

    def create(self, name, description):
        return self._db.table("tribes").insert({
            "name": name,
            "description": description
        }).execute().data

    def list(self):
        return self._db.table("tribes").select("*").execute().data

    def join(self, viber_id, tribe_id):
        return self._db.table("viber_tribes").insert({
            "viber_id": viber_id,
            "tribe_id": tribe_id
        }).execute().data

    def list_viber_tribes(self, viber_id):
        return self._db.table("viber_tribes").select("*").eq("viber_id", viber_id).execute().data

from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


@lru_cache
def get_storage_client() -> Client | None:
    key = settings.storage_key_secret or settings.supabase_key
    if not settings.supabase_url or not key:
        return None
    return create_client(settings.supabase_url, key)


def upload_resume_file(file_bytes: bytes, object_name: str, content_type: str) -> str | None:
    client = get_storage_client()
    if client is None:
        return None
    client.storage.from_(settings.supabase_bucket).upload(
        path=object_name,
        file=file_bytes,
        file_options={"content-type": content_type, "upsert": "false"},
    )
    return client.storage.from_(settings.supabase_bucket).get_public_url(object_name)


def delete_resume_file(object_name: str | None) -> None:
    client = get_storage_client()
    if client is not None and object_name:
        client.storage.from_(settings.supabase_bucket).remove([object_name])

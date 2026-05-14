from supabase import create_client, Client
from app.core.config import settings

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.STORAGE_KEY_SECRET
)

def upload_resume_file(file: bytes, filename: str) -> dict:
    try:
        response = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            filename,
            file
        )
        return response
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise e


def get_public_resume_url(filename: str) -> str:
    response = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(filename)
    return response
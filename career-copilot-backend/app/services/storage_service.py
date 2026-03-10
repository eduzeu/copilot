from supabase import create_client, Client
from app.core.config import settings

supabase: Client = create_client(settings.STORAGE_KEY_PUBLIC, settings.STORAGE_KEY_SECRET)

def upload_resume(file: bytes, filename: str) -> dict: 
    """Uploads a resume to Supabase storage."""
    try: 
        response = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(filename, file)
        if response.get('error'):
            raise Exception(response['error']['message'])
        return response
    except Exception as e: 
        print(f"Error uploading file: {e}")
        raise e
  
def get_resume_url(filename: str) -> str:
  """Generates a public URL for a stored resume."""
  try: 
      url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(filename)
      return url['publicURL']
  except Exception as e: 
      print(f"Error generating URL: {e}")
      raise e
  
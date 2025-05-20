import os
import django
from dotenv import load_dotenv

# Load the .env file BEFORE anything else
load_dotenv()

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vintage.settings")  # replace with your actual project name
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File

MEDIA_ROOT = settings.MEDIA_ROOT

for root, dirs, files in os.walk(MEDIA_ROOT):
    for filename in files:
        filepath = os.path.join(root, filename)
        relative_path = os.path.relpath(filepath, MEDIA_ROOT)
        print(f"Uploading: {relative_path}")
        with open(filepath, 'rb') as f:
            file = File(f)
            default_storage.save(relative_path, file)

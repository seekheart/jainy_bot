import os

DALLE_API_URL = os.environ.get('DALLE_API_URL')

if not DALLE_API_URL:
    raise AttributeError('DALLE_API_URL environment variable not set!')

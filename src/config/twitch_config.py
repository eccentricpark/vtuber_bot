import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

def get_twitch_access_token():
  return os.getenv("TWITCH_ACCESS_TOKEN")
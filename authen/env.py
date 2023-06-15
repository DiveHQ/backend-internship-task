"""import os
import dotenv # <- New
from dotenv import load_dotenv
# Add .env variables anywhere before SECRET_KEY
dotenv_file = os.path.join( "E:\Projects\django\CalorieHD", ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# UPDATE secret key
SECRET_KEY = os.environ['API_KEY']"""

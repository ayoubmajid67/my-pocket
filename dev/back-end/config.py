import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = 'data/profiles'
    ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4'}
    API_VERSION = 'v1'

    SQLALCHEMY_DATABASE_URI = os.getenv('AYOUB_DB_CNX')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    

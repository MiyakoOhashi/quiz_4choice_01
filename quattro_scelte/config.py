# quattro_scelte/config.py        2022/04/25  M.O
import os
# import psycopg2

# postgresql設定
# DATABASE_URL = os.environ('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# if postgres_uri.startswith("postgres://"):
#     postgres_uri = postgres_uri.replace("postgres://", "postgresql://", 1)

# sqlite(local用)設定
basedir = os.path.abspath(os.path.dirname(__name__))
sqlite_uri = "sqlite:///" + os.path.join(basedir, 'data.sqlite')


# SQLALCHEMY_DATABASE_URI = postgres_uri or sqlite_uri
SQLALCHEMY_DATABASE_URI = sqlite_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# os.urandom(24)
SECRET_KEY = b'81\xf2\xd3u^\x8f\xc6I\x93\xa5\x18\\7\x14\xac\xddv\xbbd{V^\x86'

DEBUG = False
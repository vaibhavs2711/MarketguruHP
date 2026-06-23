import os
from urllib.parse import urlparse

mysql_url = os.environ.get("MYSQLURL") or os.environ.get("DATABASE_URL")

if mysql_url and (mysql_url.startswith("mysql://") or mysql_url.startswith("mysqls://")):
    url = urlparse(mysql_url)
    DB_HOST = url.hostname
    DB_PORT = url.port or 3306
    DB_USER = url.username
    DB_PASSWORD = url.password
    DB_NAME = url.path.lstrip('/')
else:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
    DB_NAME = os.environ.get("DB_NAME", "marketguruhp")

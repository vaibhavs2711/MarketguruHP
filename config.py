import os
from urllib.parse import urlparse

mysql_url = os.environ.get("MYSQL_PUBLIC_URL") or os.environ.get("MYSQLURL") or os.environ.get("DATABASE_URL")

if mysql_url and (mysql_url.startswith("mysql://") or mysql_url.startswith("mysqls://")):
    url = urlparse(mysql_url)
    DB_HOST = url.hostname
    DB_PORT = url.port or 3306
    DB_USER = url.username
    DB_PASSWORD = url.password
    DB_NAME = url.path.lstrip('/')
else:
    # First check Railway's standard MYSQL... variables
    DB_HOST = os.environ.get("MYSQLHOST") or os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("MYSQLPORT") or os.environ.get("DB_PORT", 3306))
    DB_USER = os.environ.get("MYSQLUSER") or os.environ.get("DB_USERNAME") or os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("MYSQLPASSWORD") or os.environ.get("DB_PASSWORD", "root")
    DB_NAME = os.environ.get("MYSQLDATABASE") or os.environ.get("DB_DATABASE") or os.environ.get("DB_NAME", "marketguruhp")

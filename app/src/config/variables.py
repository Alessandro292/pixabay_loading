import os

# Minio variables
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_USER = os.getenv('MINIO_USER', 'minioadmin')
MINIO_PASSWORD = os.getenv('MINIO_PASSWORD', 'minioadmin')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'sink')

# MYSql variables
MYSQL_SERVER = os.getenv('MYSQL_SERVER', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_DB = os.getenv('MYSQL_DB', 'db')

# Pixabay variables
PIXABAY_URL = os.getenv('PIXABAY_URL', 'https://pixabay.com/api/')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '<YOUR_API_KEY>')
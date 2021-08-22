import os

BASE_DIR = os.path.dirname(__file__)

HTACCESS_INIT_CONTENT = """php_value upload_max_filesize 512M
php_value post_max_size 512M
php_value memory_limit 512M

# BEGIN WordPress

RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]

# END WordPress
"""

OUTPUT_BUILD_DIR = f"{BASE_DIR}/build"
DOCKER_COMPOSE_JINJA_FOLDER = f"{BASE_DIR}/docker"

DOCKER_COMPOSE_JINJA_DATABASE = "docker-compose-database.jinja"
DOCKER_COMPOSE_JINJA_WORDPRESS = "docker-compose-wordpress.jinja"
DOCKER_COMPOSE_DATABASE_FILENAME = "docker-compose-database.yml"
DOCKER_COMPOSE_WORDPRESS_FILENAME_UNFORMATTED = "docker-compose-{}.yml"
DATABASE_KEY_FILENAME = "database_key.json"
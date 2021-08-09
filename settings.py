import os

BASE_DIR = os.path.dirname(__file__)

OUTPUT_BUILD_DIR = f"{BASE_DIR}/build"
DOCKER_COMPOSE_JINJA_FOLDER = f"{BASE_DIR}/docker"

DOCKER_COMPOSE_JINJA_DATABASE = "docker-compose-database.jinja"
DOCKER_COMPOSE_JINJA_WORDPRESS = "docker-compose-wordpress.jinja"
DOCKER_COMPOSE_DATABASE_FILENAME = "docker-compose-database.yml"
DOCKER_COMPOSE_WORDPRESS_FILENAME_UNFORMATTED = "docker-compose-{}.yml"
DATABASE_KEY_FILENAME = "database_key.json"
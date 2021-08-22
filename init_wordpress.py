import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings import DOCKER_COMPOSE_JINJA_FOLDER,\
    OUTPUT_BUILD_DIR,\
    DOCKER_COMPOSE_JINJA_WORDPRESS,\
    DOCKER_COMPOSE_WORDPRESS_FILENAME_UNFORMATTED,\
    DATABASE_KEY_FILENAME,\
    HTACCESS_INIT_CONTENT
import json

def main():
    wordpress_domain = ""
    wordpress_port   = ""

    env = Environment(
        loader=FileSystemLoader(DOCKER_COMPOSE_JINJA_FOLDER),
        autoescape=select_autoescape()
    )

    while not wordpress_domain:
        wordpress_domain    = input("Type the domain of your WordPress site: ")

    while not wordpress_port:
        wordpress_port      = input("Type the WordPress docker port: ")

    DOCKER_COMPOSE_WORDPRESS_FILENAME = DOCKER_COMPOSE_WORDPRESS_FILENAME_UNFORMATTED.format(wordpress_domain)

    with open(f"{OUTPUT_BUILD_DIR}/{DATABASE_KEY_FILENAME}", "r") as database_key_file:
        database_key = json.loads(database_key_file.read())

    wordpress_table_prefix = wordpress_domain.replace(".", "_")
    wordpress_service_name = f"wordpress_{wordpress_table_prefix}"
    wordpress_base_folder = wordpress_domain
    
    docker_compose_content_dict = {
        "wordpress_port": wordpress_port,
        "wordpress_table_prefix": wordpress_table_prefix,
        "wordpress_service_name": wordpress_service_name,
        "wordpress_base_folder": wordpress_base_folder,
        **database_key
    }

    docker_compose_content = env.get_template(f"{DOCKER_COMPOSE_JINJA_WORDPRESS}")
    docker_compose_content = docker_compose_content.render(docker_compose_content_dict)

    with open(f"{OUTPUT_BUILD_DIR}/{DOCKER_COMPOSE_WORDPRESS_FILENAME}", "w") as docker_compose_file:
        docker_compose_file.write(docker_compose_content)

    os.system(f"docker-compose -f {OUTPUT_BUILD_DIR}/{DOCKER_COMPOSE_WORDPRESS_FILENAME} up -d")

if __name__ == "__main__":
    main()
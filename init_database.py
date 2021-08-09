import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings import DOCKER_COMPOSE_JINJA_FOLDER,\
    OUTPUT_BUILD_DIR,\
    DOCKER_COMPOSE_JINJA_DATABASE,\
    DOCKER_COMPOSE_DATABASE_FILENAME,\
    DATABASE_KEY_FILENAME
import json

def main():
    mysql_root_password = ""
    mysql_database      = ""
    mysql_user          = ""
    mysql_password      = ""

    env = Environment(
        loader=FileSystemLoader(DOCKER_COMPOSE_JINJA_FOLDER),
        autoescape=select_autoescape()
    )

    while not mysql_root_password:
        mysql_root_password = input("Type the MySQL root password: ")

    while not mysql_database:
        mysql_database      = input("Type the MySQL database name: ")

    while not mysql_user:
        mysql_user          = input("Type the MySQL user: ")

    while not mysql_password:
        mysql_password      = input("Type the MySQL password: ")

    docker_compose_content_dict = {
        "mysql_root_password": mysql_root_password,
        "mysql_database": mysql_database,
        "mysql_user": mysql_user,
        "mysql_password": mysql_password,
    }
    docker_compose_content = env.get_template(f"{DOCKER_COMPOSE_JINJA_DATABASE}")
    docker_compose_content = docker_compose_content.render(docker_compose_content_dict)

    if not os.path.exists(OUTPUT_BUILD_DIR):
        os.makedirs(OUTPUT_BUILD_DIR)

    with open(f"{OUTPUT_BUILD_DIR}/{DOCKER_COMPOSE_DATABASE_FILENAME}", "w") as docker_compose_file:
        docker_compose_file.write(docker_compose_content)
        
    with open(f"{OUTPUT_BUILD_DIR}/{DATABASE_KEY_FILENAME}", "w") as database_key_file:
        database_key_content = json.dumps(docker_compose_content_dict)
        database_key_file.write(database_key_content)

    os.system(f"docker-compose -f {OUTPUT_BUILD_DIR}/{DOCKER_COMPOSE_DATABASE_FILENAME} up -d")

if __name__ == "__main__":
    main()
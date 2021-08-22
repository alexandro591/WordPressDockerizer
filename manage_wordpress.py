import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings import JINJA_FOLDER,\
    OUTPUT_BUILD_DIR,\
    DOCKER_COMPOSE_JINJA_WORDPRESS,\
    DOCKER_COMPOSE_WORDPRESS_FILENAME_UNFORMATTED,\
    DATABASE_KEY_FILENAME,\
    HTACCESS_INIT_CONTENT,\
    NGINX_JINJA_SERVERNAME
import json

def main():
    wordpress_domain : str = ""
    wordpress_port   : str = ""
    include_www      : str = ""

    env = Environment(
        loader=FileSystemLoader(JINJA_FOLDER),
        autoescape=select_autoescape()
    )

    while not wordpress_domain:
        wordpress_domain = input("Type the domain of your WordPress site: ").replace("www", "")

    wordpress_domains = f"{wordpress_domain} www.{wordpress_domain}"
    
    while not wordpress_port:
        wordpress_port   = input("Type the WordPress docker port: ")
    
    while include_www != "n" and include_www != "y":
        include_www      = input("Should we include www in the nginx conf?: ")
        if include_www == "n":
            wordpress_domains = wordpress_domain

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
        "wordpress_domains": wordpress_domains,
        **database_key
    }

    docker_compose_content = env.get_template(f"{DOCKER_COMPOSE_JINJA_WORDPRESS}")
    docker_compose_content = docker_compose_content.render(docker_compose_content_dict)
    
    nginx_content = env.get_template(f"{NGINX_JINJA_SERVERNAME}")
    nginx_content = nginx_content.render(docker_compose_content_dict)

    os.mkdir(f"{OUTPUT_BUILD_DIR}/{wordpress_domain}")
    os.mkdir(f"{OUTPUT_BUILD_DIR}/{wordpress_domain}/data")

    with open(f"{OUTPUT_BUILD_DIR}/{wordpress_domain}/{DOCKER_COMPOSE_WORDPRESS_FILENAME}", "w") as docker_compose_file:
        docker_compose_file.write(docker_compose_content)
    
    with open(f"{OUTPUT_BUILD_DIR}/{wordpress_domain}/{wordpress_domain}.conf", "w") as nginx_file:
        nginx_file.write(nginx_content)
        
    with open(f"{OUTPUT_BUILD_DIR}/{wordpress_domain}/.htaccess", "w") as htaccess_file:
        htaccess_file.write(HTACCESS_INIT_CONTENT)

    os.system(f"docker-compose -f {OUTPUT_BUILD_DIR}/{wordpress_domain}/{DOCKER_COMPOSE_WORDPRESS_FILENAME} up -d --build")

if __name__ == "__main__":
    main()
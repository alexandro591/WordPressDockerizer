import os
import sys
from settings import OUTPUT_BUILD_DIR

def main():
  os.system("sudo apt install nginx")
  os.system("sudo apt install certbot")
  os.system("sudo apt install python3-certbot-nginx")

  action            : str = ""
  wordpress_domain  : str = ""
  include_www       : str = ""
  
  while action != "start" and action != "stop":
    action              = input("Type the action you want to take (start/stop): ")

  while not wordpress_domain:
    wordpress_domain    = input("Type the wordpress domain that is going to be affected: ")
    wordpress_domain    = wordpress_domain.replace("www", "")

  nginx_domain_action   =  f"-d {wordpress_domain}"
  
  while include_www != "y" and include_www != "n" and action == "start":
    include_www         = input("Should we include www in SSL certificate? (y/n): ")

  if include_www == "y":
    nginx_domain_action = f"-d {wordpress_domain} -d www.{wordpress_domain}"  

  if action == "start":
    os.system(f"sudo cp {OUTPUT_BUILD_DIR}/{wordpress_domain}/{wordpress_domain}.conf /etc/nginx/conf.d/")
    os.system(f"sudo certbot --nginx {nginx_domain_action}")

  if action == "stop":
    os.system(f"sudo rm /etc/nginx/conf.d/{wordpress_domain}.conf")

  os.system(f"sudo service nginx restart")
  
if __name__ == "__main__":
  main()
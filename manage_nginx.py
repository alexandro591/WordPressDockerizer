import os
import sys
from settings import OUTPUT_BUILD_DIR

os.system("sudo apt install nginx")
os.system("sudo apt install certbot")
os.system("sudo apt install python3-certbot-nginx")

action = sys.argv[1]
wordpress_domain = sys.argv[2].replace("www", "")
include_www = sys.argv[3] if len(sys.argv) > 3 else None

if action == "init" or action == "start":
  os.system(f"sudo cp {OUTPUT_BUILD_DIR}/{wordpress_domain}/{wordpress_domain}.conf /etc/nginx/conf.d/")
  nginx_domain_action =  f"-d {wordpress_domain}"
  if include_www == "--include-www":
    nginx_domain_action = f"-d {wordpress_domain} -d www.{wordpress_domain}"  
  os.system(f"sudo certbot --nginx {nginx_domain_action}")

if action == "stop":
  os.system(f"sudo rm /etc/nginx/conf.d/{wordpress_domain}.conf")

os.system(f"sudo service nginx restart")
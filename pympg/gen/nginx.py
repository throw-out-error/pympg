from re import S
from urllib.parse import urlparse
import os
from typing import Union, Literal
from .main import ConfigGenerator


class NginxConfigGenerator(ConfigGenerator):
    def __init__(
        self,
        domains: str = "example.com",
        web_root: Union[bool, str] = False,
        uri_to_forward: Union[Literal[False], str] = False,
        nginx_path: str = "/etc/nginx",
    ):
        self.domains = domains.split(",")
        self.web_root = web_root
        self.forward_uri = uri_to_forward
        self.nginx_path = nginx_path

    def generate(self):
        domain = self.domains[0]
        server_alias = " ".join(list(self.domains[1:])) or ""

        if self.forward_uri and self.forward_uri.strip() == "":
            self.forward_uri = "localhost"

        if self.forward_uri != "" and not urlparse(self.forward_uri).scheme in {
            "http",
            "https",
        }:
            self.forward_uri = f"http://{self.forward_uri}"

        config = (
            "server {\n"
            f"   listen 80;\n"
            f"   server_name {domain} {server_alias};\n"
        )
        if self.web_root != "":
            config += f"   root {self.web_root};\n"
        config += (
            "   location / {\n"
            f"       proxy_pass {self.forward_uri};\n"
            "       proxy_set_header Host $http_host;\n"
            "    }\n"
            if self.forward_uri != ""
            else ""
        )
        config += "}\n"
        sites_dir = f"{self.nginx_path}/sites-available"
        if not os.path.exists(sites_dir):
            os.makedirs(sites_dir)
        f = open(f"{sites_dir}/{domain}.conf", "w")
        f.write(config)
        f.close()
        # Enable site
        enabled_sites_dir = f"{self.nginx_path}/sites-enabled"
        if not os.path.exists(enabled_sites_dir):
            os.makedirs(enabled_sites_dir)
        if not os.path.exists(f"{enabled_sites_dir}/{domain}.conf"):
            os.link(
                f"{sites_dir}/{domain}.conf",
                f"{enabled_sites_dir}/{domain}.conf",
            )

        self.reload()

    def reload(self):
        # Reload nginx
        if os.name == "nt":
            # Do nothing for windows, may be resolved in the future
            pass
        else:
            os.system("sudo systemctl restart nginx")

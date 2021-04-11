from urllib.parse import urlparse
import os
from typing import Union, Literal
from .main import ConfigGenerator

APACHE_LOG_DIR = "${APACHE_LOG_DIR}"


class ApacheConfigGenerator(ConfigGenerator):
    def __init__(
        self,
        domains: str = "example.com",
        web_root: Union[bool, str] = False,
        uri_to_forward: Union[Literal[False], str] = False,
        apache_path: str = "/etc/apache2",
    ):
        self.domains = domains.split(",")
        self.web_root = web_root
        self.forward_uri = uri_to_forward
        self.apache_path = apache_path

    def generate(self):

        domain = self.domains[0]
        server_alias = "".join(list([f"{d} " for d in self.domains[1:]]))

        if self.forward_uri and self.forward_uri.strip() == "":
            self.forward_uri = "localhost"

        if self.forward_uri != "" and not urlparse(self.forward_uri).scheme in {
            "http",
            "https",
        }:
            self.forward_uri = f"http://{self.forward_uri}"

        config = (
            "<VirtualHost *:80>"
            f"ServerName {domain}"
            f"ServerAlias {server_alias}"
            if server_alias
            else f"DocumentRoot {self.web_root}"
            if self.web_root != ""
            else ""
            f"ProxyPass / {self.web_root}/ \nProxyPassReverse / {self.forward_uri}/"
            if self.forward_uri != ""
            else ""
            "ErrorLog {APACHE_LOG_DIR}/error.log"
            "CustomLog {APACHE_LOG_DIR}/access.log combined"
            "</VirtualHost>"
        )
        sites_dir = f"{self.apache_path}/sites-available"
        if not os.path.exists(sites_dir):
            os.makedirs(sites_dir)
        f = open(f"{sites_dir}/{domain}.conf", "w")
        f.write(config)
        f.close()
        self.reload()

    def reload(self):
        # Reload apache
        if os.name == "nt":
            os.system("httpd -k graceful")
        else:
            domains = " ".join(self.domains)
            os.system("a2enmod proxy")
            os.system("a2enmod proxy_http")
            os.system(f"a2ensite {domains}")
            os.system("sudo apachectl -k graceful")

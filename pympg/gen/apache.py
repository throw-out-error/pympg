from urllib.parse import urlparse
import os
from shutil import copyfile
from typing import Union, Literal
from .main import ConfigGenerator

APACHE_LOG_DIR = "${APACHE_LOG_DIR}"


class ApacheConfigGenerator(ConfigGenerator):
    def generate(
        self,
        domains: str = "example.com",
        web_loc: bool = False,
        uri_to_forward: Union[Literal[False], str] = False,
        apache_path: str = "/etc/apache2",
    ):
        domainAnswer = domains.split(",")
        domain = domainAnswer[0]
        server_alias = "".join(list([f"{d} " for d in domainAnswer[1:]]))

        if uri_to_forward and uri_to_forward.strip() == "":
            uri_to_forward = f"localhost"

        if uri_to_forward != "" and not urlparse(uri_to_forward).scheme in {
            "http",
            "https",
        }:
            uri_to_forward = f"http://{uri_to_forward}"

        config = f"""
            <VirtualHost *:80>
            ServerName {domain}
            {f"ServerAlias {server_alias}" if server_alias else ""}
            {f"DocumentRoot {web_loc}" if web_loc != "" else ""}
            {"ProxyPass / {uri_to_forward}/ ProxyPassReverse / {uri_to_forward}/" if uri_to_forward != "" else ""}
            ErrorLog {APACHE_LOG_DIR}/error.log
            CustomLog {APACHE_LOG_DIR}/access.log combined
            </VirtualHost>
            """
        sites_dir = f"{apache_path}/sites-enabled"
        if not os.path.exists(sites_dir):
            os.makedirs(sites_dir)
        f = open(f"{domain}.conf", "w")
        f.write(config)
        f.close()
        copyfile(f"{domain}.conf", f"{sites_dir}/{domain}.conf")
        self.reload()

    def reload(_):
        # Reload apache
        if os.name == "nt":
            os.system("httpd -k graceful")
        else:
            os.system("sudo apachectl -k graceful")

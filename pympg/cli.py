#!/usr/bin/env python
# encoding: utf-8

from pympg.gen.nginx import NginxConfigGenerator
from pympg.gen.main import ConfigGenerator
import questionary
from prompt_toolkit.styles import Style
from .gen.apache import ApacheConfigGenerator
from sys import exit

style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#2e82c7 bg:#d9d9d9"),
        ("pointer", "fg:#FF9D00 bold"),
        ("answer", "fg:#2e9dd1 bold bg:#363636"),
    ]
)


def main():
    generator: str = questionary.select(
        "What do you want to generate?",
        choices=["Apache Config", "Nginx Config"],
        style=style,
    ).ask()

    gen: ConfigGenerator = None

    if generator == "Apache Config":
        apache_path: str = questionary.path(
            "Where is apache2 located?",
            default="/etc/apache2",
            style=style,
        ).ask()
        if apache_path is None:
            print("Failed to generate: missing apache path!")
            exit(1)

        domains: str = questionary.text(
            "What domains to you want to serve? (Seperated by commas)",
            default="example.com",
            style=style,
        ).ask()
        if domains is None:
            print("Failed to generate: missing domain(s)!")
            exit(1)

        web_loc = questionary.path(
            "What is the path of your website files? (Optional)",
            default="",
            style=style,
        ).ask()
        if web_loc is None:
            print("Failed to generate: missing webroot!")
            exit(1)

        uri_to_forward = questionary.text(
            "What URI do you want to proxy to? (Optional)",
            default="",
            style=style,
        ).ask()
        if uri_to_forward is None:
            print("Failed to generate: missing proxy URI!")
            exit(1)

        if apache_path != "" and domains != "":
            gen = ApacheConfigGenerator(
                apache_path=apache_path,
                domains=domains,
                uri_to_forward=uri_to_forward,
                web_root=web_loc,
            )
            gen.generate()
        else:
            print("Failed to generate: missing answers!")
    elif generator == "Nginx Config":
        nginx_path: str = questionary.path(
            "Where is nginx located?",
            default="/etc/nginx",
            style=style,
        ).ask()
        if nginx_path is None:
            print("Failed to generate: missing apache path!")
            exit(1)

        domains: str = questionary.text(
            "What domains to you want to serve? (Seperated by commas)",
            default="example.com",
            style=style,
        ).ask()
        if domains is None:
            print("Failed to generate: missing domain(s)!")
            exit(1)

        web_loc = questionary.path(
            "What is the path of your website files? (Optional)",
            default="",
            style=style,
        ).ask()
        if web_loc is None:
            print("Failed to generate: missing webroot!")
            exit(1)

        uri_to_forward = questionary.text(
            "What URI do you want to proxy to? (Optional)",
            default="",
            style=style,
        ).ask()
        if uri_to_forward is None:
            print("Failed to generate: missing proxy URI!")
            exit(1)

        if nginx_path != "" and domains != "":
            gen = NginxConfigGenerator(
                nginx_path=nginx_path,
                domains=domains,
                uri_to_forward=uri_to_forward,
                web_root=web_loc,
            )
            gen.generate()
        else:
            print("Failed to generate: missing answers!")
    elif generator == "UFW Firewall":
        # TODO: fix this
        """gen = UfwConfigGenerator()

        allowDeny = questionary.select(
            "Would you like to accept or deny a port?",
            choices=["Allow", "Deny"],
            style=style,
        ).ask()
        port = questionary.text(
            "What port would you like to allow/deny?", style=style
        ).ask()
        if allowDeny is None:
            print("Failed to generate: you did not choose to allow/deny a port.")
            exit(1)
        if port is None:
            print("Failed to generate: Missing port")
            exit(1)
        if allowDeny != "" and port != "":
            gen.generate(port, accept=True if allowDeny == "Allow" else False)
        else:
            print("Failed to generate: missing answers!")"""
    else:
        print("Nothing to generate, exiting...")

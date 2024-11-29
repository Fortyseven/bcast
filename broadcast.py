#!/usr/bin/env python3

import json
import os
import argparse
from rich import print

from channels.channel import Channel
from channels.services.bluesky import BlueSky
from channels.services.facebook import Facebook
from channels.services.mastodon import Mastodon

channel_classes = {
    "mastodon": Mastodon,
    "bluesky": BlueSky,
    "facebook": Facebook,
}


def load_template(template_file):
    # confirm config file exists

    if not os.path.exists(template_file):
        print(f"[red]Template file not found: `{template_file}`[/red]")

    # config is in json

    with open(template_file) as f:
        config = json.load(f)

    return config


def get_var(kn: str, template, args: argparse.Namespace):
    # command line override > template.variables > None

    if args.var:
        for var in args.var:
            key, value = var.split("=")
            if kn == key:
                return value

    tvars = template.get("variables")
    if tvars:
        for k, v in iter(tvars.items()):
            if kn == k:
                return v

    return None


def main():
    parser = argparse.ArgumentParser(description="Broadcast a message to all users")
    parser.add_argument("template", help="Template for broadcast")

    parser.add_argument("-v", "--var", action="append", help="Set a template variable")

    args = parser.parse_args()

    # validate args.var entries are in the form of key=value
    if args.var:
        for var in args.var:
            if "=" not in var:
                parser.error(
                    f"Invalid varirable: {var}; must be in the form 'key=value'"
                )

    template = load_template(args.template)

    # find all of the unique {{keyword}} values in the template.message

    keywords = dict()

    for keyword in template["message"].split("{{"):
        required = False
        if "}}" in keyword:
            kn = keyword.split("}}")[0]

            if keyword[0] == "!":
                required = True
                kn = keyword.split("}}")[0][1:]
                # kn = kn[1:]

            var = get_var(kn, template, args)  # .get(kn, None)

            if var and required is None:
                raise f"Missing required variable: {kn}"

            keywords.setdefault(kn, var)

    for kw in keywords:
        template["message"] = template["message"].replace(
            "{{" + kw + "}}",
            keywords[kw] or "",
        )
        template["message"] = template["message"].replace(
            "{{!" + kw + "}}",
            keywords[kw] or "",
        )

    for channel_config_path in template["channels"]:
        with open(channel_config_path) as f:
            print("-----------------------")
            channel_config = json.load(f)

            service_class = channel_classes[channel_config["name"]]

            channel = service_class(channel_config, args)

            try:
                media_path = None

                if template.get("media_path"):
                    media_path = template.get("media_path")
                    print(f" Have media: {media_path}")
                    channel.broadcast(template.get("message"), [media_path])
                else:
                    channel.broadcast(template.get("message", ""))
            except Exception as e:
                print(
                    "[red]Error broadcasting message to: "
                    + channel_config.get("name")
                    + "[/red] : "
                    + str(e)
                )


if __name__ == "__main__":
    main()

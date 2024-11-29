from datetime import datetime, timezone
from channels.channel import Channel
import requests


def bsky_login_session(pds_url: str, handle: str, password: str) -> dict:
    resp = requests.post(
        pds_url + "/xrpc/com.atproto.server.createSession",
        json={"identifier": handle, "password": password},
    )
    resp.raise_for_status()
    return resp.json()


def bsky_post(session: dict, pds_url: str, message: str, embed: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    post = {
        "$type": "app.bsky.feed.post",
        "text": message,
        "createdAt": now,
    }

    if embed:
        post["embed"] = embed

    print(post)

    resp = requests.post(
        pds_url + "/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        json={
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": post,
        },
    )


def bsky_upload_file(pds_url, access_token, filename, img_bytes) -> dict:
    suffix = filename.split(".")[-1].lower()
    mimetype = "application/octet-stream"
    if suffix in ["png"]:
        mimetype = "image/png"
    elif suffix in ["jpeg", "jpg"]:
        mimetype = "image/jpeg"
    elif suffix in ["webp"]:
        mimetype = "image/webp"

    # WARNING: a non-naive implementation would strip EXIF metadata from JPEG files here by default
    resp = requests.post(
        pds_url + "/xrpc/com.atproto.repo.uploadBlob",
        headers={
            "Content-Type": mimetype,
            "Authorization": "Bearer " + access_token,
        },
        data=img_bytes,
    )
    resp.raise_for_status()
    return resp.json()["blob"]


class BlueSky(Channel):
    def __init__(self, config, args):
        super().__init__(config, args)
        self.validate_config()

        self.session = bsky_login_session(
            self.config["pds_url"],
            self.config["handle"],
            self.config["password"],
        )

    def validate_config(self):
        required_keys = ["pds_url", "handle", "password"]

        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

    def broadcast(self, message: str, media_list: set = None):
        if media_list is not None:
            # TODO: allow multiple media files
            media_path = media_list.pop()

            print(f"- Sending media")

            blob = bsky_upload_file(
                self.config["pds_url"],
                self.session["accessJwt"],
                media_path,
                open(media_path, "rb").read(),
            )

            images = {
                "$type": "app.bsky.embed.images",
                "images": [{"alt": "", "image": blob}],
            }

            bsky_post(self.session, self.config["pds_url"], message, embed=images)
        else:
            bsky_post(self.session, self.config["pds_url"], message)

        print(f"- Sent to BlueSky.")

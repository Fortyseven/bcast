from channels.channel import Channel

from mastodon import Mastodon as MastodonAPI


class Mastodon(Channel):
    def __init__(self, config, args):
        super().__init__(config, args)
        self.validate_config()
        self.mastodon = MastodonAPI(
            access_token=self.config["access_token"],
            api_base_url=self.config["api_base_url"],
        )

    def validate_config(self):
        required_keys = ["access_token", "api_base_url"]

        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

    def broadcast(self, message: str, media_list: set = None):
        if media_list is not None:
            print(media_list)
            media_path = media_list.pop()

            print(f"- Sending media to Mastodon: {media_path}")
            media_id = self.mastodon.media_post(media_file=media_path)

            self.mastodon.status_post(
                status="Automated test toot!", media_ids=[media_id]
            )
        else:
            self.mastodon.toot("Automated test toot w/o media!")

        print(f"- Sent to Mastodon.")

from channels.channel import Channel


class Facebook(Channel):
    def __init__(self, config, args):
        super().__init__(config, args)
        self.validate_config()

    def validate_config(self):
        required_keys = []

        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

    def broadcast(self, message: str, media: set = None):
        print(f"- Sent to Facebook")

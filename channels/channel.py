from abc import abstractmethod, ABCMeta
import os
import json


class Channel:
    __metaclass__ = ABCMeta

    def __init__(self, config, args):
        self.config = config
        self.args = args

    @abstractmethod
    def validate_config(self):
        pass

    @abstractmethod
    def broadcast(self, message: str, media: set = None):
        print(f"Broadcasting message: {message} / {media}")

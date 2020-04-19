""" Run the script with command line arguments """
from CryptoSentWebApp.media.reddit_upstream import Upstream
from CryptoSentWebApp import config


class Runner:
    """ Class to configure and run the application """
    def __init__(self, reddit_secrets_path: str):
        self.reddit_api_secrets = config.get_secret(reddit_secrets_path)

    def run(self):
        kinesis_upstream = Upstream(self.reddit_api_secrets)
        kinesis_upstream.run_upstream()

""" Data upstream channel to kinesis """
import praw
import boto3
import time

from CryptoSentWebApp import constants
from CryptoSentWebApp.objects import RedditComment


class Upstream:
    """ Kinesis upstream streaming the Reddit comment stream """
    def __init__(self, reddit_api_secrets):
        reddit_connection = praw.Reddit(
            client_id=reddit_api_secrets['client_id'],
            client_secret=reddit_api_secrets['client_secret'],
            username=reddit_api_secrets['username'],
            password=reddit_api_secrets['password'],
            user_agent=reddit_api_secrets['user_agent']
        )
        self.subreddit_connection = reddit_connection.subreddit(constants.SUBREDDIT)
        self.kinesis = boto3.client('kinesis')

    def run_upstream(self):
        """"""
        for comment in self.subreddit_connection.stream.comments(skip_existing=True):
            reddit_comment = RedditComment(comment)
            records = reddit_comment.get_records()
            print(records)
            self.kinesis.put_records(StreamName=constants.UPSTREAM_NAME, Records=records)
            time.sleep(0.1)

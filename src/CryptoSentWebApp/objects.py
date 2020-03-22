""" Streaming objects """
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
from praw.models import Comment
import json

from CryptoSentWebApp.constants import COINLIST
sid = SentimentIntensityAnalyzer()


class RedditComment:
    """ Class containing Reddit comment information """
    def __init__(self, comment: Comment):
        self.comment_id = comment.id
        self.author = comment.author.id
        self.link = comment.link_id
        self.body = comment.body
        self.ts = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')

    def get_records(self):
        records = []
        for sent in tokenize.sent_tokenize(self.body):
            for record in self.get_record(sent):
                records += [record]
        return records

    def get_record(self, sent):
        senti = sid.polarity_scores(sent)['compound']
        words = tokenize.word_tokenize(sent)
        subjects = set()
        for word in words:
            if word in COINLIST.keys() or word.upper() in COINLIST.keys():
                subjects.add(COINLIST[word.upper()])
            elif word in COINLIST.values() or word.capitalize() in COINLIST.values():
                subjects.add(word.capitalize())

        records = []
        output = {
            'Id': self.comment_id,
            'Event_ts': self.ts,
            'Author': self.author,
            'Link': self.link,
            'Sentence': sent,
            'Sentiment': senti,
        }
        if subjects:
            for subject in subjects:
                output['Subject'] = subject
                data = json.dumps(output)
                records += [{'Data': bytes(data, 'utf-8'), 'PartitionKey': 'partition_key'}]
        else:
            output['Subject'] = 'Other'
            data = json.dumps(output)
            records += [{'Data': bytes(data, 'utf-8'), 'PartitionKey': 'partition_key'}]
        return records



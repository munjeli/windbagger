import twitter
import cfg
import os
import json
import logging

fmt = "%(levelname)s\t%(funcName)s():%(lineno)i\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)


def fetch_twitter_creds():
    """
    read the file for our keys and such
    :return:
    """
    try:
        cred_path = os.path.join(cfg.windbagger_data, 'credentials.json')
        return json.load(open(cred_path, 'r'))
    except IOError as e:
        logger.critcal('Credentials for twitter not found!')


def fetch_latest(twitter_id):
    creds = fetch_twitter_creds()
    logger.debug("TWITTER: {}".format(twitter_id))
    api = twitter.Api(
        consumer_key=creds['consumer_key'],
        consumer_secret=creds['consumer_secret'],
        access_token_key=creds['access_key'],
        access_token_secret=creds['access_secret']
    )
    try:
        tweets = api.GetUserTimeline(screen_name=twitter_id, count=3)
        logger.debug(tweets)
        return tweets
    except Exception as e:
        logger.warning(e)
        pass

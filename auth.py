import tweepy

api_key = 'kqotO6Y1lW8GWUKv2bxLNcBSU'
api_secret = 'sDxTFwDpWD3ths2K10rPeC8qiZMz9wQu1P4ysJwyWVPLVuwUgy'
access_token = '1702651293892845568-jVLJV8XENvl2kfxEipCDMRMiHbY8bS'
access_token_secret = '0MGJEUkjoErjwubIyZTE2gTD9fzhfdT8lk3fZkAgY0v8b'


def get_twitter_conn_v1() -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2() -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client
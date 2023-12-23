import tweepy , json
from github import Github


from auth import get_twitter_conn_v1, get_twitter_conn_v2

g = Github('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')

client_v1 = get_twitter_conn_v1()
client_v2 = get_twitter_conn_v2()

# Replace these with your Twitter API credentials
consumer_key = 'kqotO6Y1lW8GWUKv2bxLNcBSU'
consumer_secret = 'sDxTFwDpWD3ths2K10rPeC8qiZMz9wQu1P4ysJwyWVPLVuwUgy'
access_token = '1702651293892845568-jVLJV8XENvl2kfxEipCDMRMiHbY8bS'
access_token_secret = '0MGJEUkjoErjwubIyZTE2gTD9fzhfdT8lk3fZkAgY0v8b'

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create an API object
api = tweepy.API(auth)
client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)

def post_tweet(text):
    try:
        client.create_tweet(text=text)
        print("Tweet posted successfully!")
    except tweepy.TwitterServerError as e:
        print(f"Error: {e}")


def post_tweet_wImages(text,media_path):
    try:

        mediapath = media_path
        media = client_v1.media_upload(filename=mediapath)
        media_id = media.media_id

        client_v2.create_tweet(text=text, media_ids=[media_id])

        print("Tweet posted successfully!")
    except tweepy.TwitterServerError as e:
        print(f"Error: {e}")




if __name__ == "__main__":
    tweet_text = "Hello, Python and 9o990.  #TwitterAPI"
    post_tweet(tweet_text) 
    #post_tweet_wImages(tweet_text,"./images/image3.jpg")



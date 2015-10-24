#!/usr/bin/env python
import os
import sys
import encoding_fix
import tweepy

from twitter_authentication import CONSUMER_KEY, ACCESS_TOKEN

def auth(consumer_secret, access_token_secret):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, consumer_secret)
    auth.set_access_token(ACCESS_TOKEN, access_token_secret)
    return auth

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print(tweet._json)

    def on_error(self, status_code):
        print( 'Error: ' + repr(status_code))
        if status_code == 420:
            # sleep for a minute to back off.
            import time
            print("Backing off.")
            time.sleep(60 * 2) # sleep for 2 mins.
        elif 400 <= status_code < 500:
            print("Bailing due to {}".format(status_code))
            sys.exit(1)

        return False


def main():
    consumer_secret, access_token_secret = os.environ['CONSUMER_SECRET'], os.environ['ACCESS_TOKEN_SECRET']
    api_auth = auth(consumer_secret, access_token_secret)
    while 1:
        try:
            l = StreamListener()
            streamer = tweepy.Stream(auth=api_auth, listener=l)

            keywords = ['cubs']
            streamer.filter(track = keywords)
        except KeyboardInterrupt:
            print("Exit requested")
            sys.exit(0)
        except SystemExit:
            raise
        except Exception as e:
            print("Error: {}".format(e))

if __name__ == "__main__":
    main()
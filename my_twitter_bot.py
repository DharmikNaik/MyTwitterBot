import tweepy
import time

def readLastSeenId(FILE_NAME):
        file = open(FILE_NAME, 'r')
        id = int(file.read().strip())
        file.close()
        return id

def writeLastSeenId(id, FILE_NAME):
	file = open(FILE_NAME, 'w')
	file.write(str(id))
	file.close()

def retrieveAndReplyTweets():
        print('retrieving and replying to tweets...')
        FILE_NAME = 'last_seen_id.txt'
        CONSUMER_KEY = 'ai0sm8Aw54I5aHSTeq7qHFrWu'
        CONSUMER_KEY_SECRET = 'W2TfIXJHWmY2DprIQLAQ3913wnJMziEeKORSgPlbIVi4jCgR7C'
        ACCESS_KEY = '1061922488727175168-ElLzFYStuPiXaPLqVFnReUcyw3ubkg'
        ACCESS_KEY_SECRET = 'XDWd2aoE8V6b2EJQCJ2jopUSY8Wj97uBCI6O2YvVdGzrs'
        HASHTAG = '#cricket'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
        api = tweepy.API(auth)
        
        id = readLastSeenId(FILE_NAME)
        mentions = api.mentions_timeline(id, tweet_mode='extended')

        for mention in reversed(mentions):
                print(str(mention.id) + '-' + mention.full_text)
                if HASHTAG in mention.full_text.lower():
                        print('hashtag found !!!')
                        print('replying...')
                        api.update_status('@' + mention.user.screen_name + ' IND vs PAK; IND - 401/1', mention.id)
                writeLastSeenId(mention.id, FILE_NAME)
	
while True:
        retrieveAndReplyTweets()
        time.sleep(15)

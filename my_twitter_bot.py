import tweepy
import time
import requests


#       This method gets the temperature of the mentoined city in the tweet.
#       The keyword i.e. city name is isolated from the rest of the tweet by the caller and passed as an argument.
#       Open Weather Map's API is used to get the weather information.

def getWeather(keyword):
        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+keyword+'&appid=77cf7caf259a20001f497321bc42619d')
        r_json = r.json()
        try:
                temp = r_json['main']['temp']
                temp = temp - 273.15
                temp = round(temp, 2)
                temp = ' ' + str(temp) + ' °C'
                return temp
        except:
                return " Sorry! Weather  for "+keyword+" cannot be reported"


#       A file is maintained which contains the id of the last served tweet.
#       This method reads the last served tweet's id which is further used to get the new tweets only.
        
def readLastSeenId(FILE_NAME):
        file = open(FILE_NAME, 'r')
        id = int(file.read().strip())
        file.close()
        return id

#       A file is maintained which contains the id of the last served tweet.
#       This method is used to write the last served tweet's id

def writeLastSeenId(id, FILE_NAME):
	file = open(FILE_NAME, 'w')
	file.write(str(id))
	file.close()

#       This method retrieves tweets and replies to them.

def retrieveAndReplyTweets():
        print('retrieving and replying to tweets...')
        FILE_NAME = 'last_seen_id.txt'
        CONSUMER_KEY = 'ai0sm8Aw54I5aHSTeq7qHFrWu'
        CONSUMER_KEY_SECRET = 'W2TfIXJHWmY2DprIQLAQ3913wnJMziEeKORSgPlbIVi4jCgR7C'
        ACCESS_KEY = '1061922488727175168-ElLzFYStuPiXaPLqVFnReUcyw3ubkg'
        ACCESS_KEY_SECRET = 'XDWd2aoE8V6b2EJQCJ2jopUSY8Wj97uBCI6O2YvVdGzrs'
        
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
        api = tweepy.API(auth)
        
        id = readLastSeenId(FILE_NAME)
        mentions = api.mentions_timeline(id, tweet_mode='extended')

        for mention in reversed(mentions):
                print(str(mention.id) + '-' + mention.full_text)
                tweet = mention.full_text
                index = tweet.find('``')
                if(index!=-1):
                        index=index+2
                        keyword = tweet[index:]
                        result = getWeather(keyword)
                        api.update_status('@' + mention.user.screen_name + result, mention.id)
                writeLastSeenId(mention.id, FILE_NAME)

	
while True:
        retrieveAndReplyTweets()
        time.sleep(15)

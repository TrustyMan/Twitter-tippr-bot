import tweepy

FILE_NAME = 'last_seen_id.txt'

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

def twitter_login():
    print 'Logging In...'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    print 'Logged In!'
    return api

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets(api):
    print 'retrieving and replying to tweets...'
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
    last_seen_id,
    tweet_mode='extended'
    )
    for mention in reversed(mentions):
        print str(mention.id) + ' - ' + mention.text
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id)
        if '#helloworld' in mention.text.lower():
            print 'found #helloworld'
        api.update_status('@' + mention.user.screen_name + '#helloworld back to you!', mention.id) # tweet reply
    print 'sleeping 10 seconds'
    time.sleep(10)

api = twitter_login()
while True:
    reply_to_tweets(api)
    pass
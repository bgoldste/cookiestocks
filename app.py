#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import time
import random
import sys
from cookies import cookies, companylist


cookie_len = len(cookies) - 1
#Variables that contains the user credentials to access Twitter API 
root_url = 'https://www.kimonolabs.com/'
path = 'sec/explorer?company='
current_handle = 'CookieStocks'
access_token = "3169249704-kdUxEpjvvHmcOucT7W4Jk7nw5Iw0CwDpmhnvSb2"
access_token_secret = "7sKULNkvumceyVMKxcwpMtamPmfBpLvBOESr7ytjEHfsT"
consumer_key = "6i1nW13NnLVrG0rSOUuWYYn4U"
consumer_secret = "PWMiydRpmuEKkLUJnF0gSdDNClc5diZqYzCzhPcOvuerUTIpEf"


def sec_status_builder(symbols, username):
    cookie = cookies[random.randint(0, cookie_len)]
    cookie_a = cookie.rsplit(' ')
    spaces = len(cookie_a) -1
    status = ''
    hashtags = ['#stocks', '#finance', '#money', '#trading', '#trade']



    sym_string = u''
    for sym in symbols:
        cookie_a.insert(random.randint(0, spaces), sym)
        sym_string = sym_string + sym[1:] + ','
    link = root_url + path + sym_string[:-1]
    spaces = len(cookie_a) -1
    cookie_a.insert(random.randint(0, spaces), hashtags[random.randint(0, 4)])
    for a in cookie_a:
        status = status + a + u' '

    status = status + u'@' + username +' ' 
    if random.randint(0, 1) == 1:
        status = status + u' @kimonolabs'
    status = status + u' ' + link
    return status







# def status_builder(symbols, username):
#     watch_options = ['Following', 'Like', 'Interested in', 'Watching', 'Monitoring', 'Trading', 'Liking']
#     check_options = ['Check out', 'Take a look at', "You've got to see", "You'll love", 'Get data with', 'See']
#     api_options = ['#APIs', "APIs", "#data", "#datasets", "data", "spreadsheets"]
#     status = ('.' * random.randint(0, 1)) + '@' + username + ' ' + watch_options[random.randint(0, 5) ] 
#     for sym in symbols:
#         status += ' ' + sym 
#     status += ("?" * random.randint(1, 2)) + " " + check_options[random.randint(0, 5)] + " our " + api_options[random.randint(0, 5)] + " at https://kimonolabs.com"
#     if len(status) < 141:
#         print 'less than 140'
#         return status
#     else:
#         print 'more than 140, concating'
#         return status[:140]


 
def cookie_status_builder(symbols, username):
    cookie = cookies[random.randint(0, cookie_len)]
    cookie_a = cookie.rsplit(' ')
    spaces = len(cookie_a) -1
    status = ''
    hashtags = ['#stocks', '#finance', '#money', '#trading', '#trade']

    for sym in symbols:
        cookie_a.insert(random.randint(0, spaces), sym)
    spaces = len(cookie_a) -1
    cookie_a.insert(random.randint(0, spaces), hashtags[random.randint(0, 4)])
    for a in cookie_a:
        status = status + a + ' '
    status = status + '@' + username
    if random.randint(0, 1) == 1:
        status = status + u' @kimonolabs'
    return status


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #[u'contributors', u'truncated', u'text', u'in_reply_to_status_id', u'id', u'favorite_count', u'source', u'retweeted',
        # u'coordinates', u'timestamp_ms', u'entities', u'in_reply_to_screen_name', u'id_str', u'retweet_count', u'in_reply_to_user_id',
        # u'favorited', u'user', u'geo', u'in_reply_to_user_id_str', u'possibly_sensitive', u'lang', u'created_at', u'filter_level', u'in_reply_to_status_id_str', u'place']
        d = json.loads(data)
        #catch rt case
        try: 
            # print 'getting user name for rt?'
            username = d['retweeted_status']['user']['screen_name']
            # print 'getting id for rt?'
            tweet_id = d['retweeted_status']['id']
            # print '///////////////////its a rt! og twt' , d['user']['screen_name'], '//////////'

        except:
            # print "************** NOT A RT ******************"
            username = d['user']['screen_name']
            tweet_id = d['id']



        if username != current_handle:
            symbols = [ '$' + x['text'] for x in d['entities']['symbols']]
            status = sec_status_builder(symbols, username)
            print 'updating status', status
            print sec_status_builder(symbols, username)
           
            try:
                api.update_status( in_reply_to_status_id=tweet_id, status=status)
                time.sleep(99)
                if (random.randint(0, 100) > 60):
                    print "following", username
                    api.create_friendship(username)
                elif (random.randint(0, 100) > 35):
                    print 'favoriting'
                    api.create_favorite(tweet_id)
            except:
                print 'Error, going to sleep'
                print "Error:", sys.exc_info()  
                try:
                    time.sleep(19)
                    status = cookie_status_builder(symbols, username)
                    api.update_status( status=status)
                    
                    #api.create_friendship(username)
                except:
                    print 'still failed. waiting a few minutes'
                    time.sleep(300)
                    pass
        else:   
            print "our own tweet"


        return True

    def on_error(self, status):
        print status



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    print "starting"

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = Stream(auth, l)
    stream.filter(track=companylist)

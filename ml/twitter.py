# script to fetch data from twitter for further analysis

import sys
sys.path.append('../lib/tweepy')
import tweepy
import os
import types

def __assert_environ(key):
  if not os.environ.has_key(key):
    raise Exception(key + " is not defined in the environment")
  else:
    return os.environ[key]

def read_twitter_data(filename):
  f = open(filename, "r")
  i = 0
  d = {}
  all_words = {}
  for line in f:
    if i > 500:
      break
    i = i + 1
    try:
      screen_name, ts, uid, text = line.split("\t", 3)
      u = str(uid)
      d.setdefault(u, {})
      for x in text.split(" "):
        d[u][x] = 1.0
        all_words.setdefault(x, 0)
    except Exception as e:
      # ignore error
      pass

#  for k,y in d.items():
#    for a in all_words.keys():
#      if not a in y:
#        y[a] = 0.0

  return d
  
class TweetListener(tweepy.streaming.StreamListener):

  def __init__(self):
    super(self.__class__, self).__init__()
    return

  def on_status(self, status):
    try:
      if status.user.lang == 'en':
        print "%s\t%s\t%s\t%s" % (status.author.screen_name, status.created_at, status.user.id, status.text)
    except:
      # Catch any unicode errors while printing to console
      # and just ignore them to avoid breaking application.
      pass

  def on_error(self, status_code):
    print "An error has occurred! status code = %s" % status_code
    return True

  def on_timeout(self):
    print "Snoozzing.. "
    return

  def on_delete(self, status_id, user_id):
    return

def _my_read_loop(self, resp):

    while self.running and not resp.isclosed():

        # Note: keep-alive newlines might be inserted before each length value.
        # read until we get a digit...
        c = '\n'
        while c == '\n' and self.running and not resp.isclosed():
            c = resp.read(1)
        delimited_string = c

        # read rest of delimiter length..
        d = ''
        while d != '\n' and self.running and not resp.isclosed():
            d = resp.read(1)
            delimited_string += d

        try:
          int_to_read = int(delimited_string)
          next_status_obj = resp.read(int_to_read)
          self._data(next_status_obj)
        except ValueError:
          pass

    if resp.isclosed():
        self.on_closed(resp)


def load_twitter():
  consumer_key = __assert_environ('TW_CONSUMER_KEY')
  consumer_secret = __assert_environ('TW_CONSUMER_SECRET')
  auth_token = __assert_environ('TW_AUTH_TOKEN')
  auth_secret = __assert_environ('TW_AUTH_SECRET')

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(auth_token, auth_secret)

  listener = TweetListener()

  s = tweepy.Stream(auth,  listener, timeout = None)
  setattr(s, "_read_loop", types.MethodType(_my_read_loop, s))
  s.sample()


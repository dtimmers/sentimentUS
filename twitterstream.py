import oauth2 as oauth
import urllib2 as urllib
from time import sleep
from threading import Thread
import sys

class FileOperations:
  def __init__(self, name):
    self.name = name
    self.file = open(self.name,'w')
    self.file.close()

  def open_file_append(self):
    self.file = open(self.name, 'a')

  def write_to_file(self, txt):
    self.open_file_append()
    self.file.write(txt)
    self.close_file()

  def close_file(self):
    self.file.close()

# See the README for how to get these credentials
access_token_key = ""
access_token_secret = ""
 
consumer_key = ""
consumer_secret = ""

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


# Construct, sign, and open a twitter request using the hard-coded credentials above.
def twitter_req(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples(fh):
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitter_req(url, "GET", parameters)
  for line in response:
    fh.write_to_file(line.strip()+'\n')

if __name__ == '__main__':
  time_out = 20*60 #takes 20 minutes to download the tweets
  fn = sys.argv[1]

  fileHandler = FileOperations(fn)
  try:
    t = Thread(target=fetchsamples, args=(fileHandler,))  # run function in another thread
    t.daemon = True # Python will exit when the main thread exits, even if this thread is still running
    t.start()
    sleep(time_out)
  except Exception, errtxt:
    print errtxt


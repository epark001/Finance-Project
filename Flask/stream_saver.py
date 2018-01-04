#This algorithm opens a twitter stream for the given search_terms and appends them to a file.
import tweepy
import csv
class MyStreamListener(tweepy.StreamListener):
    
    # This method will be called when new tweets come in
    def on_status(self, status):
        if (('RT') not in status.text and ('RT @') not in status.text):
            print(status.text)
            print(status.user.name)
            print(status.created_at)
            print(status.id)
            with open(filename, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([status.text, status.user.name, status.created_at, status.id])

#a = ['element','death','halloween'] this is just used as an example to call
def stream_saver(search_terms, filename):
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    b = myStream.filter(track=search_terms, async=False)
#stream_saver(a, 'filename.csv') 'filename.csv' is just a local file

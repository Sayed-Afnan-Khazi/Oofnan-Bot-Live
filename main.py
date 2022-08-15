# OofnanBot
import tweepy
import os
import time
import requests
import cv2
from facedetection import detectFaces
# from dotenv import load_dotenv
# load_dotenv()

# Authenticating to Twitter
def createApi():
    '''Function to connect and authenticate to the Twitter API'''

    # Getting the env variables
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CONSUMER_KEY"]
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_KEY = os.environ["ACCESS_KEY"]
    ACCESS_SECRET= os.environ["ACCESS_SECRET"]

    # Authorizing
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Checking the connection
    try:
        api.verify_credentials()
        print("Authorized!")
    except:
        print("An Error occurred during authentication")

    return api


def infoAboutMe(user):
    '''Function that returns a string with user's name, description and location.'''
    location_present = True # Flag Variable to check if the user has publicly set their location.
    
    if user.location == '':
        location_present = False

    if location_present:
        user_details = f" 𝐍𝐚𝐦𝐞: {user.name} \n 𝐃𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧: {user.description} \n 𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧: {user.location}"
    else:
        user_details = f" 𝐍𝐚𝐦𝐞: {user.name} \n 𝐃𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧: {user.description} \n 𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧: Unknown 🤫"
    
    return user_details


def getLastSeenID(file_name):
    fobj = open(file_name, 'r')
    last_seen_id = int(fobj.read().strip())
    fobj.close()
    return last_seen_id

def storeLastSeenID(last_seen_id, file_name):
    fobj = open(file_name, 'w')
    fobj.write(str(last_seen_id))
    fobj.close()
    return


def replyToTweets():

    # Getting the last_seen_ID
    last_seen_id = getLastSeenID("last_seen_id.txt")

    # Grabbing the mentions timeline
    timeline = api.mentions_timeline(since_id = last_seen_id, tweet_mode='extended') # Extended to allow for a tweet's full_text
    
    for tweet in reversed(timeline):


        print(f"Tweet ID: {tweet.id} - {tweet.user.name} said {tweet.full_text}")

        storeLastSeenID(tweet.id, "last_seen_id.txt")
        # 1541814691629977600
        if '#helloworld' in tweet.full_text.lower():

            reply_tweet = " #HelloWorld back to you!! " + "@" + tweet.user.screen_name
            api.update_status(reply_tweet, in_reply_to_status_id = tweet.id)
            print("A Hello World Response Has Been Sent.")

        elif '#aboutme' in tweet.full_text.lower():

            reply_tweet = infoAboutMe(tweet.user) + '\n' + "@" + tweet.user.screen_name
            api.update_status(reply_tweet, in_reply_to_status_id = tweet.id)
            print("An About Me Response Has Been Sent.")

        elif '#facedetection' in tweet.full_text.lower():
            
            # Grabbing any media in the tweet
            media_files = []
            media = tweet.entities.get('media', [])

            if(len(media) == 0):
                # No picture attached with tweet
                reply_tweet = " I could not find an image with your tweet to analyse, " + "@" + tweet.user.screen_name
                api.update_status(reply_tweet, in_reply_to_status_id = tweet.id)
                print("A Face Detection Response Has Been Sent.")

            else:
                media_files.append(media[0]['media_url'])

                # Downloading the image for further processing
                image_link = requests.get(media_files[-1])
                f = open('that_image.jpg','wb')
                f.write(image_link.content)
                f.close()

                # Detecting faces
                final_image_path, number_of_faces = detectFaces('that_image.jpg')

                # Uploading the image to twitter
                uploaded_media = api.media_upload(final_image_path)
            
                # Posting the tweet with the image
                reply_tweet = f"I found {number_of_faces} faces in this image! " + "@" + tweet.user.screen_name
                api.update_status(status=reply_tweet, media_ids=[uploaded_media.media_id],in_reply_to_status_id = tweet.id)
                print("A Face Detection Response Has Been Sent.")
                

if __name__=="__main__":
    api = createApi()
    replyToTweets()
    time.sleep(15)
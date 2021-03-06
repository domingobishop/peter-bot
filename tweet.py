from nltk.chat.util import Chat, reflections
from nltk.corpus import stopwords
import tweepy
import pairs
import search
import re


def remove_stop_words(text):
    stop_words = stopwords.words("english")
    return ' '.join([word for word in text.split() if word not in stop_words])


def reply(auth, tweet):
    api = tweepy.API(auth)
    try:
        tweetId = tweet.id
        username = tweet.user.screen_name
        text = tweet.text
        text = text.replace('@starlord_p ', '')
        if text.find('would like to know'):
            text = text.replace('I would like to know', '')
            text = remove_stop_words(text)
            print(text)
            result = search.search_guides(text)
            api.update_status("@" + username + " Maybe this guide would help: " + result, in_reply_to_status_id=tweetId)
        else:
            phrase = Chat(pairs.eliza(), reflections).respond(text)
            api.update_status("@" + username + " " + phrase, in_reply_to_status_id=tweetId)
            print("Tweet : " + text)
            print("Replied with : " + phrase)
    except tweepy.TweepError as e:
        print(e.reason)


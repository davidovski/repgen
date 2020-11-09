#!/usr/bin/env python
from config import *

"""
Reddit New Post Bot

"""

import os
import time
import logging

import praw
from subprocess import DEVNULL, STDOUT, check_call

import threading

import requests

###################
## Config
###################

def make(f, sub):
    check_call(['python3', 'movie_gen.py', f], stdout=DEVNULL, stderr=STDOUT)


    uploaded = False
    while not uploaded:
        try:
            check_call(['./bin/youtubeuploader_linux_arm64', '-filename', 'render/' + f + '.mp4', '-privacy', 'public', '-title', "r/" + sub + " \"" + f.replace("_", " ") +"\""])
            uploaded = True
            time.sleep(60)
        except Exception as e:
            pass


def check_submissions(sub):

    start_epoch = time.time() - 60*10  # 1 minute ago

    for submission in sub.new(limit=10):

        try:
            # Check if it's been created in the last minute
            if submission.created_utc >= start_epoch:

                n = submission.title.replace(" ", "_").replace(".", "_")
                filename = "stories/" + n + ".txt"


                if not os.path.exists(filename):
                    content = submission.selftext
                    with open(filename, "w") as file:
                        file.write(content)

                    print(n + "\n" + filename)

                    t = threading.Thread(target=make, args=[n, sub.display_name])
                    t.start()
        except Exception as e:
            print("Issue checking subreddit: {}".format(e))


def main():
    reddit = praw.Reddit(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=user_agent
    )

    while True:
        try:
            for sr in SUBREDDITS:
                sub = reddit.subreddit(sr)
                print("checking r/" + sub.display_name + "...")

                check_submissions(sub)
        except Exception as e:
            print("Issue checking subreddit: {}".format(e))

        print("Sleeping for 10 minutes...")
        time.sleep(10*59)


if __name__ == "__main__":
    # Start Loop
    main()


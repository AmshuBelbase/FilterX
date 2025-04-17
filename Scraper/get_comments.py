from glob import glob
from os.path import expanduser
from sqlite3 import connect
import argparse
import pathlib
import sys
import csv
import time
import emoji
from glob import glob
from os.path import expanduser
from sqlite3 import connect
import os.path
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from instaloader import ConnectionException, Instaloader, Post
from textblob import TextBlob

# 1. Authenticate to Instagram

path_to_firefox_cookies = "C:/Users/AMSHU/AppData/Roaming/Mozilla/Firefox/Profiles/orzpzb9c.default-release/cookies.sqlite"
FIREFOXCOOKIEFILE = glob(expanduser(path_to_firefox_cookies))[0]

print(FIREFOXCOOKIEFILE)

# only allow one attempt for session connection
il = Instaloader(max_connection_attempts=1)

# get cookie id for instagram
il.context._session.cookies.update(connect(FIREFOXCOOKIEFILE)
                                   .execute("SELECT name, value FROM moz_cookies "
                                            "WHERE host='.instagram.com'"))
# check connection
try:
    username = il.test_login()
    if not username:
        raise ConnectionException()
except ConnectionException:
    raise SystemExit(
        "Cookie import failed. Are you logged in successfully in Firefox?")

il.context.username = username

# save session to instaloader file for later use
il.save_session_to_file()

# 2. Build scraper

# initiating instaloader
instagram = Instaloader(download_pictures=False, download_videos=False,
                        download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)

# login
instagram.load_session_from_file('amshubelbase08')


def scrape_data(url):
    SHORTCODE = str(url[28:-1])
    print(SHORTCODE)
    post = Post.from_shortcode(instagram.context, SHORTCODE)

    csv_name = 'combined_csv.csv'
    output_path = pathlib.Path('post_data')
    output_path.mkdir(parents=True, exist_ok=True)
    csv_file_path = output_path / csv_name

    field_names = [
        "post_shortcode",
        "commenter_username",
        "comment_text",
        "comment_likes"
    ]

    # Check if the file exists BEFORE opening it
    file_exists = csv_file_path.exists()

    # post_writer = csv.DictWriter(post_file, fieldnames=field_names)

    with csv_file_path.open("a", encoding="utf-8", newline='') as post_file:
        post_writer = csv.DictWriter(post_file, fieldnames=field_names)
        # Write header only if file is new
        if not file_exists:
            post_writer.writeheader()

        # Write header only if file is new
        if not file_exists:
            post_writer.writeheader()

        c = 0
        # get comments from post
        for x in post.get_comments():
            c += 1
            post_info = {
                "post_shortcode": post.shortcode,
                "commenter_username": x.owner,
                "comment_text": (emoji.demojize(x.text)).encode('utf-8', errors='ignore').decode() if x.text else "",
                "comment_likes": x.likes_count
            }
            print(post_info)
            post_writer.writerow(post_info)

        print("Done Scraping! Comments:", c)


# scrape_data("https://www.instagram.com/p/DIHSfqPNuDW/")
scrape_data("https://www.instagram.com/p/DIcRig7Mrwl/")

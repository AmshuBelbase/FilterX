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

'''
To add user and account info, make sure you are currently logged into specified account on firefox.
'''
#######################################
# 1. Authenticate to Instagram
#######################################
path_to_firefox_cookies = "C:/Users/Username\AppData\Roaming\Mozilla\Firefox\Profiles\orzpzb9c.default-release/cookies.sqlite"
FIREFOXCOOKIEFILE = glob(expanduser(path_to_firefox_cookies))[0]


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

#######################################
# 2. Build scraper
#######################################

# initiating instaloader
instagram = Instaloader(download_pictures=False, download_videos=False,
                        download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)

# login
instagram.load_session_from_file('insta username')


def scrape_data(url):
    SHORTCODE = str(url[28:-1])
    print(SHORTCODE)
    post = Post.from_shortcode(instagram.context, SHORTCODE)

    # # csvName = SHORTCODE + '.csv'
    csvName = 'combined_csv.csv'

    output_path = pathlib.Path('post_data')
    # Create the directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    post_file = output_path.joinpath(csvName).open("w", encoding="utf-8")

    field_names = [
        "post_shortcode",
        "commenter_username",
        "comment_text",
        "comment_likes"
    ]

    post_writer = csv.DictWriter(post_file, fieldnames=field_names)
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


# scrape_data("https://www.instagram.com/p/DFAuiKSysdg/")
scrape_data(
    "https://www.instagram.com/p/DFXG2mXoGj6/")

#######################################
# 3. Add sentiment
#######################################
# load scraped data
df = pd.read_csv('post_data\combined_csv.csv')


def getPolarity(text):
    sen = TextBlob(text).sentiment.polarity
    print(text, " : ", sen)
    return sen


# Ensure all values in 'comment_text' are strings, replace NaN with an empty string
df['comment_text'] = df['comment_text'].fillna("").astype(str)

# add polarity as a column in our data
df['text_polarity'] = df['comment_text'].apply(getPolarity)
df['sentiment'] = pd.cut(df['text_polarity'], [-1, -0.0000000001,
                         0.0000000001, 1], labels=["Negative", "Neutral", "Positive"])

#######################################
# 4. Plot sentiment counts
#######################################

# prep data for graphing
# graph1 = df.groupby(['post_shortcode', 'sentiment']).count().reset_index()
# graph2 = graph1[graph1['post_shortcode'] == SHORTCODE]


colors = colors = ["#FF0066", "gray", "#00FF00"]

# could potentially add other subplots here
fig, (ax) = plt.subplots(ncols=1)

for t, y, c in zip(df["sentiment"], df["comment_text"], colors):
    ax.plot([t, t], [0, y], color=c, marker="o",
            markersize=20, markevery=(1, 2))

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_ylim(0, None)
plt.title("Instagram Comment Sentiment for 'CV5WqggMDCb'", fontsize=15)
plt.setp(ax.get_xticklabels(), rotation=0, fontsize=12)

plt.show()


# colors = colors = ["#FF0066", "gray", "#00FF00"]

# # plot
# fig, (ax) = plt.subplots(ncols=1)

# for t, y, c in zip(graph2["sentiment"], graph2["comment_text"], colors):
#     ax.plot([t, t], [0, y], color=c, marker="o",
#             MarkerSize=20, markevery=(1, 2))

# # remove spines on right and top of plot
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)

# ax.set_ylim(0, None)
# plt.title("Instagram Comment Sentiment", fontsize=15)
# plt.setp(ax.get_xticklabels(), rotation=0, fontsize=12)

# plt.show()

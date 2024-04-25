import json
import random
import statistics
import os
from datetime import datetime

analysis_count = 50000
mid_date = datetime.strptime("2022-10-27", "%Y-%m-%d")
folders = ["immigrant", "lgbtq", "misogyny", "xenophobia"]

def remove_duplicates(tweet_list):
    seen = set()
    for tweet in tweet_list:
        if tweet["id"] in seen:
            tweet_list.remove(tweet)
        seen.add(tweet["id"])
    return False

def equalize_counts(tweet_list):
    pre_list = []
    post_list = []
    for tweet in tweet_list:
        date_str = tweet["date"]
        date_str = date_str[:str(date_str).index("+")]
        if datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") > mid_date:
            post_list.append(tweet)
        else:
            pre_list.append(tweet)

    min_length = min(len(pre_list), len(post_list))
    pre_len = len(pre_list)
    post_len = len(post_list)
    for i in range(min_length, pre_len):
        del pre_list[min_length]
    for i in range(min_length, post_len):
        del post_list[min_length]
    tweet_list = pre_list + post_list
    
    return tweet_list

def find_mean_sd(tweet_list):
    pre_likes = []
    post_likes = []
    for tweet in tweet_list:
        date_str = tweet["date"]
        date_str = date_str[:str(date_str).index("+")]
        if datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") > mid_date:
            post_likes.append(tweet["likeCount"])
        else:
            pre_likes.append(tweet["likeCount"])
    

    return {
        "pre_mean": (statistics.mean(pre_likes)),
        "pre_sd": (statistics.stdev(pre_likes)),
        "post_mean": (statistics.mean(post_likes)),
        "post_sd": (statistics.stdev(post_likes))
    }

tweet_list = []

for folder in folders:
    for filename in os.listdir("tweet_data\\" + folder):
        tweets = json.load(open("tweet_data\\" + folder + "\\" + filename))
        for tweet in tweets:
            tweet["hate_speech_type"] = folder
            tweet_list.append(tweet)

remove_duplicates(tweet_list)

tweet_list.sort(reverse=True, key=lambda t : t["likeCount"])
random.shuffle(tweet_list)
equalize_counts(tweet_list)

like_stats = find_mean_sd(tweet_list)

pre_like_sum = 0 
pre_i_count = 0
pre_l_count = 0
pre_m_count = 0
pre_x_count = 0

post_like_sum = 0

post_i_count = 0
post_l_count = 0
post_m_count = 0
post_x_count = 0

for i in range(analysis_count):
    tweet = tweet_list[i]

    date_str = tweet["date"]
    date_str = date_str[:str(date_str).index("+")]
    if datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") > mid_date:
        if tweet["hate_speech_type"] == "immigrant":
            post_i_count += 1
        elif tweet["hate_speech_type"] == "lgbtq":
            post_l_count += 1
        elif tweet["hate_speech_type"] == "misogyny":
            post_m_count += 1
        else:
            post_x_count += 1
    else:
        if tweet["hate_speech_type"] == "immigrant":
            pre_i_count += 1
        elif tweet["hate_speech_type"] == "lgbtq":
            pre_l_count += 1
        elif tweet["hate_speech_type"] == "misogyny":
            pre_m_count += 1
        else:
            pre_x_count += 1


print("Before Purchase:")
print("\tImmigrant: " + str(pre_i_count))
print("\tLGBTQ: " + str(pre_l_count))
print("\tMisogyny: " + str(pre_m_count))
print("\tXenophobia: " + str(pre_x_count))
print("\tTotal: " + str(pre_i_count + pre_l_count + pre_m_count + pre_x_count)) 
print("\tLike Count Mean: " + str(like_stats["pre_mean"]))
print("\tLike Count Standard Deviation: " + str(like_stats["pre_sd"]))

print("After Purchase:")
print("\tImmigrant: " + str(post_i_count))
print("\tLGBTQ: " + str(post_l_count))
print("\tMisogyny: " + str(post_m_count))
print("\tXenophobia: " + str(post_x_count))
print("\tTotal: " + str(post_i_count + post_l_count + post_m_count + post_x_count)) 
print("\tLike Count Mean: " + str(like_stats["post_mean"]))
print("\tLike Count Standard Deviation: " + str(like_stats["post_sd"]))

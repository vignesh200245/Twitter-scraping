# -*- coding: utf-8 -*-
"""twitter scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1laAG43pWL4kE_q3iOmvwXvvfwQcR_2ct

twitter scraping
"""

import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import base64
import streamlit as st


st.header("Twitter Scraping")
Name=st.text_input("Enter your hashtag:")
Date=st.date_input("Start Date:")
Date2=st.date_input("End Date:")
Count=st.number_input("Count of Tweets:")
# Scraping the Twitter data
def scrape_twitter_data(Name,Date,Date2,Count):
    scrape_data=[]
    search_query=f"#{Name} since:{Date} until:{Date2}"
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        Twitter_List = {
            "date": tweet.date,
            "id": tweet.id,
            "url": tweet.url,
            "content": tweet.content,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        }
        # Append the tweet data to the scrape_data list
        scrape_data.append(Twitter_List)
        if i >= Count:
            break
    tweet_data = pd.DataFrame(scrape_data, columns=["date", "id", "url", "content", "user", "reply_count",
                                                        "retweet_count", "Language", "source", "like_count"])
    return tweet_data
def Send_Data_to_MDB(df):
    Data=df.to_dict('records')
    connection=pymongo.MongoClient('mongodb://vignesh2002:vignesh2002@ac-gyvyn3q-shard-00-00.r67shg1.mongodb.net:27017,ac-gyvyn3q-shard-00-01.r67shg1.mongodb.net:27017,ac-gyvyn3q-shard-00-02.r67shg1.mongodb.net:27017/?ssl=true&replicaSet=atlas-5s2wgp-shard-0&authSource=admin&retryWrites=true&w=majority')
    TwitterDB=connection['Twitter']
    collection=TwitterDB[f'{Name}_Data']
    collection.insert_many(Data)
# ------------------------------------Buttons-----------------------------------------------------------------------
Show_Tweet = st.button('Show the Tweets')
if st.session_state.get('button') != True:
    st.session_state['button'] = Show_Tweet
if st.session_state.get('button') == True:
    tweet_df = scrape_twitter_data(Name,Date,Date2,Count)
    st.dataframe(tweet_df)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('Export DATA to MongoDB'):
            Send_Data_to_MDB(tweet_df)
            st.write('Uploading Success')
    def convert_csv(df):
        return df.to_csv(index=False).encode("utf-8")
    csv = convert_csv(tweet_df)
    with col2:
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="Twitter_data.csv",
            mime="text/csv",
        )
    jsonFile = tweet_df.to_json(orient="records")
    with col3:
        st.download_button(
            label='Download as Json',
            data=jsonFile,
            file_name="twitter_json.json",
            mime="text/json",
        )




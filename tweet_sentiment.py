"""
tweet_sentiment contains function to scrape tweets based on key relevant value and returns average sentiment value.
twitter_sentimant() method take a list of header and generate average sentiment value of tweeter for each header.
"""

import os
import pandas as pd
import numphy as np
import re
import snscrape.modules.twitter as sntwitter
from scipy.stats import gmean
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize, pos_tag
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def vader_score_gmean(score_list):
    pos_list = []
    neg_list = []
    neu_list = []
    compound_list = []
    num_neg = 0
    num_neu = 0
    num_pos = 0
    num_compound = 0
    for score in score_list:
        if score['neg'] != 0:
            num_neg += 1
            neg_list.append(score['neg'])
        if score['neu']!= 0:
            num_neu += 1
            neu_list.append(score['neu'])
        if score['pos'] != 0:
            num_pos += 1
            pos_list.append(score['pos'])
        if score['compound']!= 0:
            num_compound += 1
            compound_list.append((score['compound']+1)*0.5)
    result = {}
    
    result['neu']=gmean(neu_list if len(neu_list)>0 else 0)
    result['pos']=gmean(pos_list if len(pos_list)>0 else 0)
    result['neg']=gmean(neg_list if len(neg_list)>0 else 0)
    result['compound']=gmean(compound_list if len(compound_list)>0 else 1)*2 -1
    return result


def scrape_tweet( word_list, max_tweet = 100):
    # search_line="\""+company_name+"\""
    search_line=""
    for word in word_list:
        search_line += "\""+word+"\""+' '
    attribute_container = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search_line).get_items()):
        tweet_date = str(tweet.date).split(' ')[0]
        attribute_container.append([tweet.user.username,tweet_date,tweet.likeCount,tweet.content])
        # print(attribute_container[-1])
        if i > max_tweet:
            break
    tweet_df = pd.DataFrame(attribute_container,columns=['name','date','likeCount','tweet_text'])
    return tweet_df
    

def get_tweet_sentiment_value(word_list, max_tweet=100):
    tweet_df =scrape_tweet(word_list=word_list,max_tweet=max_tweet)
    vader = SentimentIntensityAnalyzer()
    vader_score = tweet_df['tweet_text'].apply(vader.polarity_scores).tolist()
    return vader_score_gmean(vader_score)

def twitter_sentimant(header_list):
    vader_score_list=[]
    primary_token_list = ['NNP','NNPS']  # token for proper noun
    secondary_token_list = ['NN','NNS']  # token for regular noun
    for headline in header_list:
        headline = re.sub(r"[^A-Za-z\-]"," ", headline)
        # print(headline)
        line_processed=pos_tag(word_tokenize(str(headline)))
        # print(line_processed)
        parsed_headline = []
        secondary_headline = []
        for word,tag in line_processed:
            if tag in primary_token_list:
                parsed_headline.append(word)
            elif tag in secondary_token_list:
                secondary_headline.append(word)
        # if very few proper now, then use regular now to search in tweeter
        if len(parsed_headline)<4:
            parsed_headline = parsed_headline + secondary_headline
        vader_score_list.append(get_tweet_sentiment_value(parsed_headline))
    return vader_score_list


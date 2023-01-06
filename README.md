# Sentiment Analysis of Stocks from financial-news headline with twitter feedback
## Description
As influence of social media arguably more meaningfull for public sentiment compared to news headline, analyzing sentiment for company only based on financial-news or tweeter may not be prudent. This project analyze sentiment of company stocks in two steps.
- Analyze sentiment of company stocks based on financial-news headlines using natural language toolkit(nltk). 
- Collect relevent tweets[^1] for news-headlines and analyze sentiment of company stocks based on tweet for relevent headlines.
[^1]: People give shows their reaction in tweeter which may be influenced by news. Thus tweeter may represent more accurately public reaction then only words in news.

## How to run
My project does not require twitter login information. 
- Provide news headline list url in `finviz_link`
- Provide company name/name list in `company_name_list`[^2] 
[^2]: company name should be accepted by the given url host website.

`graph_generation.ipynb` contains code to further analyze the output.

## Findings
My analysis shows that, there is descripancy in only headlines based sentiment analysis and how people react on twitter. This analysis shows that further reserach is required to find a effective way to combine news-headline and social media to properly analyze public sentiment.

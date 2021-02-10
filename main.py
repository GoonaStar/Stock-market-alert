import requests
from twilio.rest import Client
import datetime
import os

# SET CONSTANTS
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "http://newsapi.org/v2/everything"

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHA_KEY")
NEWS_API_KEY = os.environ.get("NEWS_KEY")

account_sid = os.environ.get("ACCOUNT_KEY")
auth_token = os.environ.get("AUTH_TOKEN")

today = datetime.date.today()
yesterday = today- datetime.timedelta(days=1)
before_yesterday = today - datetime.timedelta(days=2)

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_API_KEY

}

parameters_news = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

# FETCH THE API FOR THE STOCK VALUES
response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
print(data)

yesterday_stock_value = data["Time Series (Daily)"][f"{yesterday.year}-{yesterday.month:02d}-{yesterday.day:02d}"][
    "4. close"]
before_yesterday_stock_value = data["Time Series (Daily)"][
    f"{before_yesterday.year}-{before_yesterday.month:02d}-{before_yesterday.day:02d}"][
    "4. close"]

# or using list comprehension:
# data = response.json()["Time Series (Daily)"]
# data_list = [value for (key, value) in data.items()]
# yesterday_data = data_list[0]

difference_price = float(yesterday_stock_value) - float(before_yesterday_stock_value)

# SET THE SIGN VALUE
is_up = None
if difference_price > 0:
    is_up = "🔺"
else:
    is_up = "🔻"
variation_price = round((difference_price / float(yesterday_stock_value)) * 100)

# IF VARIATION OF VALUES BEFORE YESTERDAY AND THE DAY BEFORE > 5, SENT ALERT
if abs(variation_price) > 5:
    response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    data_news = response_news.json()["articles"]

    three_articles = data_news[:3]

    list_content = [f"Headline: {article['title']}. \n Description: {article['description']}" for article
                    in three_articles]

    print(list_content)

    client = Client(account_sid, auth_token)
    for article in list_content:
        message = client.messages \
            .create(
            body=f"{STOCK}: {is_up}{variation_price}%\n{article}",
            from_='+15415834773',
            to='+81 80-3720-7494'
        )




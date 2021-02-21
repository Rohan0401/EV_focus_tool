import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from typing import List, Dict
from core.errors import GetStockException
from core.config import URL_PATH
from loguru import logger


class StockTraderHandler(object):
    res = None

    @classmethod
    def get_insider_df(cls, ticker: str) -> List:
        url  = (URL_PATH + ticker.lower())
        # Get dataframe
        insider = cls.get_html(url, h_class='body-table')
        try:
            insider = insider[0]
            # clean dataframe
            insider = insider.iloc[1:]
            insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']
            insider = insider[['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']]
            insider = insider.set_index('Date')
            insider = insider.to_dict(orient="records")
            return insider
        except Exception as e:
            logger.error(e)
            raise e

    @classmethod
    def get_fundamentals(cls, ticker: str) -> Dict:
        try:
            url = (URL_PATH + ticker.lower())

            # Find fundamentals table
            fundamentals = cls.get_html(url, h_class='snapshot-table2')

            fundamentals = fundamentals[0]

            # Clean up fundamentals dataframe
            fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
            colOne = []
            colLength = len(fundamentals)
            for k in np.arange(0, colLength, 2):
                colOne.append(fundamentals[f'{k}'])
            attrs = pd.concat(colOne, ignore_index=True)

            colTwo = []
            colLength = len(fundamentals)
            for k in np.arange(1, colLength, 2):
                colTwo.append(fundamentals[f'{k}'])
            vals = pd.concat(colTwo, ignore_index=True)

            fundamentals = pd.DataFrame()
            fundamentals['Attributes'] = attrs
            fundamentals['Values'] = vals
            fundamentals = fundamentals.set_index('Attributes')
            fundamentals = fundamentals.to_dict(orient="dict")
            return fundamentals
        except Exception as e:
            logger.error(e)
            return e

    @classmethod
    def get_news(cls, ticker):

        url = (URL_PATH + ticker.lower())
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        html = soup(webpage, "html.parser")
        news = cls.get_html(url, h_class='fullview-news-outer')
        news = news[0]
        try:
            # Find news table
            links = []
            for a in html.find_all('a', class_="tab-link-news"):
                links.append(a['href'])

            # Clean up news dataframe
            news.columns = ['Date', 'News Headline']
            news['Article Link'] = links
            news = news.set_index('Date')
            news = news.to_dict(orient="records")
            return news
        except Exception as e:
            return e

    
        

    @staticmethod
    def get_html(input_url, h_class):
        res = None 
        try:
            if not input_url:
                message = f"The input url {input_url} is empty"
                logger.error(message)
                raise GetStockException(message)
            req = Request(input_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            html = soup(webpage, "html.parser")
            res = pd.read_html(str(html), attrs = {'class': h_class})
            if not res:
                message = "Empty response"
                logger.error(message)
                raise GetStockException(message)
            return res
        except Exception as e:
            logger.error(e)
            raise e
    








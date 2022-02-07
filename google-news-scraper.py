from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import nltk
import traceback
import argparse
import datetime

nltk.download('punkt')

class NewsScraper:

    def __init__(self):
        #take the inputs and assign it to the variables
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--start-date', metavar='', help="Start Date for scraping news", required=False)
        parser.add_argument('-e', '--end-date', metavar='', help="End Date for scraping news", required=False)
        parser.add_argument('-t', '--search-text', metavar='', help="Search Text", required=True)

        args = parser.parse_args()
        self.start_date = args.start_date
        self.end_date = args.end_date
        self.search_text = str(args.search_text)

        if (self.start_date == None):
            self.start_date = str((datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d/%m/%Y'))
        if (self.end_date == None):
            self.end_date = str(datetime.datetime.today().strftime('%m/%d/%Y'))

        self.init_config()


    def init_config(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        self.config = Config()
        self.config.browser_user_agent = user_agent


    def fetch_news_urls(self):
        googlenews = GoogleNews(start=self.start_date, end=self.end_date, region='IN')
        print("Searching Google News for: {}".format(self.search_text))
        googlenews.search(self.search_text)
        result=googlenews.result()
        self.news_df=pd.DataFrame(result)
        print("Downloading news from GoogleNews")
        for i in range(2,5):
            print("Downloading page {} of GoogleNews".format(i))
            googlenews.getpage(i)
            result=googlenews.result()
            self.news_df=pd.DataFrame(result)
            print(len(self.news_df.index))


    def scrape_news(self):
        self.fetch_news_urls()
        parsed_news=[]
        for index in self.news_df.index:
            news_dict={}
            print("Reading article {} - {}".format(index, self.news_df['title'][index]))
            article = Article(self.news_df['link'][index],config=self.config)
            try:
                article.download()
                article.parse()
                article.nlp()
                news_dict['Date']=self.news_df['date'][index]
                news_dict['Media']=self.news_df['media'][index]
                news_dict['Title']=article.title
                news_dict['Article']=article.text
                news_dict['Summary']=article.summary
                parsed_news.append(news_dict)
            except Exception as e:
                print("Unable to download article: {}, from URL: {} ".format(self.news_df['title'][index], self.news_df['link'][index]))

        news_df=pd.DataFrame(parsed_news)
        export_file_name = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M') + "-news-articles.xlsx"
        news_df.to_excel(export_file_name)
        print("Scraped news successfully exported to: {}".format(export_file_name))



if __name__ == "__main__":
    try:
        news_scraper = NewsScraper()
        news_scraper.scrape_news()
    except Exception as e:
        print(traceback.format_exc())

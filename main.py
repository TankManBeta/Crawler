from get_movie_data import DouCrawler
from get_paper_data import CNKICrawler

if __name__ == "__main__":
    # dou_crawler = DouCrawler()
    # dou_crawler.get_data()
    cnki_browser = CNKICrawler("县级博物馆", "发展")
    cnki_browser.get_paper_data()

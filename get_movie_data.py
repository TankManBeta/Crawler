# -*- coding: utf-8 -*-

"""
    @Author 坦克手贝塔
    @Date 2022/3/12 18:16
"""

import requests
import time
from bs4 import BeautifulSoup


class DouCrawler:
    def __init__(self) -> None:
        self.url = "https://movie.douban.com/top250"

    def get_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/99.0.4844.51 Safari/537.36 ",
        }

        index = 0
        general_info = []
        while index < 250:
            parameters = {
                "start": str(index),
                "filter": ""
            }
            response = requests.get(self.url, headers=headers, params=parameters)
            if response.status_code == 200:
                print("成功："+str(response.status_code))
                bs = BeautifulSoup(response.text, "lxml")
                general_info += bs.find_all("div", {"class": "item"})
                index += 25
                time.sleep(10)
            else:
                print("失败："+str(response.status_code))
                time.sleep(60)
                response = requests.get(self.url, headers=headers, params=parameters)

        for item in general_info:
            movie_name = item.find_all("span", {"class": "title"})[0].string
            movie_star = item.find_all("span", {"class": "rating_num"})[0].string
            movie_brief_introduction = item.find_all("span")[-1].string
            print("电影名：", movie_name, "得分：", movie_star, "简介：", movie_brief_introduction)


if __name__ == "__main__":
    my_crawler = DouCrawler()
    my_crawler.get_data()
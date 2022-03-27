import requests
import time
from bs4 import BeautifulSoup
import pymysql


class DouCrawler:
    def __init__(self) -> None:
        self.url = "https://movie.douban.com/top250"

    @staticmethod
    def create_table():
        sql_create_table = """
        CREATE TABLE Movie (
        id INT auto_increment PRIMARY KEY ,
        name CHAR(100) ,
        star FLOAT ,
        introduction CHAR(200)
        );
        """
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='MovieDB')
        cursor = conn.cursor()
        try:
            cursor.execute(sql_create_table)
            conn.commit()
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()

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
                time.sleep(5)
            else:
                print("失败："+str(response.status_code))
                time.sleep(10)
                response = requests.get(self.url, headers=headers, params=parameters)

        DouCrawler.create_table()
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='MovieDB')
        cursor = conn.cursor()

        for item in general_info:
            movie_name_option = item.find_all("span", {"class": "title"})
            movie_name = movie_name_option[0].string if movie_name_option else ""
            movie_star_option = item.find_all("span", {"class": "rating_num"})
            movie_star = movie_star_option[0].string if movie_star_option else ""
            movie_introduction_option = item.find_all("span", {"class": "inq"})
            movie_introduction = movie_introduction_option[0].string if movie_introduction_option else ""
            sql_insert_data = "INSERT INTO Movie(name, star, introduction) VALUES (%s, %s, %s);"
            try:
                cursor.execute(sql_insert_data, [movie_name, float(movie_star), movie_introduction])
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
        conn.close()

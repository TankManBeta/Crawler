import time
from selenium import webdriver, common
from selenium.webdriver.common.by import By


class CNKICrawler:
    def __init__(self, keyword1, keyword2):
        self.url = "https://kns.cnki.net/kns8/AdvSearch"
        self.executable_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        self.keyword1 = keyword1
        self.keyword2 = keyword2

    def get_paper_data(self):
        browser = webdriver.Chrome(self.executable_path)
        browser.get(self.url)
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/div[1]/div[1]').click()
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/div[1]/div[2]/ul/li[4]').click()
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys(self.keyword1)
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[3]/a').click()
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/div[1]/div[1]').click()
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/div[1]/div[2]/ul/li[4]').click()
        browser.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[2]/div[2]/input').send_keys(self.keyword2)
        time.sleep(2)
        browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input').click()

        time.sleep(2)
        page_count = browser.find_element(By.XPATH, '//*[@id="countPageDiv"]/span[2]').text
        page_count = int(page_count.split('/')[-1])
        for _ in range(page_count):
            for i in range(1, 21):
                try:
                    title = browser.find_element(
                        By.XPATH, f'//*[@id="gridTable"]/table/tbody/tr[{i}]/td[9]/a[1]').get_attribute("title")
                except common.exceptions.NoSuchElementException:
                    break
                if title != "下载":
                    continue
                else:
                    browser.find_element(By.XPATH, f'//*[@id="gridTable"]/table/tbody/tr[{i}]/td[2]/a').click()
                    time.sleep(3)
                    windows = browser.window_handles
                    browser.switch_to.window(windows[1])
                    try:
                        temp_browser = browser.find_element(By.ID, "pdfDown")
                        if temp_browser.text == "分页下载":
                            browser.close()
                            browser.switch_to.window(windows[0])
                            continue
                        else:
                            temp_browser.click()
                    except common.exceptions.NoSuchElementException:
                        continue
                    browser.close()
                    browser.switch_to.window(windows[0])
                    time.sleep(3)
            browser.find_element(By.ID, "Page_next_top").click()
            time.sleep(3)
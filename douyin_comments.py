import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from single_video_comments import drop_down, str2num, crawl_comments

#parameters
account_home_page= 'https://www.douyin.com/user/MS4wLjABAAAAABJTNtdE9bZKmIZfL_pR15F8X0VNK591ffRA9pXXZsw'
video_num = 10
max_video_num = 100

comment_num = 10
max_comment_num = 50

driver = webdriver.Chrome()
driver.get(account_home_page)
drop_down(driver, "video", max_video_num)

account_id = driver.find_element(By.CSS_SELECTOR, ".Nu66P_ba").text
account_path = './' + account_id
if not os.path.exists(account_path):
    os.mkdir(account_path)


lis = driver.find_elements(By.CSS_SELECTOR, '.Eie04v01')
url_likes = []
for li in lis:
    url = li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    video_like = str2num(li.find_element(By.XPATH, './div/a/div/span/span').text)
    url_likes.append([url, video_like])

url_likes.sort(key=lambda x : x[-1], reverse=True)

num = 0
for url, _ in url_likes[:min(video_num, len(url_likes))]:
    num += 1
    comment_path = account_path + "/" + str(num) + ".txt"
    crawl_comments(driver, url, comment_num, max_comment_num, comment_path)


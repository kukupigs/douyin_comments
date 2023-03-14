from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

video_num = 10
comment_num = 10

def drop_down(driver, video_or_comment, max_num):
    #等待用户验证
    prev_height = 0
    if video_or_comment == "video":
        wait_ele = ".Eie04v01"
        wait_time = 20

        new_num = 60
        ele_num = 20

    elif video_or_comment == "comment":
        wait_ele = ".RHiEl2d8"
        wait_time = 10

        new_num = 25
        ele_num = 5

    else:
        raise ValueError
    
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_ele)))
    
    while True:
        # Get current scroll height
        curr_height = driver.execute_script("return document.documentElement.scrollHeight")

        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait for a few seconds
        time.sleep(3)

        # Get the new scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        new_num = new_num + ele_num

        # Break if we have reached the bottom of the page
        if (new_height == curr_height == prev_height) or (new_num >= max_num):
            break

        # Update the previous scroll height
        prev_height = curr_height

def extract(comment_splitted):
    try:
        text = comment_splitted[1]
        if comment_splitted[-1] == '回复':
            like = str2num(comment_splitted[-3])
        else:
            like = str2num(comment_splitted[-4])
        
    except:
        text = ""
        like = 0
    return text, like

def str2num(s):
    try:
        if s[-1] == '万':
            n = int(float(s[:-1]) * 10000)
        else:
            n = int(s)
    except:
        n = 0
    return n

def crawl_comments(driver, url, comment_num, max_num ,comment_path):
    driver.get(url)
    drop_down(driver, "comment", max_num)
    video_like = driver.find_element(By.CSS_SELECTOR, ".CE7XkkTw").text

    comments = driver.find_elements(By.CSS_SELECTOR, ".RHiEl2d8")
    text_likes = []
    for comment in comments:
        comment_splitted = comment.text.split(sep='\n')
        print(comment_splitted)
        text_likes.append(extract(comment_splitted))

    text_likes.sort(key= lambda x : x[-1], reverse=True)
    try:
        video_name = driver.find_element(By.CSS_SELECTOR, ".Nu66P_ba").text.split(sep=' ')[0]
    except:
        video_name = 'unknown video'

    f = open(comment_path, 'w',encoding='utf-8')
    f.write('视频名称：' + video_name + '\n')
    f.write('视频点赞：' + video_like + '\n')
    f.write('视频地址：' + url + '\n')
    f.write('评论：' + '\n')
    for i in range(min(comment_num, len(text_likes))):
        f.write('点赞数：' + str(text_likes[i][-1]) + '  ' + text_likes[i][0] + '\n')
    f.close()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    url = "https://www.douyin.com/video/7208122860320181561"

    crawl_comments(driver, url, 10, 50, "test.txt")
# 导入所需的模块

import os from selenium import webdriver from selenium.webdriver.common.by import By import time import random

# 抖音用户主页链接和需要获取评论的视频数量

account_home_page = 'https://www.douyin.com/user/MS4wLjABAAAAABJTNtdE9bZKmIZfL_pR15F8X0VNK591ffRA9pXXZsw' video_num = 20 comment_num = 50

# 下拉函数，用于滚动网页并加载更多内容

def drop_down(): for x in range(1, 50, 4): time.sleep(2) j = x / 9 js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j driver.execute_script(js)

# 将评论中的点赞数字符串转化为数字

def str2num(s): if s[-1] == '万': n = int(float(s[:-1]) * 10000) else: n = int(s) return n

# 提取评论中的文本和点赞数

def extract(comment_splitted): text = comment_splitted[1] if comment_splitted[-1] == '回复': like = str2num(comment_splitted[-3]) else: like = str2num(comment_splitted[-4]) return text, like

# 创建 Chrome 浏览器实例并打开用户主页

driver = webdriver.Chrome() driver.get(account_home_page) time.sleep(3) drop_down() driver.implicitly_wait(10)

# 获取用户 ID 并创建以其命名的文件夹，用于存储评论

account_id = driver.find_element(By.XPATH, '//*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div[1]/h1/span/span/span/span/span/span').text account_path = './' + account_id if not os.path.exists(account_path): os.mkdir(account_path)

# 获取热门视频的链接和点赞数，并按照点赞数排序

lis = driver.find_elements(By.CSS_SELECTOR, '.Eie04v01') url_likes = [] for li in lis: url = li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') video_like = str2num(li.find_element(By.XPATH, 'a/div/span/span').text) url_likes.append([url, video_like]) url_likes.sort(key=lambda x: x[-1], reverse=True)

# 针对每个视频获取热门评论

num = 0 for url, video_like in url_likes[:min(video_num, len(url_likes))]: num += 1 driver.get(url) time.sleep(random.randint(1, 2)) drop_down()

# 尝试获取视频名称

try: video_name = driver.find_element(By.XPATH, '//*[@id="douyin-right-container"]/div[2]/div/div[1]/div[3]/div/div[1]/div/h2/span').text.split(sep=' ')[0] except: # 如果无法获取视频名称，将其设置为"unknown video" video_name = 'unknown video'

# 生成评论文件路径

comment_path = account_path + '/' + str(num) + '.txt'

# 打开评论文件，以utf-8编码方式写入

f = open(comment_path, 'w',encoding='utf-8')

# 写入视频名称、点赞数、视频地址等信息

f.write('视频名称：' + video_name + '\n') f.write('视频点赞数：' + str(video_like) + '\n') f.write('视频地址：' + url + '\n') f.write('评论：' + '\n')

# 写入评论信息，包括点赞数和评论文本

for i in range(min(comment_num, len(text_likes))): f.write('点赞数：' + str(text_likes[i][-1]) + ' ' + text_likes[i][0] + '\n')

# 关闭评论文件

f.close()

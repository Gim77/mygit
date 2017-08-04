#coding:utf-8
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import json
import time
from PIL import Image, ImageOps
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

# driver = webdriver.PhantomJS()
driver = webdriver.Chrome('D:/chromedriver')
# driver.maximize_window()
driver.get('https://passport.jd.com/new/login.aspx')
assert '京东' in driver.title

change = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/a')
change.click()

name = driver.find_element_by_name('loginname')
name.send_keys(u'18850467053')
password = driver.find_element_by_name('nloginpwd')
password.send_keys(u'Z606a417yhgmxx7')
time.sleep(1)
submit = driver.find_element_by_id('loginsubmit')
submit.click()

#
# time.sleep(2)
#
# submit = driver.find_element_by_id('loginsubmit')
# submit.click()

# 截取验证码
# driver.get_screenshot_as_file('a.jpg')
# location = driver.find_element_by_id('JD_Verification1').location
# size = driver.find_element_by_id('JD_Verification1').size
# left = location['x']
# top = location['y']
# right = location['x'] + size['width']
# bottom = location['y'] + size['height']
# a = Image.open("a.jpg")
# image = a.crop((left, top, right, bottom))
#
# image = image.point(lambda x: 0 if x < 143 else 255)
# borderImage = ImageOps.expand(image, border=20, fill='white')
# image.save('a.jpg')
# 获取总页数
# page_num = driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b')
time.sleep(2)
driver.get('http://try.jd.com/activity/getActivityList?page=1&activityType=1')
page_num = driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b').text

ids = []
for page in range(1, int(page_num) + 1):
    driver.get('http://try.jd.com/activity/getActivityList?page={}&activityType=1'.format(page))
    elements = driver.find_elements_by_xpath("//*[@id=\"goods-list\"]/div[2]/div/ul/li/div/a" )
    for element in elements:
        link = element.get_attribute('href')
        product_id = re.findall(r"http://try\.jd\.com/([0-9]+)\.html", link)[0]
        ids.append(product_id)

# 判断是否已经申请
n = 0
for id in ids:
    driver.get('http://try.jd.com/migrate/getActivityById?id={}'.format(id))
    isApply = re.findall(r'"submit"\:([a-z]+)\,', driver.page_source)
    try:
        if isApply[0] == 'false':
            n += 1
            print(id, n)
            driver.get('http://try.jd.com/migrate/apply?activityId={}&source=0'.format(id))
            time.sleep(10)
    except Exception:
        pass
driver.quit()

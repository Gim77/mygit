#coding:utf-8
from selenium import webdriver
import selenium
import time
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
password.send_keys(u'xxxxxxxxxx')
time.sleep(1)
submit = driver.find_element_by_id('loginsubmit')
submit.click()


ids = []
for page in range(5, 91):
    driver.get('http://try.jd.com/activity/getActivityList?page={}&activityType=1'.format(page))
    elements = driver.find_elements_by_xpath("//*[@id=\"goods-list\"]/div[2]/div/ul/li/div/a" )
    for element in elements:
        link = element.get_attribute('href')
        product_id = re.findall(r"http://try\.jd\.com/([0-9]+)\.html", link)[0]
        ids.append(product_id)


for id in ids:
    print(id)
    driver.get('http://try.jd.com/migrate/apply?activityId={}&source=0'.format(id))
    time.sleep(10)



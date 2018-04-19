#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Constant
HOMEPAGE = "https://www.atgame.kr/ssl/member/login.atg?login_rtn="
THESHOW = "http://www.atgame.kr/product/view.atg?item=1103012355"
GOW4 = "http://www.atgame.kr/product/view.atg?item=1103012359"

ITEMURL = GOW4

USERID = ""
PASSWORD = ""
NAME = u""

###############################################
REALORDER = True  # True to order automatically
###############################################

WAITTIME = 1000
SLEEPSEC = 1
LOOP = -1  # -1 for infinite


# Logic
def login(driver):
    try:
        userid = driver.find_element(By.ID, 'id')
        passwd = driver.find_element(By.ID, 'pw')
        button = driver.find_element(By.ID, 'btn-login')
        userid.send_keys(USERID)
        passwd.send_keys(PASSWORD)
        button.click()

        # wait until logged-in
        logout = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[@href='http://www.atgame.kr/biz/member/logout.atg']")))
    except NoSuchElementException:
        try:
            username = driver.find_element_by_xpath("//div[@class='login']/strong[1]")
            print(username.get_attribute("innerHTML"))
        except NoSuchElementException, e:
            print e

def checkStock(driver, i):
    try:
        buybutton = driver.find_element_by_xpath("//button[@id='btn-order']")
        print "Go! Checkout~"
        return False
    except NoSuchElementException:
        print('[%d]%s' % (i, 'out of stock'))
        return True

def checkout(driver):
    orderbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//button[@id='btn-order']")))
    orderbutton.click()

def closePopups(driver):
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        alert.accept()
    except TimeoutException:
        print "no alert"

def order(driver):
    try:
        # 주문고객과 동일한 주소 선택
        addressradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@id='chk-ord']")))
        addressradio.click()

        # 결제하기
        placebutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//button[@id='btn-order']")))
        if REALORDER:
            placebutton.click()
        else:
            print 'waiting for placing order...'
    except NoSuchElementException, e:
        print e

# Main
if __name__ == "__main__":
    # init webdriver
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 2)

    # open site
    driver.get(HOMEPAGE)

    # login then move to item page
    login(driver)
    driver.get(ITEMURL)

    # check stock and save to cart
    i = 1
    while(checkStock(driver, i)):
        i += 1
        time.sleep(SLEEPSEC)
        if (i > LOOP and LOOP != -1):
            break
        driver.get(ITEMURL)

    # check out
    checkout(driver)

    # close pop-up if exist
    closePopups(driver)

    # order
    order(driver)

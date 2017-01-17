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
HOMEPAGE = "http://www.atgame.kr/"
PS4PRO = "http://www.atgame.kr/product/product_view.game?item=1103012016&cat=010601"
DUALSHOCK4GOLD = "http://www.atgame.kr/product/product_view.game?item=1103012058&cat="
ITEMURL = PS4PRO

USERID = ""
PASSWORD = ""
NAME = u""

###############################################
REALORDER = True # True to order automatically
###############################################

WAITTIME = 1000
SLEEPSEC = 1
LOOP = -1 # -1 for infinite


# Logic
def login(driver):
    try:
        userid = driver.find_element(By.NAME, 'userid')
        # userid = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME,'userid')))
        passwd = driver.find_element(By.NAME, 'userpwd')
        button = driver.find_element_by_xpath("//form[@name='FRMLOGINTOP']/input[4]")
        userid.send_keys(USERID)
        passwd.send_keys(PASSWORD)
        button.click()

        # wait until logged-in
        logout = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//img[@class='btn_logout']")))
    except NoSuchElementException:
        try:
            username = driver.find_element_by_xpath("//div[@class='login']/strong[1]")
            print(username.get_attribute("innerHTML"))
        except NoSuchElementException, e:
            print e

def checkStock(driver, i):
    try:
        # outofstock = driver.find_element_by_class_name('order_desc')
        # print('[%d]%s' % (i, outofstock.get_attribute("innerHTML")))
        buybutton = driver.find_element_by_xpath("//div[@class='order_btn']/img[@src='/images/product/btn_cart.gif']")
        print "Go! Checkout~"
        return False
    except NoSuchElementException:
        print('[%d]%s' % (i, 'out of stock'))
        return True

def checkout(driver):
    cartbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//div[@class='order_btn']/img[1]")))
    cartbutton.click()
    cartarea = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_area")))
    try:
        orderbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//div[@class='btn_right'][1]/img[1]")))
        print(orderbutton.get_attribute("innerHTML"))
        orderbutton.click()
    except NoSuchElementException, e:
        print e

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
        addressradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@name='same'][@value='1']")))
        addressradio.click()

        # 할인혜택 받기
        point = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.NAME, "NowUsePoint")))
        mypoint = int(point.get_attribute("value"))
        print "point: %d" % mypoint
        if (mypoint > 100):
            pointbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.ID, "img_direct_use")))
            pointbutton.click()

        # 무통장입급
        bankradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@name='rdo_payment'][@value='Z']")))
        bankradio.click()

        # 은행선택
        try:
            bankselect = driver.find_element_by_xpath("//select[@name='bank2code']/option[@value='하나은행']")
            bankselect.click()
        except NoSuchElementException, e:
            bankselect = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//select[@name='bank2code']/option[@value='국민은행']")))
            bankselect.click()
        # 이름
        payer = driver.find_element(By.NAME, 'payer')
        payer.send_keys(NAME)

        # 결제하기
        placebutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//div[@class='btn_payment']/img[@class='first']")))
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

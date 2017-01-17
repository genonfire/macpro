#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Constant
HOMEPAGE = "http://www.game2buy.co.kr/shop/member/login.php?&"
PS4PRO = "http://www.game2buy.co.kr/shop/goods/goods_view.php?goodsno=4934&category=016001"
STAND = "http://www.game2buy.co.kr/shop/goods/goods_view.php?goodsno=4955&category=016003"
ITEMURL = PS4PRO

USERID = ""
PASSWORD = ""

###############################################
REALORDER = True # True to order automatically
###############################################

WAITTIME = 1000
SLEEPSEC = 1
LOOP = -1 # -1 for infinite


# Logic
def login(driver):
    try:
        userid = driver.find_element_by_xpath("//input[@type='text'][@name='m_id']")
        # userid = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'m_id')))
        passwd = driver.find_element_by_xpath("//input[@type='password'][@name='password']")
        button = driver.find_element_by_xpath("//input[@type='image'][@src='/shop/data/skin/150519_skin/img/common/btn_login.gif']")
        userid.send_keys(USERID)
        passwd.send_keys(PASSWORD)
        button.click()

        # wait until logged-in
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//area[@href='/shop/member/logout.php?&']")))
    except NoSuchElementException, e:
        print e

def checkStock(driver, i):
    try:
        buybutton = driver.find_element_by_xpath("//a/img[@src='/shop/data/skin/150519_skin/images/btn_buy.gif']")
        print "Go! Checkout~"
        return False
    except NoSuchElementException:
        print('[%d]%s' % (i, 'out of stock'))
        return True

def checkout(driver):
    cartbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//a/img[@src='/shop/data/skin/150519_skin/images/btn_buy.gif']")))
    cartbutton.click()

def closePopups(driver):
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        alert.dismiss()
    except TimeoutException:
        print "no alert"

def order(driver):
    try:
        # 적립금
        emoney = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text'][@id='emoney']")))
        emoneytext = emoney.find_element_by_xpath('..').get_attribute("innerHTML")
        splice = emoneytext.split('보유적립금 : ')
        splice1 = splice[1].split('원')
        point = splice1[0].replace(',', '')
        mypoint = int(point)
        print "point: %d" % mypoint
        if (mypoint >= 100):
            driver.execute_script("document.getElementById('emoney').setAttribute('value', '')");
            emoney.send_keys(mypoint)
            print 'using point %d' % mypoint

        # 무통장입금
        bankradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@type='radio'][@name='settlekind'][@value='a']")))
        bankradio.click()
        while (not bankradio.is_selected()):
            print 'bankradio not selected'
            bankradio.click()

        # 결제하기
        orderbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@type='image'][@src='/shop/data/skin/150519_skin/img/common/btn_payment.gif']")))
        orderbutton.click()
    except NoSuchElementException, e:
        print e

def placing(driver):
    try:
        # 동의
        concent = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox'][@name='doubleCheckYN']")))
        concent.click()
        while (not concent.is_selected()):
            print 'concent not checked'
            concent.click()
        # 입금계좌
        try:
            bankselect = driver.find_element_by_xpath("//select[@name='bankAccount']/option[@value='1']")
            print bankselect.get_attribute('value')
            bankselect.click()
        except NoSuchElementException, e:
            try:
                bankselect = driver.find_element_by_xpath("//select[@name='bankAccount']/option[@value='2']")
                bankselect.click()
            except NoSuchElementException, e:
                print e
        # 결제하기
        placebutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//img[@src='/shop/data/skin/150519_skin/img/common/btn_payment.gif']")))
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
    default_handle = driver.current_window_handle

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

    # order
    order(driver)

    # placing
    placing(driver)

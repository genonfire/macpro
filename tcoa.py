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
HOMEPAGE = "http://www.tcoa.co.kr/member/login.html"
PS4PRO = "http://www.tcoa.co.kr/product/detail.html?product_no=340&cate_no=32&display_group=1"
STAND = "http://www.tcoa.co.kr/product/detail.html?product_no=281&cate_no=43&display_group=1"
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
        userid = driver.find_element(By.ID, 'member_id')
        # userid = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'member_id')))
        passwd = driver.find_element(By.ID, 'member_passwd')
        button = driver.find_element_by_xpath("//img[@src='http://img.echosting.cafe24.com/design/skin/default/member/btn_login.gif']")
        userid.send_keys(USERID)
        passwd.send_keys(PASSWORD)
        button.click()

        # wait until logged-in
        logout = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@id='member_nick']/span[@class='xans-member-var-name']")))
        print 'logged in as %s' % logout.get_attribute("innerHTML")
    except NoSuchElementException, e:
        print e

def checkStock(driver, i):
    try:
        buybutton = driver.find_element_by_xpath("//a[@class='first ']/img[@src='http://img.echosting.cafe24.com/design/skin/default/product/btn_buy_big.gif']")
        print "Go! Checkout~"
        return False
    except NoSuchElementException:
        print('[%d]%s' % (i, 'out of stock'))
        return True

def checkout(driver):
    cartbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//img[@src='http://img.echosting.cafe24.com/design/skin/default/product/btn_buy_big.gif']")))
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
        # 주문자 정보와 동일
        addressradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@id='sameaddr0']")))
        addressradio.click()

        # 무통장입급
        bankradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@id='addr_paymethod1']")))
        bankradio.click()
        while (not bankradio.is_selected()):
            print 'bankradio not selected'
            bankradio.click()

        # 이름
        payer = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.ID, "pname")))
        # while (not payer.is_displayed()):
            # payer = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.ID, "pname")))
        payer.send_keys(NAME)

        # 은행선택
        try:
            bankselect = driver.find_element_by_xpath("//select[@id='bankaccount']/option[@value='bank_04:56500201340709:이채호:국민은행:www.kbstar.com']")
            bankselect.click()
        except NoSuchElementException, e:
            print e

        # 동의
        concent = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@id='chk_purchase_agreement0']")))
        concent.click()
        while (not concent.is_selected()):
            print 'concent not checked'
            concent.click()

        # 결제하기
        placebutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//img[@id='btn_payment']")))
        placebutton.location_once_scrolled_into_view
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

    # close pop-up if exist
    closePopups(driver)

    # order
    order(driver)

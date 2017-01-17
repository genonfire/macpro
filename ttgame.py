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
HOMEPAGE = "http://www.ttgame.kr/member/login.html"
PS4PRO = "http://www.ttgame.kr/product/detail.html?product_no=1843&cate_no=203&display_group=1"
HEADSET = "http://www.ttgame.kr/product/detail.html?product_no=828&cate_no=244&display_group=1#none"
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
        userid = driver.find_element(By.NAME, 'member_id')
        # userid = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME,'member_id')))
        passwd = driver.find_element(By.NAME, 'member_passwd')
        button = driver.find_element_by_xpath("//img[@src='http://img.echosting.cafe24.com/skin/base_ko_KR/member/btn_login.gif']")
        userid.send_keys(USERID)
        passwd.send_keys(PASSWORD)
        button.click()

        # wait until logged-in
        logout = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/exec/front/Member/logout/']")))
    except NoSuchElementException, e:
        print e

def checkStock(driver, i):
    try:
        # outofstock = driver.find_element_by_xpath("//div[@class='xans-element- xans-product xans-product-detail']/div[@class='headingArea ']/span[@class='icon']/img[@class='icon_img']")
        buybutton = driver.find_element_by_xpath("//a[@class='first ']/img[@src='/web/upload/btn_buy_off.gif']")
        print "Go! Checkout~"
        return False
    except NoSuchElementException:
        print('[%d]%s' % (i, 'out of stock'))
        return True

def checkout(driver):
    cartbutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//img[@src='/web/upload/btn_buy_off.gif']")))
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

        # 적립금
        point = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//strong[@class='point']")))
        mypoint = int(point.get_attribute("innerHTML"))
        print "point: %d" % mypoint
        if (mypoint > 0):
            try:
                inputmile = driver.find_element_by_xpath("//input[@type='text'][@id='input_mile']")
                driver.execute_script("document.getElementById('input_mile').setAttribute('value', '')");
                inputmile.send_keys(mypoint)
                print 'using point: %d' % mypoint
            except NoSuchElementException, e:
                print e

        # 무통장입급
        bankradio = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@id='addr_paymethod0']")))
        bankradio.click()

        # 이름
        payer = driver.find_element(By.ID, 'pname')
        payer.send_keys(NAME)

        # 은행선택
        try:
            bankselect = driver.find_element_by_xpath("//select[@id='bankaccount']/option[@value='bank_81:118-910007-54304:(주)와이세븐스타일:KEB하나은행:www.hanabank.com']")
            bankselect.click()
        except NoSuchElementException, e:
            bankselect = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//select[@name='bankaccount']/option[@value='bank_20:1005-402-029120:(주)와이세븐스타일:우리은행:www.wooribank.com']")))
            bankselect.click()

        # 동의
        concent = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//input[@id='chk_purchase_agreement0']")))
        concent.click()
        while (not concent.is_selected()):
            print 'concent not checked'
            concent.click()

        # 결제하기
        placebutton = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//img[@id='btn_payment']")))
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

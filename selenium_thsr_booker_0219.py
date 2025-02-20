import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select            #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException   # handle exception
from ocr_component_0219 import get_captcha_code                      #取得驗證碼


options = webdriver.ChromeOptions()     #創立 Driver 物件所需的參數物件
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get("https://irs.thsrc.com.tw/IMINT/")                           #要爬的網站
time.sleep(2)                                                           #等待 2 秒
accept_cookie_button = driver.find_element(By.ID, "cookieAccpetBtn")    # 用 cookie 進入操作介面
accept_cookie_button.click()                                            #按左鍵


## 出發站(startStation), 抵達站(destStation), 出發日期(uk-select)
start_station_element = driver.find_element(By.NAME, "selectStartStation")          #選 "出發站" 的按鍵
Select(start_station_element).select_by_visible_text('台中')                        #填寫 "台中" 

start_station_element = driver.find_element(By.NAME, "selectDestinationStation")    #選 "抵達站" 的按鍵
Select(start_station_element).select_by_visible_text('台南')                        #填寫 "台南" 

start_station_element = driver.find_element(By.NAME, "toTimeTable")                 #選 "出發時間" 的按鍵
Select(start_station_element).select_by_visible_text('18:30')                       #填寫 "時間" 

## 選擇出發時間(start_date)
# start_date = "二月 21, 2025"
driver.find_element(
    By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()        #點開 "出發日期"
time.sleep(2)

start_date = 'February 21, 2025'                                                    #輸入日期
driver.find_element(
    By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']").click() 

while True:
    #驗證碼(captcha)
    captcha_img = driver.find_element(
        By.ID, 'BookingS1Form_homeCaptcha_passCode')
    captcha_img.screenshot('captcha.png')                           #截圖驗證碼
    captcha_code = get_captcha_code()
    captcha_input = driver.find_element(By.ID, 'securityCode')
    captcha_input.send_keys(captcha_code)                           #填寫正確的驗證文字
    time.sleep(2)

    #提交表單(submit)
    driver.find_element(By.ID, 'SubmitButton').click()
    time.sleep(5)

    # check validation is success or not
    try:
        driver.find_element(By.ID, 'divErrMSG')
        print("驗證碼錯誤")
        time.sleep(20)
    except NoSuchElementException:
        print("進到第二步驟")
        break



### 第二頁面 ###




time.sleep(20)      # 等待20秒，觀察結果
driver.quit()       # 關閉瀏覽器
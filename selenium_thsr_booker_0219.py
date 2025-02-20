import pprint
import time
import os                           #拿電腦的環境變數
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select            #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException   # handle exception
from ocr_component_0219 import get_captcha_code                 #從另一個程式檔案，取得驗證碼


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

## 選擇出發時間 (start_date)
# start_date = "二月 21, 2025"
driver.find_element(
    By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()        #點開 "出發日期"    # XPATH = 尋找特殊格式。 @ 是寫相對應的後台代碼
time.sleep(2)

start_date = 'February 21, 2025'                                                    #輸入日期
driver.find_element(
    By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']").click() 

while True:
    #驗證碼 (captcha)
    captcha_img = driver.find_element(
        By.ID, 'BookingS1Form_homeCaptcha_passCode')
    captcha_img.screenshot('captcha.png')                           #截圖驗證碼
    captcha_code = get_captcha_code()
    captcha_input = driver.find_element(By.ID, 'securityCode')
    captcha_input.send_keys(captcha_code)                           #填寫正確的驗證文字
    time.sleep(2)

    #提交表單 (submit)
    driver.find_element(By.ID, 'SubmitButton').click()
    time.sleep(5)

    # check validation is success or not
    try:
        time.sleep(5)
        driver.find_element(By.ID, 'BookingS2Form_TrainQueryDataViewPanel')
        print("驗證碼正確, 進到第二步驟")
        break
    except NoSuchElementException:
        print("驗證碼錯誤，重新驗證")



### 第二頁面 ###
trains_info = list()
trains = driver.find_element(
    By.CLASS_NAME, 'result-listing').find_elements(By.TAG_NAME, 'label')

for train in trains:
    info = train.find_element(By.CLASS_NAME, 'uk-radio')                #點選 "車次時間"

    trains_info.append(                                                 #整理成 dictionary ，為了顯示來做選擇
        {
            # info.grt ('屬性名稱')
            'depart_time': info.get_attribute('querydeparture'),        #出發時間
            'arrival_time': info.get_attribute('queryarrival'),         #抵達時間
            'duration': info.get_attribute('queryestimatedtime'),       #期間
            'train_code': info.get_attribute('querycode'),              #車次
            'radio_box': info,                                          #資訊
        }
    )

pprint.pprint(trains_info)                                              #列印出 "火車資訊" 的列表
## 選擇車次 (Choose train)
for idx, train in enumerate(trains_info):
    print(
        f"({idx}) - {train['train_code']}, \
        行駛時間={train['duration']} | \
        {train['depart_time']} -> \
        {train['arrival_time']}")                                       # \ 是為了能夠串接下一行的代碼
which_train = int(input("選擇您的車次。請輸入數字 0~9: "))         #輸入 "數字" 選擇要選的車次
trains_info[which_train]['radio_box'].click()                           #點選頁面的按鈕 

## 提交預定請求 (Submit booking requests)
driver.find_element(By.NAME, 'SubmitButton').click()
print("選擇車次完成, 進到第三步驟")



### 第三頁面 ###
## 檢查用戶預定訊息 (Check booking infomation for user)
print("確認訂票: ")
print(
    f"車次: {trains_info[which_train]['train_code']} | \
    行駛時間: {trains_info[which_train]['duration']} | \
    {trains_info[which_train]['depart_time']}   -> \
    {trains_info[which_train]['arrival_time']}"
)
print('您的車票共 ', driver.find_element(By.ID, 'TotalPrice').text, " 元")
driver.find_element(
    By.CLASS_NAME, 'ticket-summary').screenshot('thsr_summary.png')

## 輸入個人資料 (Enter personal detail)
input_personal_id = driver.find_element(By.ID, 'idNumber')         #找到後台代碼
personal_id = input("請輸入身分證字號: ")                           #輸入身分證字號
input_personal_id.send_keys(personal_id)                           #填入資訊

input_phone_number = driver.find_element(By.ID, 'mobilePhone')  
phone_number = input("請輸入手機號碼: ")                            #輸入手機號碼
input_phone_number.send_keys(phone_number)

input_email = driver.find_element(By.ID, 'email')               
email = input("請輸入Email: ")                                     #輸入 Email
input_email.send_keys(email)                                        


driver.find_element(By.NAME, 'agree').click()                   #接受使用者個資條款
driver.find_element(By.ID, 'isSubmit').click()                  #送出表單



time.sleep(20)      # 等待20秒，觀察結果
driver.quit()       # 關閉瀏覽器
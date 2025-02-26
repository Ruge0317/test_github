import pprint
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 下拉式選單使用
from selenium.common.exceptions import NoSuchElementException  # Handle exception

# Project modules
from d0219ocr_component import get_captcha_code
from d0224booking_info_extraction_flow import (
    ask_booking_infomation,
    ask_missing_infomation,
    convert_date_to_thsr_format
)

def create_driver():
    options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
    options.add_argument("--disable-blink-features=AutomationControlled")
    global driver
    driver = webdriver.Chrome(options=options)
    driver.get("https://irs.thsrc.com.tw/IMINT/")


def booking_with_info(start_station, dest_station, start_time, start_date):
    #
    # 第一個頁面
    #

    # Click accept cookie button
    accept_cookie_button = driver.find_element(By.ID, "cookieAccpetBtn")
    accept_cookie_button.click()

    # Choose Booking parameters: startStation, destStation, time
    start_station_element = driver.find_element(By.NAME, 'selectStartStation')
    Select(start_station_element).select_by_visible_text(start_station)

    dest_station_element = driver.find_element(
        By.NAME, 'selectDestinationStation')
    Select(dest_station_element).select_by_visible_text(dest_station)

    start_time_element = driver.find_element(By.NAME, 'toTimeTable')
    Select(start_time_element).select_by_visible_text(start_time)

    # Choose Booking parameters: date
    driver.find_element(
        By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()
    
    # Choose Booking date: 包含今天與其他天
    driver.find_element(
        By.XPATH,
        f"//span[(@class='flatpickr-day' or @class='flatpickr-day today selected') and @aria-label='{start_date}']"
    ).click()

    while True:
        # captcha
        captcha_img = driver.find_element(
            By.ID, 'BookingS1Form_homeCaptcha_passCode')
        captcha_img.screenshot('captcha.png')
        captcha_code = get_captcha_code()
        captcha_input = driver.find_element(By.ID, 'securityCode')
        captcha_input.send_keys(captcha_code)
        time.sleep(2)

        # submit
        driver.find_element(By.ID, 'SubmitButton').click()

        # check validation is success or not
        try:
            time.sleep(5)
            driver.find_element(By.ID, 'BookingS2Form_TrainQueryDataViewPanel')
            print("驗證碼正確, 進到第二步驟")
            break
        except NoSuchElementException:
            print("驗證碼錯誤，重新驗證")

    #
    # 第二個頁面
    #
    trains_info = list()
    trains = driver.find_element(
        By.CLASS_NAME, 'result-listing').find_elements(By.TAG_NAME, 'label')
    for train in trains:
        info = train.find_element(By.CLASS_NAME, 'uk-radio')
        trains_info.append(
            {
                # info.get('屬性名稱')
                'depart_time': info.get_attribute('querydeparture'),
                'arrival_time': info.get_attribute('queryarrival'),
                'duration': info.get_attribute('queryestimatedtime'),
                'train_code': info.get_attribute('querycode'),
                'radio_box': info,
            }
        )
    # Show train info & Choose train
    for idx, train in enumerate(trains_info):
        print(
            f"({idx}) - {train['train_code']}, \
            行駛時間={train['duration']} | \
            {train['depart_time']} -> \
            {train['arrival_time']}"
        )

    return trains_info


def select_train_and_submit_booking(trains_info, which_train=None):

    if which_train is None:
        # 如果沒有選擇車次，則由使用者選擇(一般程式的執行流程，採用CMD輸入)
        which_train = int(input("選擇您的車次。請輸入數字 0~9: "))
    trains_info[which_train]['radio_box'].click()

    # Submit booking requests
    driver.find_element(By.NAME, 'SubmitButton').click()
    print("選擇車次完成, 進到第三步驟")

    #
    # 第三個頁面
    #
    # Check booking infomation for user
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

    # Enter personal detail
    input_personal_id = driver.find_element(By.ID, 'idNumber')

    # personal_id = input("請輸入身分證字號:\n")
    personal_id = os.getenv('PERSONAL_ID')  # 從環境變數拿
    input_personal_id.send_keys(personal_id)

    input_phone_number = driver.find_element(By.ID, 'mobilePhone')
    # phone_number = input("請輸入手機號碼:\n")
    phone_number = os.getenv('PERSONAL_PHONE_NUMBER')
    input_phone_number.send_keys(phone_number)

    input_email = driver.find_element(By.ID, 'email')
    # email = input("請輸入Email:\n")
    email = os.getenv('PERSONAL_EMAIL')
    input_email.send_keys(email)

    # Final Check
    driver.find_element(By.NAME, 'agree').click()  # 接受使用者個資條款
    driver.find_element(By.ID, 'isSubmit').click()  # 送出表單

    # Save booking result
    screenshot_filename = 'thsr_booking_result.png'
    driver.find_element(
        By.CLASS_NAME, 'ticket-summary').screenshot(screenshot_filename)
    print("訂票完成!")

    return screenshot_filename


if __name__ == "__main__":

    # Booking parameters
    start_station = '台中'
    dest_station = '板橋'
    start_time = '18:00'
    start_date = '二月 25, 2025'

    create_driver()

    # Step 1
    booking_info = ask_booking_infomation()

    # Step 2
    booking_info = ask_missing_infomation(booking_info)

    # Step 3: 調整日期格式以便爬蟲使用, ex: '2025/02/25' -> '二月 25, 2025'
    booking_info = convert_date_to_thsr_format(booking_info)

    # Step 4
    trains_info = booking_with_info(
        start_station=booking_info['出發站'],
        dest_station=booking_info['到達站'],
        start_time=booking_info['出發時間'],
        start_date=booking_info['出發日期'])
    
    # Step 5
    select_train_and_submit_booking(trains_info)


    time.sleep(10)
    driver.quit()

    
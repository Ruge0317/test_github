from d0220chatgpt_sample import chat_with_chatgpt
from datetime import date
import json, re



standard_format = {
    "出發站": "出發站名",
    "到達站": "到達站名",
    "出發日期": "YYYY/MM/DD",
    "出發時間": "H:S"
}
today = date.today().strftime("%Y/%m/%d")  # 取得今天日期


def extract_dict_from_string(input_string):
    # 定義正則表達式來匹配字典內容
    pattern = r"\{\s*'[^']*':\s*'[^']*'(?:,\s*'[^']*':\s*'[^']*')*\s*\}"
    match = re.search(pattern, input_string)

    if match:
        dict_string = match.group(0)
        # 將單引號替換為雙引號以便於 json.loads 解析
        dict_string = dict_string.replace("'", "\"")
        print("After regular expression ....: ", dict_string)
        return json.loads(dict_string)
    else:
        raise ValueError("Information Extraction Failed.")


def ask_booking_infomation():
    print("Ask booking information")

    user_response = input(
        "請輸入你的高鐵訂位資訊，包含：出發站、到達站、出發日期、出發時間: ")
    system_prompt = f"""
    我想要從回話取得訂票資訊，包含：出發站、到達站、出發日期、出發時間。
    今天是 {today}，請把資料整理成python dictionary格式，例如：{standard_format}，
    不知道就填空字串，且回傳不包含其他內容。
    """           #"且回傳不包含其他內容" = 為了不讓亂回話，一定要加
    booking_info = chat_with_chatgpt(user_response, system_prompt)
    return json.loads(booking_info.replace("'", "\""))


def ask_missing_infomation(booking_info):  # Slot filling
    print("Ask missing information")
    missing_slots = [key for key, value in booking_info.items() if not value]
    if not missing_slots:
        print("All slots are filled")
        return booking_info
    else:
        user_response = input(
            f"請補充你的高鐵訂位資訊，包含：{', '.join(missing_slots)}: ")

        system_prompt = f"""
        我想要從回話取得訂票資訊，包含：{', '.join(missing_slots)}。           
        並與 {booking_info} 合併，今天是 {today} 。
        請把資料整理成python dictionary格式，例如：{standard_format}，
        不知道就填空字串，且回傳不包含其他內容。。
        """


        booking_info = chat_with_chatgpt(user_response, system_prompt)      #使用 chatgpt 來回話
        return json.loads(booking_info.replace("'", "\""))                  #把字串改成 dictionary ，把 單引號(')，改成雙引號(") 用 \ 來跳脫字元


def convert_date_to_thsr_format(booking_info):
    map_number_to_chinese_word = {
        "01": "January", "02": "February", "03": "March", "04": "April",
        "05": "May", "06": "June", "07": "July", "08": "August",
        "09": "September", "10": "October", "11": "November", "12": "December"
    }
    Year, Month, Day = booking_info['出發日期'].split('/')
    booking_info['出發日期'] = f"{map_number_to_chinese_word[Month]} {Day}, {Year}"
    print("格式轉換後......")
    print(booking_info)
    return booking_info


if __name__ == '__main__':
    # Step 1
    booking_info = ask_booking_infomation()

    # Step 2
    booking_info = ask_missing_infomation(booking_info)

    # Step 3：調整日期格式以便爬蟲使用, ex: '2025/02/25' -> '二月 25, 2025'
    booking_info = convert_date_to_thsr_format(booking_info)
    

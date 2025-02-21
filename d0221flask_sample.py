from flask import Flask
from d0220chatgpt_sample import chat_with_chatgpt

"""
執行 flask App, 要在 "終端機(terminal)" 啟用要打 flask --app d0221flask_sample run
會在你的本地電腦運行: http://127.0.0.1:5000


"""


app = Flask(__name__)


@app.route("/")                     # route 會觸發 flask 的功能
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/home/<user_message>")                 #若要使用其他的網頁，要在網址上打上 "/home(名稱)"   # 每次增加要用 "/" 隔開
def hello_home(user_message):                      #可以在網址後面 "/" 再做詢問
    chatgpt_response = chat_with_chatgpt(
        user_message=user_message,                  
        system_prompt="你是一位後端管理員，有前端使用者會呼叫你。"
    )
    return chatgpt_response



## 如果要使用 python xxx.py 執行
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template
from markupsafe import escape
from d0220chatgpt_sample import chat_with_chatgpt

"""
執行 flask App, 要在 "終端機(terminal)" 啟用要打 flask --app d0221flask_sample run
會在你的本地電腦運行: http://127.0.0.1:5000


"""


app = Flask(__name__)


@app.route("/")                     # route 會觸發 flask 的功能
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test/<int:user_id>/")                     
def hello_user(user_id):
    return f"<p>Hello, USER-{user_id}, world!</p>"

# 路徑
@app.route("/test/<path:subpath>/")                     
def hello_path(subpath):
    return f"<p>Hello, PATH-{escape(subpath)}, world!</p>"


@app.route("/home/<user_message>/")                 #若要使用其他的網頁，要在網址上打上 "/home(名稱)"   # 每次增加要用 "/" 隔開
def hello_home(user_message):                      #可以在網址後面 "/" 再做詢問
    chatgpt_response = chat_with_chatgpt(
        user_message=user_message,                  
        system_prompt="你是一位後端管理員，有前端使用者會呼叫你。"
    )
    return chatgpt_response


@app.route("/sample/")                     
def show_html_sample():
    return render_template(
        'sample.html', 
        name="tony",
        numbers=[11, 22, 33, 44, 55],
        pairs=[('A', 1), ('B', 2), ('C', 3)],
        dict_data={'A': 1, 'B': 2, 'C': 3}
    )


## 如果要使用 python xxx.py 執行
if __name__ == '__main__':
    app.run(debug=True)
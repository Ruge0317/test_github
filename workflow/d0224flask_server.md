1. 執行你的Flask App, 使其運行在你的本地電腦(http://127.0.0.1:5000)
    
    * 一般模式
        > flask --app <你的應用程式檔案名稱, 不用.py> run

    * Debug 模式
        > flask --app <你的應用程式檔案名稱, 不用.py> run --debug 

    * Python 執行: 設定會由程式碼提供
        > python <你的應用程式檔案名稱>

2. 使用 route 裝飾器為網站分頁引流，不同頁面由不同function定義其內容

3. 使用 render_templates 獲得以下好處:
    * 切割前後端工作
    * 程式碼會比較簡潔
    * 利用 Jinja 渲染模板傳遞變數


* CMD 按 Ctrl+c 可以關閉執行中的程序
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage  #傳回LINE官方後台的資料格式
)
from linebot.v3.webhooks import (
    MessageEvent,  #傳過來的方法
    TextMessageContent  #使用者傳過來的資料格式
)
import os
import sys


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
#1.先到Line的Developer Console,把Channel Secert Key 跟 Channel Access Token複製起來
#2.把這兩個密文,存到環境變數內:搜尋<環境變數>,新增兩個環境變數,並且把值貼上去
#3.按下確定儲存,要記得你的變數名稱,這些資訊只會存在你當前使用的電腦裡
#4.透過以下程式碼取得環境變數所儲存的對應數值

channel_secret = os.getenv('LINEBOT_SECRET_KEY', None)
channel_access_token = os.getenv('LINEBOT_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINEBOT_SECRET_KEY as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINEBOT_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)
configuration = Configuration(access_token=channel_access_token)

#設計一個callback的路由,提供給LINE官方後台去呼叫(也就是所謂的webhook server)
#因為官方會把使用者傳輸的訊息轉傳給webhook server,所以會使用RESTful API 的POST方法
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#根據不同事件(event),用不同的方式回應,message event代表使用者單純傳訊息的事件
#textmessagecontent代表使用者傳說的訊息內容是文字,符合兩個條件的事件,會handle_message所處理
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()
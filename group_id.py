from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINEのチャネルアクセストークンとチャネルシークレットを設定
line_bot_api = LineBotApi('ytfeoRwOS4vGXVa5OX2lEczjlF0LrLEXmVPRvTRKD2s4kY9uO7L76kVKjoCrhgFRKo/tuGRui0RlrPPLx1+tHynWbkqhniyYTJ+suSvdAcVa0iWCtbsruCYD18QHIanFoNV0+s3jAm65sbzgOjYvwwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('92a52a3896b35276e6f89fb8b3286a2f')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージイベントが発生したときにグループIDを取得
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # グループIDの取得
    if event.source.type == 'group':
        group_id = event.source.group_id
        print(f"Group ID: {group_id}")
        
        # グループに返信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Your Group ID is: {group_id}"))

if __name__ == "__main__":
    app.run(port=5000)
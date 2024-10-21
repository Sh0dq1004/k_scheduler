from linebot import LineBotApi
from linebot.models import TextSendMessage

def sending(message):
    # チャネルアクセストークンを設定
    line_bot_api = LineBotApi('ytfeoRwOS4vGXVa5OX2lEczjlF0LrLEXmVPRvTRKD2s4kY9uO7L76kVKjoCrhgFRKo/tuGRui0RlrPPLx1+tHynWbkqhniyYTJ+suSvdAcVa0iWCtbsruCYD18QHIanFoNV0+s3jAm65sbzgOjYvwwdB04t89/1O/w1cDnyilFU=')
    # ユーザーIDまたはグループIDにメッセージを送信
    user_id='Cd7d1aa1cee1550bbc34b10183bb68888'
    line_bot_api.push_message(user_id, TextSendMessage(text=message))
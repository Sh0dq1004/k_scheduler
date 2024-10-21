import line
from gform import google_form_launcher

if __name__=="__main__":
    url = google_form_launcher(test=False)
    text=f"【お知らせ】\n今月もあと少し！皆さんマッスルハッスルしてますか？来月分のトレーニングの日付を以下のフォームに入力お願いします！\n{url}"
    line.sending(message=text)

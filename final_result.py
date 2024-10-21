import line
from gform import get_response

if __name__=="__main__":
    resultDict = get_response()
    text=f"【お知らせ】\n来月の予定が決まりました！\n"
    for i in resultDict:
        if len(resultDict[i]) >= 3:
            text+=f"{i}\n"
    text+="今月もマッスル目指して頑張ろう！"
    line.sending(message=text)
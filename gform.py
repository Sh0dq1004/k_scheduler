from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime as dt

def init_setting():
    # サービスアカウントのJSONキーのパス
    SERVICE_ACCOUNT_FILE = 'service_account.json'
    # 認証スコープを指定
    SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/drive']
    # 認証情報をサービスアカウントから取得
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # Google Forms APIのサービスを作成
    service = build('forms', 'v1', credentials=creds)
    return service

def google_form_launcher(test=True):
    service=init_setting()
    if test==True:
        if input("Create a new form. Y/N ") == "Y":
            form_id=create_new_form(service)
        else:
            with open(file="form_id.txt",mode="r",encoding="utf-8") as f:
                form_id=f.read()
    else:
        form_id=create_new_form(service)
    # 質問をフォームに追加
    create_questions(service,form_id,training_days())

    print(f"https://docs.google.com/forms/d/{form_id}/edit")
    with open(file="form_id.txt",mode="w",encoding="utf-8") as f:
        f.write(form_id)

    return f"https://docs.google.com/forms/d/{form_id}/edit"

def create_new_form(service):
    cMonth=dt.datetime.now().month
    if cMonth==12:
        new_form = {"info": {"title": "1月のトレーニング予定日 アンケート"}}
    else:
        new_form = {"info": {"title": f"{cMonth+1}月のトレーニング予定日 アンケート"}}
    # フォームを作成
    form = service.forms().create(body=new_form).execute()
    # 作成されたフォームのIDを返す
    return form['formId']

def create_questions(service, form_id, options):
    question1 = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": "以下の時間の中で可能な日をすべで入力してください。",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "CHECKBOX",
                                    "options": [{"value": i} for i in options]
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 0  # フォーム内の位置
                    }
                }
            }
        ]
    }
    question2 = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": "名前を選択してください",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": i} for i in ["かい","頌太","関山","そら","たいが"]]
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 0  # フォーム内の位置
                    }
                }
            }
        ]
    }
    service.forms().batchUpdate(formId=form_id, body=question1).execute()
    service.forms().batchUpdate(formId=form_id, body=question2).execute()

def training_days():
    cDatetime=dt.datetime.now()
    if cDatetime.month==12:
        week_day=dt.date(cDatetime.year,1,1).weekday() #0=Monday
    else:
        week_day=dt.date(cDatetime.year,cDatetime.month+1,1).weekday() #0=Monday

    traningDays=[]
    if cDatetime.month+1 == 2:
        if cDatetime.year%4==0 and (cDatetime.year%100!=0 or cDatetime.year%400==0):
            traningDays.extend([i for i in range(2-week_day,29,7) if i>0])
            traningDays.extend([i for i in range(4-week_day,29,7) if i>0])
        else:
            traningDays.extend([i for i in range(2-week_day,28,7) if i>0])
            traningDays.extend([i for i in range(4-week_day,28,7) if i>0])
    elif cDatetime.month+1 in [4,6,9,11]:
        traningDays.extend([i for i in range(2-week_day,30,7) if i>0])
        traningDays.extend([i for i in range(4-week_day,30,7) if i>0])
    else:
        traningDays.extend([i for i in range(2-week_day,31,7) if i>0])
        traningDays.extend([i for i in range(4-week_day,31,7) if i>0])

    traningDays.sort()
    if cDatetime.month==12:
        return [f"1/{i} 18:40~" for i in traningDays]
    else:
        return [f"{cDatetime.month+1}/{i} 18:40~" for i in traningDays]

def get_response():
    resultDict={}
    service=init_setting()
    with open(file="form_id.txt",mode="r",encoding="utf-8") as f:
        form_id=f.read()
    res = service.forms().responses().list(formId=form_id).execute()
    questionIds=list(res["responses"][0]["answers"])
    for i in res["responses"]:
        for j in i["answers"][questionIds[1]]["textAnswers"]["answers"]:
            if j["value"] not in resultDict:
                resultDict[j["value"]]=[i["answers"][questionIds[0]]["textAnswers"]["answers"][0]["value"]]
            else:
                resultDict[j["value"]].append(i["answers"][questionIds[0]]["textAnswers"]["answers"][0]["value"])
    return resultDict

if __name__=="__main__":
    #google_form_launcher()
    get_response()
import json
import datetime
import openai
from function import initialize, stream

openai.api_key = initialize.openAI_KEY()

class character:
    #hunger: 空腹度(0-100)，drowsiness: 眠気(0-100)
    def __init__(self, persona, hunger, drowsiness, place, clothes):
        #\nSchedule should be accomplished properly.
        self.striatum = [{"role": "system", "content": str(persona) + "\nDecide your action and output json style. Pay attention to these notices.\n*Hunger and drowsiness should be less than 80."}]
        self.language = [{"role": "system", "content": str(persona) + "\nGenerate the character's text based on given object and function."}]
        self.status = {}
        self.status["hunger"] = hunger
        self.status["drowsiness"] = drowsiness
        self.status["place"] = place
        self.status["clothes"] = clothes
        self.schedule = {"8:00": "school"}

    #時間経過によるステータスの変化を計算する．timeの単位は分
    def status_flow_awake(self, time):
        #6時間で80上昇
        self.status["hunger"] += time * 80 / 360
        #16時間で80上昇
        self.status["drowsiness"] += time * 80 / 960
        
    
    def status_flow_asleep(self, time):
        #8時間で30上昇
        self.status["hunger"] += time * 30 / 480
        #8時間で80減少
        self.status["drowsiness"] = max(0, self.status["drowsiness"] - time * 80 / 480)
    
    def status_change(self, key, value):
        self.status[key] = value

    #現在地点にあるオブジェクトを検索する
    #directory: オブジェクトデータが格納されたディレクトリのパス
    def get_object(self, directory):
        path = directory + "/" + str(self.status["place"]) + ".txt"
        return stream.read_file(path)

    #選択されたオブジェクトがもつ機能を検索する
    #directory: オブジェクトデータが格納されたディレクトリのパス
    def get_function(self, directory, object):
        path = directory + "/" + str(self.status["place"]) + "/" + object + ".txt"
        return stream.read_file(path)
    
    #オブジェクトを選ばせる
    #directory: オブジェクトデータが格納されたディレクトリのパス
    def choose_object(self, directory, date):
        txt_object = self.get_object(directory)
        prompt = "date: " + str(date) + "\nyour status: " + str(self.status) + "\nyour schedule: " + str(self.schedule) + "\nYou can access objects below. Choose one object. Permitted key is 'object' only.\n" + str(txt_object)
        self.striatum.append({"role": "user", "content": prompt})
        res = openai.ChatCompletion.create(model = "gpt-4", messages = self.striatum)
        ans = res["choices"][0]["message"]["content"].strip()
        self.striatum.append({"role": "assistant", "content": ans})
        return ans

    #オブジェクトの機能を選ばせる
    def choose_function(self, directory, object):
        txt_function = self.get_function(directory, object)
        prompt = "You can act following in function below. Choose one function and decide arguments. Permitted keys are 'function' and some defined arguments.\n" + txt_function
        self.striatum.append({"role": "user", "content": prompt})
        res = openai.ChatCompletion.create(model = "gpt-4", messages = self.striatum)
        ans = res["choices"][0]["message"]["content"].strip()
        self.striatum.append({"role": "assistant", "content": ans})
        return ans
    
    def generate_text(self, object, function):
        prompt = object + "\n" + function + "\ndate: " + str(date) + "\nyour status: " + str(self.status) + "\nyour schedule: " + str(self.schedule)
        self.language.append({"role": "user", "content": prompt})
        res = openai.ChatCompletion.create(model = "gpt-4", messages = self.language)
        ans = res["choices"][0]["message"]["content"].strip()
        self.language.append({"role": "assistant", "content": ans})
        return ans

    def tempfunc(self):
        self.language.append({"role": "assistant", "content": "You came back from school."})
        self.striatum.append({"role": "assistant", "content": "You came back from school."})


#システム内時間
date = datetime.datetime(2023, 11, 17, 7, 00)
#ほのかの初期化
persona_honoka = stream.read_file("./data/honoka_free/honoka_person_free_personality.txt")
honoka = character(persona_honoka, 75, 5, "house", "nightgown")

#オブジェクトデータが格納されたディレクトリの指定
directory = "./data/object"

#ログの初期化
log = stream.log("./output/log.txt", "simulation.py")
log.add_line()

while True:
    print(date)
    print(honoka.status)
    print(honoka.schedule)
    log.add(str(date))
    log.add(str(honoka.status))
    log.add(str(honoka.schedule))
    #今いる場所にあるオブジェクト読み込み
    ans1 = honoka.choose_object(directory, date)
    print(ans1)
    log.add(ans1)

    #選択されたオブジェクト読み込み
    object = json.loads(ans1)["object"]
    ans2 = honoka.choose_function(directory, object)
    log.add(ans2)
    print(ans2)
    ans = honoka.generate_text(ans1, ans2)
    print(ans)
    log.add(ans)

    #functionと使用時間(min)の抽出
    temp = json.loads(ans2)
    function = temp["function"]

    if function == "exit":
        log.add_line()
        honoka.tempfunc()
        log.add("Honoka came back from school.")
        honoka.status_flow_awake(570)
        td = datetime.timedelta(minutes = 570)
        date += td
        continue

    #ステータスに干渉するfunctionの処理
    if function == "dress":
        honoka.status_change("clothes", temp["changeclothes_"])
    if function == "cook":
        former = honoka.status["drowsiness"]
        honoka.status_change("hunger", max(0, honoka.status["drowsiness"] - 80))
    
    min = int(temp["time_"])
    #時間周りの処理
    if function == "sleep":
        honoka.status_flow_asleep(min)
    else:
        honoka.status_flow_awake(min)
    td = datetime.timedelta(minutes = min)
    date += td

    log.add_line()

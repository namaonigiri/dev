#感情評価による発話の取捨選択
import random
import openai
from function import stream, initialize

def input_infomation():
    internal_state = input("internal state: ")
    external_situation = input("external_situation: ")
    infomation = "{'internal_state': '"+ internal_state + "', 'external_situation': '" + external_situation + "'}"
    return infomation

def make_inst(posi, nega):
    return "A positive value indicates " + posi + ", and a negative value indicates "+ nega + ". The higher the absolute value, the greater the emotion."
#openai.api_key = input("APIのシークレットキー:")
openai.api_key = initialize.openAI_KEY()

#人格データの読み込み
f = open("./data/honoka_free/honoka_person_free_personality.txt")
txt_chara = f.read()
#former: "You are a scenario writer. Think of a character below.\n" + txt_chara + "\nRate the magnitude of her emotion based on Plutchik's wheel of emotions in the condition on a scale from -100 to 100. Think of four items below and output with json style.\n*x1: " + make_inst("joy", "sadness") + "\n*x2: "+ make_inst("anticipation", "surprise") + "\n*x3: " + make_inst("anger", "fear")
prompt = """You are a scenario writer. Think of a character below.
""" + txt_chara + """
Rate the magnitude of her emotion based on Plutchik's wheel of emotions in the condition on a scale from -100 to 100. Think of four items below and output with json style.
x1: """ + make_inst("joy", "sadness") + """
x2: """ + make_inst("anticipation", "surprise") + """
x3: """ + make_inst("anger", "fear") + """
x4: """ + make_inst("trust", "disgust")

honoka = [{"role": "system", "content": prompt}]

log = stream.log("./output/log.txt", "emotion.py")
log.add_line()

while True:
    #入力
    info = input_infomation()
    #ログとり
    log.add(info)

    #プロンプトいじり
    prompt = info
    honoka.append({"role": "user", "content": prompt})

    #生成
    res = openai.ChatCompletion.create(model="gpt-4", messages=honoka)
    ans = res["choices"][0]["message"]["content"].strip()

    #出力
    print(ans)
    stream.printline()

    #ログとり
    log.add(ans)
    log.add_line()

    #user消去
    honoka.pop(1)
import re
import csv
import json
import random
import openai
from function import stream


def make_inst(posi, nega):
    return "Positive value indicates " + posi + ", and negative value indicates "+ nega + ". The higher its absolute value, the greater the emotion."

def make_prompt(name, persona_path, number):
    persona_txt = stream.read_file(persona_path)
    if number == 0:
        prompt = persona_txt + """\n
        Rate the magnitude of """ + name + """'s emotion based on Plutchik's wheel of emotions in the situation on a scale from -100 to 100. Think of four item below and output with json style.
        x1: """ + make_inst("joy", "sadness") + """
        x2: """ + make_inst("anticipation", "surprise") + """
        x3: """ + make_inst("anger", "fear") + """
        x4: """ + make_inst("trust", "disgust") + """
        example: {"x1": 82, "x2": -38, "x3": 0, "x4": 98}
        """
    
    elif number == 1:
        prompt = persona_txt + """\n
        Rate the magnitude of """ + name + """'s emotion based on Plutchik's wheel of emotions in the situation on a scale from 0 to 100. Think of eight items below and output with json style.
        *joy
        *anticipation
        *anger
        *trust
        *sadness
        *surprise
        *fear
        *disgust
        example: '{"joy": 80, "anticipation": 60, "anger": 0, "trust": 70, "sadness": 0, "surprise": 50, "fear": 10, "disgust": 0}'
        """

    elif number == 2:
        prompt = persona_txt + """\n
        Rate the magnitude of """ + name + """'s emotion based on Ekman's theory in the situation on a scale from 0 to 100. Think of six items below and output with json style.
        *happiness
        *sadness
        *disgust
        *anger
        *fear
        *surprise
        example: '{"happiness": 70,  "sadness": 0, "disgust": 0, "anger": 0, "fear": 10, "surprise": 50}'
        """
    
    return prompt

openai.api_key = initialize.openAI_KEY()


#パスの指定
path_persona = "./data/hinata/hinata.txt"
path_state = "./data/honoka/internal_state.txt" #現在の知覚によらない，当人の状態・動作　基本となる感情を定める
path_log = "./output/log.txt"
path_output = "./output/state2vec.csv"


#ログの初期化
log = stream.log(path_log, "test.py")
log.add_line()


#人格データの読み込み
#"state or action" represents current state or action of the character. "eyesight" represents the place the character is. 
txt_persona = stream.read_file(path_persona)
prompt = make_prompt("Hinata", path_persona, 1)
character = [{"role": "system", "content": prompt}]

#感情を評価したいデータの読み込み
states = stream.read_file(path_state)
states = states.split("\n")

output = []
flag = 0

#"""
for x in states:
    #生成
    character.append({"role": "user", "content": x})
    res = openai.ChatCompletion.create(model="gpt-4-1106-preview", temperature = 0, messages = character, response_format = {"type": "json_object"})
    ans = res["choices"][0]["message"]["content"].strip()
    temp = re.findall(r'\{.*\}', ans.replace("\n", ""))
    #出力
    print(x)
    print(ans)
    stream.printline()

    #ログとり
    log.add(x)
    log.add(ans)
    log.add_line()

    #ベクトル抽出
    vec = json.loads(temp[-1]).values()
    #output.append(vec)

    #user消去
    character.pop(1)

    if flag == 0:
        with open(path_output, "w") as f:
            writer = csv.writer(f)
            writer.writerow(vec)
            flag = 1
    
    else:
        with open(path_output, "a") as f:
            writer = csv.writer(f)
            writer.writerow(vec)



"""
with open(path_output, "w") as f:
    writer = csv.writer(f)
    for x in output:
        writer.writerow(x)
"""
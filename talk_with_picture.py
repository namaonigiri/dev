#画像を感情に変換
#mainの先頭に入力すべき変数あり
import re
import csv
import json
import base64
import requests
from function import stream, process, initialize

api_key = initialize.openAI_KEY()


#ベクトルのインストラクション
def make_inst(posi, nega):
    return "Positive value indicates " + nega + ", and Negative value indicates "+ posi + ". The higher its absolute value, the greater the emotion."

#function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


#function to get responce of ChatGPT
def get_response(model, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0
        
    }

    #ChatGPTにrequest
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    output = response.json()

    return output

def make_prompt(name, persona_path, number):
    persona_txt = stream.read_file(persona_path)
    if number == 0:
        prompt = persona_txt + """\n
        Rate the magnitude of """ + name + """'s emotion based on Plutchik's wheel of emotions in the situation on a scale from -100 to 100. Think of four items below and output with json style.
        x1: """ + make_inst("joy", "sadness") + """
        x2: """ + make_inst("anticipation", "surprise") + """
        x3: """ + make_inst("anger", "fear") + """
        x4: """ + make_inst("trust", "disgust") + """
        example: {"x1": 82, "x2": -38, "x3": 0, "x4": 98}"""
    
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


def main():
    #入力すべき事項
    n = 1 #画像の数
    m = 0 #終わった数
    name = "Honoka"
    persona_path = "./data/honoka/honoka.txt"#ペルソナテキストのパス
    picture_path = "./data/sample_scene/scene3/3.jpg"#写真path
    log_path = "./output/log.txt"#ログのパス
    output_path = "./output/log.txt"

    #ログの初期化
    log = stream.log(log_path, "talk_with_picture.py")
    log.add_line()
    persona_txt = stream.read_file(persona_path)
    messages = [{"role": "system", "content": persona_txt}]

    for i in range(m, n):
        #写真をデコード
        image = encode_image(picture_path)

        #userプロンプトをアペンド
        input = {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}]}
        messages.append(input)
        messages.append({"role": "user", "content": "This is your view and User is near to you. You want to talk about this scenery."})

        res = get_response("gpt-4-vision-preview", messages)
        ans = res["choices"][0]["message"]["content"]
        print(ans)

        stream.printline()

        #ログとり
        log.add(str(ans))
        log.add_line()

        messages.pop(1)
        messages.pop(1)

if __name__ == "__main__":
    main()

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
    n = 3 #画像の数
    m = 0 #終わった数
    name = "Honoka"
    persona_path = "./data/honoka/honoka.txt"#ペルソナテキストのパス
    picture_path = "./data/sample_scene/scene3"#写真のディレクトリ
    log_path = "./output/log.txt"#ログのパス
    output_path = "./output/pic2vec_scene3.csv"

    #ログの初期化
    log = stream.log(log_path, "pic2vec2.py")
    log.add_line()
    prompt = make_prompt(name, persona_path, 1)
    messages = [{"role": "system", "content": prompt}]

    for i in range(m, n):
        #写真をデコード
        image_path = f"{picture_path}/{i+1}.jpg"
        image = encode_image(image_path)

        #userプロンプトをアペンド
        input = {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}]}
        messages.append(input)

        res = get_response("gpt-4-vision-preview", messages)
        ans = res["choices"][0]["message"]["content"]
        temp = re.findall(r'\{.*\}', ans.replace("\n", ""))
        print(len(messages))

        print(f"pic{i+1}")
        print(temp)
        stream.printline()
        #tempをjsonに変換し，valueを取得
        vec = json.loads(temp[-1]).values()

        #ログとり
        log.add(f"pic{i+1}")
        log.add(str(temp))
        log.add_line()

        messages.pop(1)

        #途中で不具合が起きてもいいように逐次出力
        if i == 0:
            with open(output_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(vec)
        else:
            with open(output_path, "a") as f:
                writer = csv.writer(f)
                writer.writerow(vec)

if __name__ == "__main__":
    main()

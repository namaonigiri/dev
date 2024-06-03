import openai
from function import stream

openai.api_key = initialize.openAI_KEY()

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

persona_path = "./data/honoka/honoka.txt"
question_path = "./data/honoka/internal_state.txt"
answer_path = "./output/honoka_p.txt"

prompt = make_prompt("Honoka", persona_path, 1)
question_txt = stream.read_file(question_path)
answer_txt = stream.read_file(answer_path)

conv = []
conv.append({"role": "system", "content": prompt})
conv.append({"role": "user", "content": question_txt})
conv.append({"role": "assistant", "content": answer_txt})
while True:
    prompt = input(">> ")
    conv.append({"role": "user", "content": prompt})
    res = openai.ChatCompletion.create(model="gpt-4-1106-preview", messages = conv)
    ans = res["choices"][0]["message"]["content"].strip()

    print(ans)
    conv.append({"role": "user", "content": "ans"})
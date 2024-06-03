import csv
import openai
from function import stream

openai.api_key = initialize.openAI_KEY()

def read_csv(path):
    ans = []
    with open(path) as f:
        for x in csv.reader(f):
            temp = []
            for y in x:
                temp.append(int(y))
            ans.append(temp)
    
    return ans

def main():
    state_path = "./data/honoka/internal_state.txt"
    vector_path = "./output/honoka/state2vec/state2vec.csv"
    path_log = "./output/log.txt"
    init_prompt = """Concerning a specified character, I gained evaluations on emotions in a given situation on a scale from 0 to 100.

    Guess the character's profile and write instructions for ChatGPT to play the character in Japanese. The more accurate your answers, the higher the prize you will receive!

    Here is descriptions of emotions:
    emotion based on Plutchik's wheel of emotions in the situation on a scale from 0 to 100. There are eight items below.
    *x1: joy
    *x2: anticipation
    *x3: anger
    *x4: trust
    *x5: sadness
    *x6: surprise
    *x7: fear
    *x8: disgust
    """

    log = stream.log(path_log, "gyaku.py")
    log.add_line()

    conv = [{"role": "system", "content": init_prompt}]

    vecs = read_csv(vector_path)
    state_txt = stream.read_file(state_path)
    states = state_txt.split("\n")

    l = []
    for i in range(len(vecs)):
        st = "{"
        for j in range(len(vecs[0])):
            st = st + f"'x{j + 1}': " + str(vecs[i][j]) + ","
        st = st + "}"
        l.append(st)
    
    user_prompt = ""
    for i in range(len(l)):
        user_prompt = user_prompt + f"state{i + 1}: " + states[i] + "\n" + f"emotion{i + 1}: " + l[i] + "\n" 

    conv.append({"role": "user", "content": user_prompt})
    res = openai.ChatCompletion.create(model="gpt-4-1106-preview", messages = conv)
    ans = res["choices"][0]["message"]["content"].strip()
    print(ans)

    log.add(ans)

if __name__ == "__main__":
    main()
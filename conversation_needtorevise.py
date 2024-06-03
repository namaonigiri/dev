#複数のChatGPTエージェントで会話するやつ
#前の発話の話題に対する反応度のようなものを計算できる関数が欲しい！
import math
import random
import openai
from function import initialize

#openai.api_key = input("APIのシークレットキー:")
openai.api_key = initialize.openAI_KEY()

#次に誰が喋るか決定する関数
def darts(p):
    r = random.random()
    sum = 0

    for i in range(len(p)):
        sum += p[i]

        if(r < sum):
            ans = i
            break
    
    return ans


#前に喋ったn番目の人は喋らないようにするsoftmax関数
def softmax_skip(numbers, n):
    ans = []
    sum = 0

    for i in range(len(numbers)):
        #n番目（前に喋った人）は喋らない
        if(i == n):
            ans.append(0)
            continue
        
        temp = math.exp(numbers[i])
        ans.append(temp)
        sum += temp
    
    ans2 = []
    for x in ans:
        ans2.append(x/sum)
    
    return ans2


#log: 会話セッション, motivation: 発話しやすさ(0-1)
class character:
    def  __init__(self, name, persona, motivation):
        self.name = name    
        self.persona = persona
        self.log = [{"role": "system", "content": "あなたはラジオパーソナリティのひとりです．適宜話題を変えつつ会話を進展させてください．"}]
        self.motivation = motivation

    def add_log(self, x):
        self.log.append(x)


hanako = character("hanako", "引っ込み思案な女の子", 0.2)
tarou = character("tarou", "元気な男の子", 0.8)
jirou = character("jirou", "頭脳明晰な男の子", 0.5)
yoshiko = character("yoshiko", "体を動かすのが好きな女の子", 0.7)

c = []
c.append(hanako)
c.append(tarou)
c.append(jirou)
c.append(yoshiko)

m = []
for x in c:
    m.append(x.motivation)
print(m)
print(softmax_skip(m, 100))

next_talker = darts(softmax_skip(m, 100))
wadai = "あなたたちはラジオ出演者です。好きなゲームに関してトークしてください。"
add = {"role": "user", "content": wadai}

while True:
    for x in c:
        x.add_log(add)
    
    res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=c[next_talker].log)
    ans = res["choices"][0]["message"]
    print(c[next_talker].name + ": " + ans["content"])

    add = {"role": ans["role"], "content": ans["content"]}
    
    next_talker = darts(softmax_skip(m, next_talker))

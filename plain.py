#ただ話すだけ
import openai
from function import initialize, stream


openai.api_key = initialize.openAI_KEY()


log = stream.log("./output/log.txt", "plain.py")
log.add_line()
honoka = initialize.ref_file("./data/honoka/honoka.txt")


while True:
    user_input = input("あなた: ")
    if user_input == "quit":
        break  
    log.add(user_input)
    honoka.append({"role": "user", "content": user_input})

    res = openai.ChatCompletion.create(model = "gpt-4", messages = honoka)
    ans = res["choices"][0]["message"]["content"].strip()
    honoka.append({"role": "assistant", "content": ans})

    print("ほのか: " + ans)
    log.add(ans)
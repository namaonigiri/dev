import openai
from function import initialize, stream

openai.api_key = initialize.openAI_KEY()


log = stream.log("./output/log.txt", "withact.py")
log.add_line()
honoka = initialize.ref_file("./data/honoka/honoka.txt")


while True:
    user_action = input("type of action(if you simply want to talk, input '会話'): ")
    prompt = {"action": user_action}
    if user_action == "quit":
        break
    elif user_action == "会話":
        user_input = input("content: ")
        prompt["content"] = user_input
    
    log.add(str(prompt))
    honoka.append({"role": "user", "content": str(prompt)})

    res = openai.ChatCompletion.create(model = "gpt-4", messages = honoka)
    ans = res["choices"][0]["message"]["content"].strip()
    honoka.append({"role": "assistant", "content": ans})

    print("ほのか: " + ans)
    log.add(ans)
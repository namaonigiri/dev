#adventure game
import datetime as dt
import openai

#openai.api_key = input("APIのシークレットキー:")
openai.api_key = initialize.openAI_KEY()

def printline():
  print("---------------------------------------------")
def where_to_go(place):
  printline()
  print("システム: どこへ行きますか？")
  for x in place:
    print("―"+x)
  flag = 0
  while flag == 0:
    printline()
    ans = input(">>")
    printline()
    if(ans in place):
      flag = 1
    else:
      print("そんな場所には行けません！")
  return ans

y = 2023
m = 10
d = 13

place_basic = ["学校", "商店街", "公園", "喫茶店", "自宅"]

place_holiday = ["学校", "商店街", "公園", "喫茶店", "遊園地", "水族館", "デパート", "どこにも行かない"]

#なりきり用データの読み込み
f = open("./data/honoka.txt")
txt_chara = f.read()

date = dt.date(y, m, d)
print(str(y)+"/"+str(m)+"/"+str(d))
character = [{"role": "system", "content": txt_chara}]
#date.strftime("%a") == "Sat" or "Sun"
while True:
  if True:
    dest = where_to_go(place_holiday)
    character.append({"role": "user", "content": "ほのかと" + dest + "に来た"})

    while True:
      gamaster = [{"role": "system", "content": "You are a game master. You decide happening or not happening event in a game."}]
      gamaster += character
      gamaster.pop(1)
      gamaster.append({"role": "user", "content": "Need event? If you think yes, describe the event in the place, output only description of the event beginning in Japanese. If you think no, output 'いいえ'."})
      res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=gamaster)
      ans = res["choices"][0]["message"]["content"].strip()
      if(ans != "いいえ"):
        print(ans)
        character.append({"role": "assistant", "content": ans})
      printline()

      res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=character)
      ans = res["choices"][0]["message"]["content"].strip()
      character.append({"role": "assistant", "content": ans})
      print("ほのか: "+ans)

      prompt = input("あなた: ")
      character.append({"role": "user", "content": prompt})

      printline()

  else:
    where_to_go(place_basic)
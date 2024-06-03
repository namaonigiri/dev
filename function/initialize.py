import openai
#pathの.txtファイルを参照してチャットを生成する
def ref_file(path):
    f = open(path)
    txt_chara = f.read()
    return [{"role": "system", "content": txt_chara}]

def openAI_KEY():
    f = open("./openAI_KEY.txt")
    key = f.read()

    return key

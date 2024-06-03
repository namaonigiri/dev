import csv

#出力ログをとる
class log:
    #path: ログ置き場，str: 適当な文字列（だいたい実行ファイル名）
    def __init__(self, path, file_name):
        self.path = path
        with open(self.path, mode = "w") as f:
            f.write(file_name)

    #ログに追加する
    def add(self, sentence):
        with open(self.path, mode="a") as f:
            f.write("\n" + sentence)

    #ログに区切り線を追加する
    def add_line(self):
        with open(self.path, mode = "a") as f:
            f.write("\n---------------------------------------------")
    
    #ログに改行を追加する

#ファイル読み込み
def read_file(path):
    f = open(path)
    return f.read()

#
def read_csv(path):
    ans = []
    with open(path) as f:
        for x in csv.reader(f):
            temp = []
            for y in x:
                temp.append(float(y))
            ans.append(temp)
    
    return ans

#区切り線を出力する（見やすさのためにループ終了ごとに出力させることが多い
def printline():
  print("---------------------------------------------")
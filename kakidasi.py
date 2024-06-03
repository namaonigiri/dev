#各種設定（ここを書き換える）
file_name = "kusoge.txt"
character_name = ""
output_file = ".txt"


f = open("./manuscript/" + file_name)
original = f.read()
splitted = original.splitlines()

l = []
for x in splitted:
    if x.startswith(character_name + "「") == True:
        temp = x[3:-1]
        l.append(temp)

with open("./output/" + output_file, mode = 'a') as f:
    for x in l:
        f.write(x + '\n')
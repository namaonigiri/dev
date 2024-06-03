import csv
from function import stream

def read_csv(path):
    ans = []
    with open(path) as f:
        for x in csv.reader(f):
            temp = []
            for y in x:
                temp.append(y)
            ans.append(temp)
    
    return ans

dim = 8
origin = read_csv(f"./output/honoka/vec{dim}.csv")
path_output = f"./output/vector{dim}.csv"
origin_emo = []
for x in origin:
    origin_emo.append(x[0:-1])

list_emo = [0]
list_vec = [0]

for i in range(len(origin)):
    for j in range(len(list_emo)):
        if origin_emo[i] == list_emo[j]:
            list_vec[j].append(origin[i])
            break
        elif j == len(list_emo) - 1:
            list_emo.append(origin_emo[i])
            list_vec.append([origin[i]])
list_vec.pop(0)  
list_emo.pop(0)
ans = []
for i in range(len(list_vec)):
    sum = 0
    for y in list_vec[i]:
        sum += int(y[-1])
    if sum / len(list_vec[i]) >= 0.5:
        temp = list_emo[i]
        temp.append(1)
        ans.append(temp)
    else:
        temp = list_emo[i]
        temp.append(0)
        ans.append(temp)
for x in list_vec:
    print(x)
print(len(ans))
with open(path_output, "w") as f:
    writer = csv.writer(f)
    for x in ans:
        writer.writerow(x)
#画像評価と状態評価を統合する
import csv
from function import stream

def main():
    dim = 8
    pic_path = f"./output/honoka/pic2vec_{dim}.csv"
    #state_path = f"./output/honoka/state2vec_{dim}.csv"
    label_path = "./output/honoka/action.txt"
    output_path = "./output/pic8.csv"

    n = [1, 3, 4, 8, 11, 12, 13, 14, 17, 19, 20, 22, 25, 26, 27, 31, 33, 37, 39, 40]
    pic_raw = stream.read_csv(pic_path)
    #state = stream.read_csv(state_path)
    label = stream.read_file(label_path).split("\n")
    pic = []
    for i in range(len(pic_raw)):
        for x in n:
            if i == (int(x)-1):
                pic.append(pic_raw[i])
    flag = 0
    with open(output_path, "w") as f:
        writer = csv.writer(f)
        for x in pic:
            writer.writerow(x)


    vec = []
    for i in range(len(pic)):
        for j in range(len(state)):
            l = []
            for k in range(len(pic[0])):
                l.append((pic[i][k] + state[j][k]) / 200)
            #l.append(int(label[20*i+j]))
            vec.append([l])
            if flag == 0:
                with open(output_path, "w") as f:
                    writer = csv.writer(f)
                    writer.writerow(l)
                    flag = 1
            else:
                with open(output_path, "a") as f:
                    writer = csv.writer(f)
                    writer.writerow(l)

if __name__ == "__main__":
    main()
#画像評価と状態評価を統合する
import csv
from function import stream

def main():
    dim = 8
    pic_path = f"./output/task/pic2vec_scene3_1.csv"
    state_path = f"./output/task/walking2.csv"
    output_path = "./output/task/integrated3_true_hyper.csv"

    n = [1, 3, 4, 8, 11, 12, 13, 14, 17, 19, 20, 22, 25, 26, 27, 31, 33, 37, 39, 40]
    pic = stream.read_csv(pic_path)
    state = stream.read_csv(state_path)

    flag = 0

    vec = []
    pre = []
    for x in state[0]:
        pre.append(x / 100)
        print(x/100)
    
    for i in range(len(pic)):
        l = []
        print(pre)
        for k in range(len(pic[0])):
            l.append((pic[i][k] / 100 + pre[k]) / 2)
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
        pre = l
                    

if __name__ == "__main__":
    main()
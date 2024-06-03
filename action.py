import csv
from function import stream

def main():
    finished = 6
    n = 20
    pic = [1, 3, 4, 8, 11, 12, 13, 14, 17, 19, 20, 22, 25, 26, 27, 31, 33, 37, 39, 40]
    state_path = "./data/honoka/internal_state.txt"
    output_path = "./output/action.txt"

    state = stream.read_file(state_path)
    for i in range(finished, n):
        l = []
        for x in state.split("\n"):
            print(f"pic{pic[i]}")
            print(x)
            while True:
                choice = input(">>")
                if choice == "1" or choice == "0":
                    break
            stream.printline()

            l.append(choice)
        
        for x in l:
            if i == 0:
                with open(output_path, "w") as f:
                    f.write(f"{x}\n")
            else:
                with open(output_path, "a") as f:
                    f.write(f"{x}\n")

if __name__ == "__main__":
    main()
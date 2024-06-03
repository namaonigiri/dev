import sys
def calc(a, b):
    #数字を分割
    a_divide = list(a)
    b_divide = list(b)
    a_divide.reverse()
    b_divide.reverse()

    #桁別に計算を保持する行列
    mat = []

    for i, x in enumerate(a_divide):
        temp = []
        for j, y in enumerate(b_divide):
            degit = i + j + 1
            if 9 < degit:
                temp.append(0)
            else:
                e = 1
                for k in range(degit - 1):
                    e *= 10
                temp.append(e)
        mat.append(temp)

    ans = 0
    for x in mat:
        print(x)


calc("125135", "1515153")
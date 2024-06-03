from function import stream
a = stream.read_csv("./output/honoka/formlp/vector8.csv")
c = 0
for x in a:
    if x[8] == 1:
        c += 1
print(c)
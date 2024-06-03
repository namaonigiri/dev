#文字列が条件に合うかを調べる
def check_string(s):
    ls = list(s)
    #記号の出現管理
    flag = False
    #アルファベットの出現管理
    chars = []

    for x in ls:  
        if x == "@" or x == "$" or x == "%":
            if flag == False:
                flag = True
        
        elif not (x in chars):
            chars.append(x)
    
    if 5 <= len(chars) and flag:
        return True
    
    else:
        return False

# 文字列を二分割
def divide_list(l):
    half = len(l) // 2
    return [l[: half], l[half: ]]

def return_min(s):
    for i in range(6, length + 2):
            for j in range(length - i + 2):
                part = s[j: j + i - 1]
                if check_string(part):
                    return len(part)

lines = ["kwljmkr@%@hhdv%tl%xhcphddyg$mqqgcbnnenkaxb@@s$@lnazrt%@@seg@ejaw%%%tqlbobvplwttk%%$gwq%tajemr@v@o%bamw%o%twonzbveoaeld@$tps$vpxmtj$lswirys%vbjyccpahtiqgjgym@$vlt%f$kdztl%d%xmwsal$fajtmdrad@tpkeuwgjyvkl$jmg$vlgz@@azmvpn@f@x%e$%o$klj$py@mo%tmnpfrmsoyfpepn%y%ppznnmzjjy%mgzmrexptsjsy%vlozvj@vu@svlvvhoyk"]
flag = False
while True:
        for x in lines:
            flag = flag or check_string(x)
        print("uhehe")
        print(lines)
        if not flag:
            break
        
        else:
            prev = lines
            lines = []
            for x in prev:
                for y in divide_list(x):
                    lines.append(y)
        
print(prev)
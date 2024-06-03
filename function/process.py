import re
import json
#出力された文字列をjsonにする
def tojson(string):
    temp = re.findall(r'\{.*\}', string.replace("\n", ""))
    ans = json.loads(temp[-1])
    return ans
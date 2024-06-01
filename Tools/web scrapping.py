import json
Lst = list()
with open(r'C:\\Users\\Lenovo\\Desktop\\New Text Document.txt', encoding="utf-8") as f:
    Dict = dict()
    while True:
        line = f.readline()
        print(line)
        if line == "%":
            break
        elif line == "#\n":
            Lst.append(Dict)
            Dict = dict()
        else: 
            splited_line = line.split("^")
            Dict[splited_line[0]] = splited_line[1].split("\n")[0]

with open("C:\\Users\\Lenovo\\Desktop\\New.txt", "w") as g:
    json.dump(Lst, g)
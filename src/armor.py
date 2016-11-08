def armor(type_, name, string):
    s  = "---- BEGIN " + type_ + " ----\n"
    if name != "":
        s += "Name: " + name + "\n\n"
    else:
        s += "\n"
    s += string + "\n\n"
    s += "---- END " + type_ + " ----"
    return s

def unarmor(type_, armor):
    armor = armor.split("\n")
    i = False
    s = []
    name = ""
    for j in armor:
        if j == "---- BEGIN " + type_ + " ----":
            i = True
        elif j == "---- END " + type_ + " ----":
            i = False
        elif j.startswith("Name: "):
            name = j[6:]
        elif j == "":
            continue
        elif i:
            s.append(j)
        else:
            continue
    return ('\n'.join(s), name)

def insert_newlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

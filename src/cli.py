import rsa, keyring, base64
from armor import armor, unarmor, insert_newlines
from getpass import getpass

pubkr = keyring.Keyring("public", "public.kr")
prikr = keyring.Keyring("private", "private.kr")


def makekey_assistant():
    if input("Willst du wirklich einen neuen Schlüssel erstellen? Um einen bereits vorhandenenen zu Importieren nutze den importkey-Befehl. (y/N)") == "y":
        print("Generiere Schlüssel (dauert einen Moment)")
        print("Schlüssel-Länge: 1024-Bits")
        your_new_key = rsa.makeYourKey(1024)
        print("Schlüssel erzeugt.")
        name = input("Wir speichern die Schlüssel in einem sogenannten Keyring. Bitte geben sie ihren Namen ein: ")
        pubkr.add(name, your_new_key)
        passw = getpass("Für ihren privaten Schlüssel benötigen wir ein Passwort: ")
        prikr.add(name, your_new_key, passw)
        print("Schlüsselpaar erzeugt und unter dem Namen '" + name + "' abgespeichert.")
        
def encrypt_assistant():
    fname = input("Bitte gebe den Pfad der zu verschlüsselnden Datei an: ")
    f = open(fname, "rb")
    content = f.read()
    f.close()
    print("Datei eingelesen.")
    names = pubkr.gets()
    print("Namen: " + ' '.join(names))
    name = input("Bitte wähle einen aus: ")
    while not name in names:
        if name == "": return
        print("Dieser Name existiert nicht.")
        print("Namen: " + ' '.join(names))
        name = input("Bitte wähle einen anderen aus: ")
    print("Verschlüssele (dauert einen Moment)")
    crypt = rsa.encrypt(content, pubkr.get(name))
    crypt = str(base64.b64encode(bytes(crypt, "utf-8")), "utf-8")
    crypt = insert_newlines(crypt, 60)
    crypt = armor("RSPLUS OUTPUT", name, crypt)
    f = open(fname + ".crypt", "w")
    f.write(crypt)
    f.close()
    
    print("Die verschlüsselte Version der Datei können sie unter " + fname +  ".crypt finden. Sie können diese Datei an den Empfänger versenden.")
    
def decrypt_assistant():
    cname = input("Bitte gebe den Pfad zur .crypt-Datei an: ")
    if cname.split(".")[-1] != "crypt":
        print("Keine Crypt-Datei angegeben.")
        return
    c = open(cname, "r")
    crypt = c.read()
    c.close()
    fname = '.'.join(cname.split(".")[:-1])

    print("Die Datei wird entschlüsselt.")
    crypt, name = unarmor("RSPLUS OUTPUT", crypt)
    crypt = ''.join(crypt.split("\n"))
    crypt = str(base64.b64decode(bytes(crypt, "utf-8")), "utf-8")

    passw = getpass("Für ihren privaten Schlüssel benötigen wir ein Passwort: ")

    names = prikr.gets(passw)
    if not name in names:
        print("You do not have the private key to encrypt.")
        return
    print("Entschlüssele (dauert einen Moment)")

    msg = str(bytes(rsa.decrypt(crypt, prikr.get(name, passw)).strip("b'"), "utf-8"), "utf-8")
    msg = eval("'''" + msg + "'''")
    f = open(fname, "w")
    f.write(msg)
    f.close()
    
    
def importkey_assistant():
    fname = input("Dateiname der .key-Datei: ")
    f = open(fname, "r")
    a = f.read()
    f.close()

    a, name = unarmor("RSPLUS KEY TRANSFER", a)
    a = str(base64.b64decode(bytes(a, "utf-8")), "utf-8")
    pub = N = 0
    for i in a.split("\n"):
        if i.startswith("Public-Key: "):
            pub = int(i[12:])
        elif i.startswith("Key-N: "):
            N = int(i[7:])
    kp = {'pub': pub, 'N': N, 'pri': 0}
    pubkr.add(name, kp)

    print("Der Schlüssel wurde erforlgreich importiert.")
    
def exportkey_assistant():
    passw = getpass("Für ihren privaten Schlüssel benötigen wir ein Passwort: ")
    names = prikr.gets(passw)
    print("Namen: " + ' '.join(names))
    name = input("Bitte wähle einen aus: ")
    while not name in names:
        if name == "": return
        print("Dieser Name existiert nicht.")
        print("Namen: " + ' '.join(names))
        name = input("Bitte wähle einen anderen aus: ")

    kp = prikr.get(name, passw)

    fname = name + ".key"

    print("Speichere Daten ...")
    msg  = "Public-Key: " + str(kp['pub']) + "\n"
    msg += "Key-N: " + str(kp['N'])
    msg = str(base64.b64encode(bytes(msg, "utf-8")), "utf-8")
    msg = insert_newlines(msg, 60)

    key = armor("RSPLUS KEY TRANSFER", name, msg)
    f = open(fname, "w")
    f.write(key)
    f.close()
    print("Fertig!")

print("RS+ CLI")
print("You may use: exit, importkey, exportkey, makekey, encrypt, decrypt")
inp = input("RS+ ::> ")
while inp != "exit":
    if inp == "":
        inp = input("RS+ ::> ")
        continue
    elif inp == "makekey":
        makekey_assistant()
    elif inp == "encrypt":
        encrypt_assistant()
    elif inp == "decrypt":
        decrypt_assistant()
    elif inp == "exportkey":
        exportkey_assistant()
    elif inp == "importkey":
        importkey_assistant()
    else:
        print("Command not found.")
        print("You may use: exit, importkey, exportkey, makekey, encrypt, decrypt")
    print()
    inp = input("RS+ ::> ")

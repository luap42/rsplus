import json, prikrenc, os
class Keyring:
    def __init__(self, mode="public", file=None):
        self.file = file
        self.mode = mode
        self.exist = False
        if os.path.isfile(self.file):
            self.exist = True
        
    def updateKeyring(self, passw):
        try:
            f = open(self.file, "r")
            kr = f.read()
            if self.mode != "private":
                print("Accessing public keyring...")
                self.keyring = json.loads(kr)
            else:
                try:
                    self.keyring = json.loads(prikrenc.decrypt_kr(kr, passw))
                except:
                    self.keyring = {}
            f.close()
            del f
        except:
            self.keyring = {}

    def add(self, name, kp, passw=""):
        self.updateKeyring(passw)
        if self.keyring == {} and self.exist:
            return
        if self.mode == "private":
            kp = {'pub': kp['pub'], 'pri': kp['pri'], 'N': kp['N']}
        else:
            kp = {'pub': kp['pub'], 'pri': 0, 'N': kp['N']}
        self.keyring[name] = kp
        if self.file != None:
            try:
                f = open(self.file, "w")
                if self.mode != "private":
                    f.write(json.dumps(self.keyring))
                else:
                    f.write(prikrenc.encrypt_kr(json.dumps(self.keyring), passw))
                f.close()
            except: pass

    def gets(self, passw=""):
        self.updateKeyring(passw)
        return self.keyring.keys()

    def get(self, name, passw=""):
        self.updateKeyring(passw)
        return self.keyring[name]

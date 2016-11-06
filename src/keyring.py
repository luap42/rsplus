import json
class Keyring:
    def __init__(self, mode="public", file=None):
        self.file = file
        self.mode = mode
        try:
            f = open(file, "r")
            self.keyring = json.loads(f.read())
            f.close()
            del f
        except:
            self.keyring = {}

    def add(self, name, kp):
        if self.mode == "private":
            kp = {'pub': kp['pub'], 'pri': kp['pri'], 'N': kp['N']}
        else:
            kp = {'pub': kp['pub'], 'pri': 0, 'N': kp['N']}
        self.keyring[name] = kp
        if self.file != None:
            try:
                f = open(self.file, "w")
                f.write(json.dumps(self.keyring))
                f.close()
            except: pass

    def gets(self):
        return self.keyring.keys()

    def get(self, name):
        return self.keyring[name]

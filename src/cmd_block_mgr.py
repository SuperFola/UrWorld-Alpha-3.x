import arkpov as ark


class CmdBlockManager:
    def __init__(self):
        self.blocks = []
        #self.blocks[0] -> [(x, y), code_str]

    def add(self, x, y, code=None):
        self.blocks.append([(x, y), code])

    def pop(self, x, y):
        for i in range(len(self.blocks)):
            pos = self.blocks[i][0]
            if pos == (x, y):
                self.blocks.pop(i)
                break

    def modify(self, x, y, code=None):
        self.get_block(x, y, code)

    def get_block(self, x, y, modifiy=False, modif=''):
        for i in range(len(self.blocks)):
            pos = self.blocks[i][0]
            if pos == (x, y):
                if not modifiy:
                    return self.blocks[i]
                else:
                    self.blocks[i] = modif

    def get_code(self, x, y):
        block = self.get_block(x, y)
        return block[1]

    def exec(self, x, y):
        code = self.get_code(x, y)
        if code is not None:
            evalue = ark.eval_for_cmd_block(code)
            if evalue is not None:
                return evalue
            return ""
        return "Erreur, le code fournit n'est pas exécutable"

    def rc(self, x, y):
        return self.exec(x, y)
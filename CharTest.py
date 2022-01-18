import re
class Char:
    def __init__(self, char, ind):
        if len(char) == 3:
            char = char[1]
            self.cor = 2
        elif re.match('[A-Z]', char[0]):
            self.cor = 1
        else:
            self.cor = 0
        self.val = char[0].lower()
        self.ind = ind

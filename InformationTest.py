from collections import defaultdict

class Information:
    def __init__(self, wordlength, validwordlist):
        self.correct = [''] * wordlength
        self.semis = set()
        self.picks = [set() for i in range(wordlength)]
        self.bad = set()
        self.words = validwordlist.copy()
        self.mins = defaultdict(int)
        self.maxs = {}
        self.countwordlist = defaultdict(int)
        self.guess = 0
        self.prevGuesses = []
        self.unused = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}

    def updateWords(self, Chararray):
        newWords = []
        for word in self.words:
            valid = True
            counts = defaultdict(int)
            for i in range(len(word)):
                counts[word[i]] += 1
                if (self.correct[i] != '' and word[i] != self.correct[i]) or (
                        word[i] in self.picks[i] and word[i] != self.correct[i]) or (word[i] in self.bad):
                    valid = False
                    break
            if not valid: continue
            for char in self.semis:
                if char not in word:
                    valid = False
                    break
            for key in counts.keys():
                if key in self.mins.keys() and counts[key] < self.mins[key]:
                    valid = False
                    break
                if key in self.maxs.keys() and counts[key] > self.maxs[key]:
                    valid = False
                    break

            if valid:
                newWords.append(word)
                for char in word:
                    self.countwordlist[char] += 1
        self.words = newWords
        self.unused = self.unused - self.bad - self.semis - {item for item in self.correct}

    def updateInfo(self, Chararray):
        self.guess += 1
        Pguess = ''
        for Charobj in Chararray:
            Pguess += Charobj.val
        self.prevGuesses.append(Pguess)
        self.countwordlist = defaultdict(int)
        correct = defaultdict(int)
        incorrect = defaultdict(int)
        for Charobj in Chararray:
            if Charobj.cor == 1:
                correct[Charobj.val] += 1
                self.semis.add(Charobj.val)
                self.picks[Charobj.ind].add(Charobj.val)
            elif Charobj.cor == 2:
                correct[Charobj.val] += 1
                self.correct[Charobj.ind] = Charobj.val
                self.picks[Charobj.ind].update(self.semis)
            elif Charobj.cor == 0:
                incorrect[Charobj.val] += 1
                self.bad.add(Charobj.val)
        self.bad = self.bad - correct.keys()
        for key in correct.keys():
            self.mins[key] = max(correct[key], self.mins[key])
        for key in incorrect.keys():
            if key in correct.keys():
                self.maxs[key] = correct[key]
        self.updateWords(Chararray)

    def sortdict(self):
        return sorted(self.countwordlist.items(), key=lambda item: -item[1])

    def copy(self):
        infocopy = Information(len(self.correct), self.words)
        infocopy.correct = self.correct
        infocopy.semis = self.semis
        infocopy.picks = self.picks
        infocopy.bad = self.bad
        infocopy.words = self.words
        infocopy.mins = self.mins
        infocopy.maxs = self.maxs
        infocopy.countwordlist = self.countwordlist
        return infocopy
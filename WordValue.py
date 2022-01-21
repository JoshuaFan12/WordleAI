class WordValue:
    def __init__(self, word, wordValueDict):
        self.word = word
        self.wordValueDict = wordValueDict
        self.letters = set([char for char in word])
        self.value = self.getValueOfWord()

    def getValueOfWord(self):
        value = 0
        for char in self.letters:
            value += self.wordValueDict[char]
        return value
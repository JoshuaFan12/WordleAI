from WordValue import WordValue

class UniqueLetterStart:
    def __init__(self, wordValueObjects=[], value=[]):
        self.words = wordValueObjects
        self.value = value
        self.letters = set()
        for wordValueObj in wordValueObjects:
            self.letters.update(wordValueObj.letters)

    def addWord(self, wordValueObject):
        self.words.append(wordValueObject.word)
        self.value.append(wordValueObject.value)
        self.letters.update(wordValueObject.letters)


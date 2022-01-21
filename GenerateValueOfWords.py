from UniqueLetterStarts import UniqueLetterStarts

class ValueWords:
    def __init__(self, letterDictValues, words, fileToRead='4UniqueWords.csv', multiplier=0.75):
        self.wordLists = []
        self.letterValues = letterDictValues
        self.words = words
        self.multiplier = multiplier
        self.wordValues = {}
        self.populateWordValues()

        with open(fileToRead, 'r') as infile:
            for line in infile:
                self.wordLists.append(line.replace("\n", "").split('\t'))

        # print(self.wordValues)
        # print(len(self.wordLists))

        self.wordValue = list()
        self.populateWordListValue()
        self.wordValue = sorted(self.wordValue, key=lambda wordTuple: wordTuple[0], reverse=True)
        print(len(self.wordValue))
        self.printBestWords()

    def populateWordValues(self):
        for word in self.words:
            curWordVal = 0
            for i in range(len(word)):
                curWordVal += self.letterValues[word[i]]
            self.wordValues[word] = curWordVal

    def populateWordListValue(self):
        for wordList in self.wordLists:
            curWordListValue = 0
            wordList = sorted(wordList, key=lambda word: self.wordValues[word], reverse=True)
            # print(wordList)
            for i in range(len(wordList)):
                curWordListValue += self.wordValues[wordList[i]] * (self.multiplier ** i)
            self.wordValue.append((round(curWordListValue), wordList))

    def printBestWords(self, count=100):
        for i in range(min(count, len(self.wordValue))):
            print(f"Value: {self.wordValue[i][0]}, words: {self.wordValue[i][1]}")

    def printWordValue(self, word):
        print(f"{word}: {self.wordValues[word]}")


starts = UniqueLetterStarts()
# starts.printOptionsToFile()
letterValueDict = starts.letterValueDict
words = starts.possibleWords
valueWords = ValueWords(letterValueDict, words, fileToRead="4UniqueWords2.txt")
valueWords.printBestWords()
valueWords.printWordValue("rates")
valueWords.printWordValue("plonk")
valueWords.printWordValue("chimb")
valueWords.printWordValue("fudgy")


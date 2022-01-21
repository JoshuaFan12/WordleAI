from collections import defaultdict
from WordValue import WordValue
from UniqueLetterStart import UniqueLetterStart

class UniqueLetterStarts:
    def __init__(self, wordLength = 5, numWords = 4, wordFileName = "Scrable.txt", multiplier=.75):
        if wordLength * numWords > 26:
            print("Impossible with provided parameters :(")
            return

        self.wordLength = wordLength
        self.numWords = numWords
        self.wordFileName = wordFileName

        self.allXLetterWords = set()
        self.uniqueLetterWords = set()
        self.populateWords()

        self.letterValueDict = {}
        for i in range(26):
            self.letterValueDict[chr(ord('a') + i)] = 0
        self.populateValueDictionary()
        numLettersToDisposeOf = 26 - (wordLength * numWords)
        self.worstLetters = set([item[0] for item in sorted(self.letterValueDict.items(), key=lambda item: -item[1])[-numLettersToDisposeOf:]])
        self.possibleWords = set()
        self.removeWordsWithBadLetters()
        self.wordValueObjects = set()
        self.populateWordValueObjects()

        self.possibilities = set()
        startPoss = UniqueLetterStart()
        self.possibilities.add(startPoss)
        # self.tryPossibleWords(1)

    def populateWords(self):
        with open(self.wordFileName, 'r') as wordFile:
            lines = wordFile.readlines()
            for line in lines:
                curWord = line[:-1].lower()
                if len(curWord) == self.wordLength:
                    self.allXLetterWords.add(curWord)
                    if self.allUniqueLetters(curWord):
                        self.uniqueLetterWords.add(curWord)

    def allUniqueLetters(self, word):
        for i in range(len(word) - 1):
            if word[i] in word[i+1:]:
                return False
        return True

    def populateValueDictionary(self):
        for word in self.allXLetterWords:
            for char in word:
                self.letterValueDict[char] += 1

    def populateWordValueObjects(self):
        print(len(self.possibleWords))
        for word in self.possibleWords:
            curWordValueObj = WordValue(word, self.letterValueDict)
            self.wordValueObjects.add(curWordValueObj)

    def removeWordsWithBadLetters(self):
        print("Unique words: ", len(self.uniqueLetterWords))
        newWords = set()
        for word in self.uniqueLetterWords:
            badWord = False
            for char in self.worstLetters:
                if char in word:
                    badWord = True
            if not badWord:
                newWords.add(word)

        self.possibleWords = newWords

    def tryPossibleWords(self, depth):
        # self.printPossibilities()
        if depth > self.numWords:
            return
        newPossibilities = set()
        print("Test")
        print(len(self.wordValueObjects))
        for possibility in self.possibilities:
            for wordValueObj in self.wordValueObjects:
                validWord = True
                for char in wordValueObj.word:
                    if char in possibility.letters:
                        validWord = False
                        break
                if validWord:
                    print(wordValueObj.word)
                    newPossibilities.add(UniqueLetterStart(possibility.words.copy(), possibility.value.copy()).addWord(wordValueObj))
        self.possibilities = newPossibilities
        self.tryPossibleWords(depth + 1)


    def printPossibilities(self):
        for poss in self.possibilities:
            if poss == None or poss.words == None:
                continue
            words = [wordValueObj.word for wordValueObj in poss.words]
            print(f"Possibility: {words}")

    def printOptions(self):
        for word1 in self.possibleWords:
            for word2 in self.possibleWords:
                if not self.allUniqueLetters(word1+word2):
                    continue
                for word3 in self.possibleWords:
                    if not self.allUniqueLetters(word1 + word2 + word3):
                        continue
                    for word4 in self.possibleWords:
                        if not self.allUniqueLetters(word1 + word2 + word3 + word4):
                            continue
                        else:
                            print(f"Words: {word1} {word2} {word3} {word4}")


    def printOptionsToFile(self):
        with open("4UniqueWords3.csv", 'w') as outfile:
            possWordsList = sorted(list(self.possibleWords))
            for i in range(len(possWordsList)):
                word1 = possWordsList[i]
                if word1 > 'burgs':
                    continue
                for j in range(i+1, len(possWordsList)):
                    word2 = possWordsList[j]
                    if not self.allUniqueLetters(word1+word2):
                        continue
                    for k in range(j+1, len(possWordsList)):
                        word3 = possWordsList[k]
                        if not self.allUniqueLetters(word1+word2+word3):
                            continue
                        for l in range(k+1, len(possWordsList)):
                            word4 = possWordsList[l]
                            if not self.allUniqueLetters(word1+word2+word3+word4):
                                continue
                            else:
                                print(f"Words: {word1} {word2} {word3} {word4}")
                                str = f"{word1},{word2},{word3},{word4}\n"
                                outfile.write(str)
                                outfile.flush()

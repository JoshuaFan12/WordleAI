from InformationTest import Information
from CharTest import Char
from collections import defaultdict
import re
import csv

class WordleAI:
    def __init__(self, wordlist, frequency, wordlength=5):
        self.xWordlist = wordlist[wordlength].copy()
        self.wordLength = wordlength
        self.alphabetWords = set()
        self.frequency = frequency
        self.__generateAlphabet(self.wordLength)
        self.info = Information(wordlength, self.frequency)
    def copy(self):
        AICopy = WordleAI([self.xWordlist]*(self.wordLength+1), self.frequency, self.wordLength)
        AICopy.xWordlist = self.xWordlist.copy()
        AICopy.wordLength = self.wordLength
        AICopy.alphabetWords = self.alphabetWords.copy()
        AICopy.frequency = self.frequency.copy()
        AICopy.info = self.info.copy()
    def reset(self, frequency):
        self.frequency = frequency
        self.info = Information(self.wordLength, self.frequency)
    def solve(self,wordinput, wordFreq = []):
        if wordinput is None:
            return None
        wordinput = wordinput.split(' ')
        Chararray = [Char(wordinput[i], i) for i in range(self.wordLength)]
        self.info.updateInfo(Chararray)
        wordFreq = [word for word in self.info.words if word in self.frequency]

        if '' not in self.info.correct:
            return 'WIN'
        # print(sorted(wordFreq, key=lambda item: self.frequency.index(item))[0:min(len(self.info.words), 5)], len(self.info.words))
        suggestion = self.suggest()
        # print(suggestion[:min(5,len(suggestion))])
        # print(self.info.words)
        if len(wordFreq) > 19 and suggestion[0][0] != '?':
            return suggestion[0][0]
        elif len(wordFreq) > 2:
            mmbool = self.minMax()
            if mmbool != '?':
                return mmbool
            else:
                print('?')
                return suggestion[0][0]
        else:
            return sorted(wordFreq, key=lambda item: self.frequency.index(item))[0]
    def __generateAlphabet(self, wordlength):
        alphabetWords = {}
        for i in range(26):
            currchar = chr(ord('a') + i)
            alphabetWords[currchar] = set()
        for word in self.xWordlist:
            for char in word[0:-1]:
                alphabetWords[char].add(word)
        self.alphabetWords = alphabetWords
    def suggest(self):
        sortedDict = self.info.sortdict().copy()
        bestValue = [('?',0)]*20
        for i in range(len(sortedDict)):
            if sortedDict[i][0] in self.info.bad or  sortedDict[i][0] in self.info.correct:
                sortedDict[i] = (sortedDict[i][0], 0)
            if sortedDict[i][0] in self.info.semis:
                sortedDict[i] = (sortedDict[i][0], sortedDict[i][1]/2)
        unresDict = defaultdict(int)
        for item in sortedDict:
            unresDict[item[0]] = item[1]
        for word in self.xWordlist:
            if word in self.info.prevGuesses: continue
            value = 0
            for j in range(len(word)):
                value = value + unresDict[word[j]]
                if (len(word) > j+1) and word[j] in word[j+1:]:
                    if word[j] in self.info.correct and word[j] not in self.info.maxs.keys():
                        value += 0.1 * (self.info.countwordlist[word[j]]-len(self.info.words))
                    else: value = value - unresDict[word[j]]
                if word[j] in self.info.semis and word[j] not in self.info.picks[j]:
                    value += 0.1*(self.info.countwordlist[word[j]]-len(self.info.words))

            for i in range(len(bestValue)):
                if value > bestValue[i][1]:
                    for j in range(len(bestValue)-1, i, -1):
                        bestValue[j] = bestValue[j-1]
                    bestValue[i] = (word, value)
                    break
        return bestValue
    def guessToTxt(self, word, guess):
        temp = defaultdict(int)
        for char in word:
            temp[char] -= 1
        for char in guess:
            if char in temp.keys():
                temp[char] += 1

        ans = []
        for i in range(len(word)):
            if guess[i] in word:
                if word[i] == guess[i]:
                    ans += [f'[{guess[i]}] ']
                else:
                    ans += [(guess[i].upper() + ' ')]
            else:
                ans += [(guess[i] + ' ')]

        for key in temp.keys():
            for i in range(0, temp[key]):
                ans[ans.index(key.upper() + ' ')] = key + ' '
        ans2 = ''
        for item in ans:
            ans2 += item
        return ans2
    def minMax(self):
        validWords = self.info.words.copy()
        unique = set()
        incorrectInd = []

        for i in range(len(self.info.correct)):
            if self.info.correct[i] == '':
                incorrectInd += [i]
        truncatedWords = [[word[ind] for ind in incorrectInd] for word in validWords]

        for i in range(len(truncatedWords)):
            for char in truncatedWords[i]:
                for chararray in truncatedWords[i+1:]:
                    if char not in chararray and char not in self.info.correct:
                        unique.add(char)
                        break
        unique = list(unique)
        minMaxWords = set()
        for i in range(len(unique)):
            for j in range(i+1, len(unique)):
                minMaxWords.update(self.alphabetWords[unique[i]].intersection(self.alphabetWords[unique[j]]))
        pruning = len(self.xWordlist)
        bestGuess = '?'
        for guess in minMaxWords:
            currMax = 0
            myID = defaultdict(int)
            for word in validWords:
                myID[self.guessToTxt(word,guess)] += 1
                currMax = max(currMax, myID[self.guessToTxt(word,guess)])
                if currMax > pruning:
                    break
            if currMax == 1:
                return guess
            if currMax < pruning:
                pruning = currMax
                bestGuess = guess
        return bestGuess




                       # numRemaining = 0
                        # for j in range(len(word)):
                        #     # numRemaining += unsortDict[word[j]]
                        #     if word[j] in self.info.picks[j]:
                        #         numRemaining -= 1*unsortDict[word[j]]
                        #     if word[j] in self.info.correct or word[j] in self.info.semis or (j < len(word) - 1 and word[j] in word[j+1:]):
                        #         continue
                        #     else:
                        #         numRemaining += 10*unsortDict[word[j]]
                        # numRemaining = max(1, numRemaining)
                        # bestValue.append((word, numRemaining))
                        # return sorted(bestValue, key=lambda item: -item[1])[0:min(5, len(bestValue))]
        return 'There are no possible answers'

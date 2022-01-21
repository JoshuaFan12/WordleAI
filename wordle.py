from collections import defaultdict
from WordleAITest import WordleAI
import csv

hist = [0]*20
alphabetWordlist = {}
wordlist = defaultdict(set)
with open('Scrable.txt', 'r') as file:
    for line in file:
        wordlist[len(line) - 1].add(line[0:-1].lower())

frequency = 0
wordlength = 5
with open(f'{wordlength}LetterFreq.txt', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for line in spamreader:
        frequency = line
        break

def helper(game, word, guess = 'raise', j = 0, result = []):
    # print(guess)
    j+=1
    temp = defaultdict(int)
    for char in word:
        temp[char] -= 1
    for char in guess:
        if char in temp.keys():
            temp[char] += 1

    ans = []
    # print(guess)
    # print(word)
    for i in range(len(word)):
        if guess[i] in word:
            if word[i] == guess[i]:
                ans += [f'[{guess[i]}] ']
            else: ans += [(guess[i].upper() + ' ')]
        else: ans += [(guess[i] + ' ')]

    for key in temp.keys():
        for i in range(0, temp[key]):
            ans[ans.index(key.upper() + ' ')] = key + ' '
    ans2 = ''
    for item in ans:
        ans2 += item
    result += [(ans2 + ' ' + str(len(game.info.words)))]
    nextGuess = game.solve(ans2[:-1])
    # print(nextGuess)
    if nextGuess != 'WIN':
        if j > 25:
            print(j)
            print(word)
            for item in result:
                print(item)
            return None

        helper(game, word, nextGuess, j, result)

    else:
        if j > 0:
            print(j)
            print(word)
            for item in result:
                print(item)
        hist[j] += 1
game = WordleAI(wordlist.copy(), frequency.copy(), wordlength)
for word in frequency:
    helper(game, word, 'rates', 0, [])
    game.reset(frequency.copy())
    if word == 'murky':
        break
# game = WordleAI(wordlist.copy(), frequency.copy(), wordlength)
# helper(game, 'wives', 'facet')


print(hist)

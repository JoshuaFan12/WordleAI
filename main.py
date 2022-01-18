from collections import defaultdict

from WordleAI import WordleAI



# Guesslist = defaultdict(set)
alphabetWordlist = {}
wordlist = defaultdict(set)

# with open('oneThousandMostCommon.txt','r') as file:
#     for line in file:
#         Guesslist[len(line)-1].add(line[0:-1])
with open('Scrable.txt', 'r') as file:
    for line in file:
        wordlist[len(line) - 1].add(line[0:-1].lower())

confirm = True
while confirm:
    game = WordleAI(wordlist, int(input('How many letters? ')))
    game.solve()
    if not bool(input('continue? ')):
        confirm = False

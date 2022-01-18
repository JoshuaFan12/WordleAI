new = ''
import csv
with open('frequency.txt','r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for line in spamreader:
        new = line

for i in range(4,12):
    with open(f'{i}LetterFreq.txt', 'x') as file:
        for word in new:
            print(word)
            if len(word) == i:
                file.write(word + ',')
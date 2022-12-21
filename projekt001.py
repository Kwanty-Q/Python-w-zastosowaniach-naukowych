from turtle import color
import tqdm
import time
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor


import argparse
from ast import arg

parser = argparse.ArgumentParser()
parser.add_argument('file_name')
parser.add_argument('-a', '--liczba_wyrazow', default = 10)
parser.add_argument('-f', '--min', default = 0)
#parser.add_argument('-o', '--ignore', nargs = '*')

args = parser.parse_args()
#print(f'fsd {args.file_name} dsfsdf dsada {3 + 8}')
#print(f'{args.file_name = }')
#print(f'{args.liczba_wyrazow = }')
#print(f'{args.min = }')
#print(f'{args.ignore = }')


dictionary = {}
#print(type(dictionary))

min_dl = int(args.min)

with open(args.file_name, 'r', encoding="utf8") as f:
#with open('Lab1/test.txt', 'r', encoding="utf8") as f:
    for line in f:
        new_line = line.strip().split(' ') # co zrobić, żeby rozdzielało też I'll ?
        
        for word in new_line:
            word = word.replace('.', '')
            word = word.replace(',', '')
            word = word.replace('[', '')
            word = word.replace(']', '')
            word = word.replace(':', '')
            word = word.replace(';', '')
            word = word.replace('?', '')
            word = word.replace('!', '')
        #    co z apostrofem?
            if len(word) >= min_dl:
                if word in dictionary:
                    dictionary[word] = dictionary[word] + 1
                else:
                    dictionary[word] = 1

      #      print(word)       
            '''if word in dictionary:
                dictionary[word] = dictionary[word] + 1
            else:
                dictionary[word] = 1'''

# dwa sposoby na usunięcie słowa
#del dictionary['a']
#dictionary.pop('in')
#dictionary.pop('')
#dictionary.pop('/')


data = []
#print(type(data))


for a, b in dictionary.items():
    data.append((a, b))



graph = Pyasciigraph()

ile_wyswietlic = int(args.liczba_wyrazow) # args.liczba_wyrazow #10
'''print(args.liczba_wyrazow)
print(ile_wyswietlic)
print(type(args.liczba_wyrazow))
print(type(ile_wyswietlic))'''

data.sort(reverse=True, key=lambda tup: tup[1] ) # sortowanie od największego
hist = []
for w1 in range(ile_wyswietlic): #obcinanie histogramu
    hist.append(data[w1])


#pattern = [Gre, Red, Yel, Blu]
pattern = [Red, Yel, Blu,  ICya]
data_hist = vcolor(hist, pattern)

for line in graph.graph('Histogram liczby słów', data_hist):
#for line in graph.graph('Histogram liczby słów', data):
    print(line)
    
#koniec

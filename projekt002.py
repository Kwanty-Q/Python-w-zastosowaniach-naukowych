import numpy as np
import random
from PIL import Image, ImageDraw
import math

import argparse
from ast import arg

import tqdm
import time



class Symulacja:

    def __init__(self, n, m, gestosc_spinow):
        self.siatka = [] # czy to jest dobrze?
        for i in range(n):
            wiersz = []
            for j in range(m):
                spin = random.random() #np.random.rand(1)
                if spin < gestosc_spinow :
                    spin = 1
                else:
                    spin = -1
                wiersz.append(spin)
            self.siatka.append(wiersz)
        self.siatka = np.array(self.siatka)
        #print(self.siatka)

    def liczenie_energii(self, n, m, J, B, magnetyzacja):
        energia1 = 0 # czyli tylko suma iloczynów spinów
        for i in range(n-1):
            for j in range(m-1):
                energia1 = energia1 + self.siatka[i][j] *(self.siatka[i+1][j] + self.siatka[i][j+1] )
        for i in range(n-1):
            energia1 = energia1 + self.siatka[i][j] *(self.siatka[i+1][j] + self.siatka[i][1] )
        for j in range(m-1):
            energia1 = energia1 + self.siatka[i][j] *(self.siatka[1][j] + self.siatka[i][j+1] )
        energia1 = energia1 + self.siatka[n-1][m-1] *(self.siatka[1][m-1] + self.siatka[n-1][1] )
        energia =  - J*energia1 - B*magnetyzacja
    #   print('Energia: ', energia)
        return energia

    def mikrokrok(self, n, m, beta, energia_stara, J, B, magnetyzacja):
        # random.randrange(20)	Returns a random integer from 0 to 19
        # losowanie spinu:
        i = random.randrange(n)
        j = random.randrange(m)
        # print(i, j)
        self.siatka[i][j] = - self.siatka[i][j] 
        energia_nowa = self.liczenie_energii(n, m, J, B, magnetyzacja) # liczymy jeszcze raz energię

        if (energia_nowa < energia_stara):
            pass # akceptujemy nowy spin
        else:
            p = random.random() #np.random.rand(1)
            P_delta_E = math.exp(- beta * (energia_nowa - energia_stara) )
            if(p < P_delta_E):
                pass # akceptujemy nowy spin
            else:
                self.siatka[i][j] = - self.siatka[i][j] #powrót do poprzedniego stanu
        return energia_nowa
        


    def licz_magnetyzacje(self, n, m, nr, obrazki): # i przy okazji rysuj obrazek
        magnetyzacja = 0
        img = Image.new('RGB', (10*n + 4, 10*m + 4), (255, 255, 255)) # rozmiar obrazka zmienia się w zależności od rozmiarów siatki
        klatka = ImageDraw.Draw(img)
        wys = 10
        for i in range(n):
            for j in range(m):
                spin = self.siatka[i][j]
                if spin == 1 :
                    klatka.multiline_text((4 + i*wys, j*wys), "+", fill=(0, 0, 0))
                else:
                    klatka.multiline_text((4+i*wys, j*wys), "-", fill=(0, 0, 0))
                    # jeszcze kolorki + i - pozmieniać
                magnetyzacja = magnetyzacja + spin
        magnetyzacja_cała = magnetyzacja / (n*m)
        #print('Magnetyzacja: ', magnetyzacja_cała)
#        img.show()
        if (prefix != 'brak'):
            img.save(prefix + str(nr) +'.png') # dodać warunek na brak nazwy
        obrazki.append(img)
        return magnetyzacja_cała
    
    def makrokroki(s, n, m, J, B, beta, liczba_krokow, obrazki, magnetyzacje):
        for i in tqdm.tqdm(range(liczba_krokow)):
        #    time.sleep(1)
    #    for i in range(liczba_krokow):
            magnetyzacja = s.licz_magnetyzacje(n, m, i, obrazki)
            
            magnetyzacje.append(magnetyzacja)
        #    print('Magnetyzacja: ', magnetyzacja)
                #zapisanie magnetyzacji do pliku
            magnetyzacja_suma = magnetyzacja * (n*m)
            stara_energia = s.liczenie_energii(n, m, J, B, magnetyzacja_suma) 

            for k in range(n*m):
                energia = s.mikrokrok(n, m, beta, stara_energia, J, B, magnetyzacja_suma) 
                stara_energia = energia


# wczytywanie parametrów
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', default = 7)
parser.add_argument('-j', '--J', default = 1)
parser.add_argument('-b', '--beta', default = 1)
parser.add_argument('-c', '--B', default = 1)

parser.add_argument('-k', '--kroki', default = 4) # liczba kroków
parser.add_argument('-s', '--spiny', default = 0.5) # początkowa gęstość spinów
# opcjonalne:
# nazwę pliku z obrazkami (prefix, do którego program dodaje mumer kroku; jeżeli parametr
#  nie zostanie podany, obrazki się nie generują)
parser.add_argument('-o', '--obrazki', default = 'brak')
# nazwę pliku z animacją (jeżeli parametr nie zostanie podany, animacja się nie generuje)
parser.add_argument('-a', '--animacja', default = 'brak')
# nazwę pliku z magnetyzacją (jeżeli parametr nie zostanie podany, magnetyzacja się nie zapisuje)
parser.add_argument('-m', '--magnetyzacja', default = 'brak')


args = parser.parse_args()

n = int(args.n)
m = n # tego nie było, ale w sumie czemu nie - siatka nie musi być kwadratowa
J = float(args.J)
beta = float(args.beta)
B = float(args.B)
liczba_krokow = int(args.kroki) # makrokroków 1 * liczba spinów
gestosc_spinow = float(args.spiny)

#prefix = 'ising'

prefix = args.obrazki
animacja = args.animacja
plik_magnetyzacja = args.magnetyzacja

obrazki = []

magnetyzacje = []

symulacja1 = Symulacja(n, m, gestosc_spinow)
symulacja1.makrokroki(n, m, J, B, beta, liczba_krokow, obrazki, magnetyzacje)


if plik_magnetyzacja != 'brak':
    with open(plik_magnetyzacja, 'w') as f:
        for m in magnetyzacje:
            f.write(str(m) + '\n')


if animacja != 'brak':      
    obrazki[0].save(animacja + '.gif',
               save_all=True, append_images=obrazki[1:], duration=100, loop=1)
               # loop odpowiada za to, czy filmik zapętla się w nieskończoność, czy nie

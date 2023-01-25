import time
import numpy as np

import random
import math
import tqdm

class Timer:
    times = []

    def __init__(
        self,
        text="Czas wykonania: {:0.7f} sekund",
        logger=print,
    ):
        self._start_time = None
        self.text = text
        self.logger = logger

    def start(self):
        self._start_time = time.perf_counter()


    def stop(self):

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        self.times.append(elapsed_time)

        if self.logger:
            self.logger(self.text.format(elapsed_time))

        return elapsed_time

    def average(self):
        av = sum(self.times) / len(self.times)
        return av

    def max_time(self):
        max_t = max(self.times)
        return max_t

    def min_time(self):
        min_t = min(self.times)
        return min_t

    def sdev(self):
        return np.std(self.times)
    
####################################################



n = 10 # rozmiar siatki
m = n # tego nie było, ale w sumie czemu nie - siatka nie musi być kwadratowa
J = 1
beta = 1
B = 1
liczba_krokow = 100 # liczba kroków; makrokroków 1 * liczba spinów
gestosc_spinow = 0.5 # początkowa gęstość spinów


def nowa_siatka(n, m, gestosc_spinow):
    siatka = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            spin = random.random() #np.random.rand(1)
            if spin < gestosc_spinow :
                spin = 1
            else:
                spin = -1
            siatka [i][j] = spin
    return siatka

def liczenie_energii(n, m, J, B, magnetyzacja, numba_siatka):
    energia1 = 0 # czyli tylko suma iloczynów spinów
    for i in range(n-1):
        for j in range(m-1):
            energia1 = energia1 + numba_siatka[i][j] *(numba_siatka[i+1][j] + numba_siatka[i][j+1] )
    for i in range(n-1):
        energia1 = energia1 + numba_siatka[i][j] *(numba_siatka[i+1][j] + numba_siatka[i][1] )
    for j in range(m-1):
        energia1 = energia1 + numba_siatka[i][j] *(numba_siatka[1][j] + numba_siatka[i][j+1] )
    energia1 = energia1 + numba_siatka[n-1][m-1] *(numba_siatka[1][m-1] + numba_siatka[n-1][1] )
    energia =  - J*energia1 - B*magnetyzacja
    #   print('Energia: ', energia)
    return energia

def mikrokrok(n, m, beta, energia_stara, J, B, magnetyzacja, numba_siatka):
    i = random.randrange(n)
    j = random.randrange(m)
        # print(i, j)
    numba_siatka[i][j] = - numba_siatka[i][j] 
    energia_nowa = liczenie_energii(n, m, J, B, magnetyzacja, numba_siatka) # liczymy jeszcze raz energię

    if (energia_nowa < energia_stara):
        pass # akceptujemy nowy spin
    else:
        p = random.random() #np.random.rand(1)
        P_delta_E = math.exp(- beta * (energia_nowa - energia_stara) )
        if(p < P_delta_E):
            pass # akceptujemy nowy spin
        else:
            numba_siatka[i][j] = - numba_siatka[i][j] #powrót do poprzedniego stanu
    return energia_nowa

def licz_magnetyzacje(n, m, numba_siatka): # i przy okazji rysuj obrazek
    magnetyzacja = 0
    for i in range(n):
        for j in range(m):
            spin = numba_siatka[i][j]                    
            magnetyzacja = magnetyzacja + spin
    magnetyzacja_cała = magnetyzacja / (n*m)
    return magnetyzacja_cała

def makrokroki(n, m, J, B, beta, liczba_krokow):
    numba_siatka = nowa_siatka(n, m, gestosc_spinow)
    for i in tqdm.tqdm(range(liczba_krokow)):
        magnetyzacja = licz_magnetyzacje(n, m, numba_siatka)
        magnetyzacja_suma = magnetyzacja * (n*m)
        stara_energia = liczenie_energii(n, m, J, B, magnetyzacja_suma, numba_siatka) 

        for k in range(n*m):
            energia = mikrokrok(n, m, beta, stara_energia, J, B, magnetyzacja_suma, numba_siatka) 
            stara_energia = energia



t = Timer()

'''t.start()
time.sleep(1)
t.stop()

t.start()
time.sleep(1.5)
t.stop() 

t.start()
time.sleep(2)
t.stop()'''  

for i in range(10):
    t.start()
    makrokroki(n, m, J, B, beta, liczba_krokow)
    t.stop()

print(f'Średni czas wykonania funkcji: {t.average()}')
print(f'Maksymalny czas wykonania funkcji: {t.max_time()}')
print(f'Minimalny czas wykonania funkcji: {t.min_time()}')
print(f'Odchylenie standardowe: {t.sdev()}')







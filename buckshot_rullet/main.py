naboje = []
ostry_naboj = 0
pusty_naboj = 0
o =0
from random import *
# piwo - przeładowuje strzelbe
# lupa - pozwala zobaczyć jaki jest nabój
# andrenalina - pozwala zabrać przedmiot innemu graczowi
# piła ręczna - podwaja obrażenia strzelby na 2 tury
# inwenter - zmienia nabój w komorze, czyli zamienia pusty nabój na ostry lub odwrotnie
# telefon jednorazowy - tajemniczy głos z telefonu mówi ci przyszłość
# przeterminowane tabletki - leczą 2 zdrowia, ale jest szansa 75%, że zaszkodzą i zabiorą 1 zdrowie
# kajdanki - unieruchamia przeciwnika na 2 tury
# papierosy - leczą 1 zdrowie 
przedmioty = ["piwo", "lupa", "andrenalina", "piła ręczna", "inwenter", "telefon jednorazowy", "przeterminowane tabletki", "kajdanki", "papierosy"]
class Postać:
    def __init__(self, nazwa, zdrowie):
        self.nazwa = nazwa
        self.zdrowie = zdrowie
        self.mzdrowie = zdrowie
        self.co = []
        self.pzedmioty = []
        self.niezakajdankowany = True
    def strzel(self, cel):
        if naboje[0] == "ostry":
            cel.zdrowie -= 1
            naboje.pop(0)
            print(f"{self.nazwa} strzelił do {cel.nazwa} ostrym nabojem! Zdrowie {cel.nazwa} wynosi teraz {cel.zdrowie}.")
        else:
            naboje.pop(0)
            print(f"{self.nazwa} próbował strzelić do {cel.nazwa}, ale nabój był pusty!")
    def piwo(self):
        if "piwo" in self.pzedmioty:
            print(f"{self.nazwa} wypił piwo, dlatego przeładował strzelbe i wyrzucił{naboje[0]}.")
            self.pzedmioty.remove("piwo")
            naboje.pop(0)
        else:
            print(f"{self.nazwa} nie ma piwa, więc nie może przeładować strzelby.")
    def papierosy(self):
        if "papierosy" in self.pzedmioty:
            print(f"{self.nazwa} zapalił papierosa, więc odzyskał 1 zdrowie.")
            self.zdrowie += 1
            self.pzedmioty.remove("papierosy")
            if self.zdrowie > self.mzdrowie:
                self.zdrowie = self.mzdrowie
        else:
            print(f"{self.nazwa} nie ma papierosów, więc nie może zapalić.")
    def lupa(self):
        if "lupa" in self.pzedmioty:
            print(f"lupa {self.nazwa} pozwala mu zobaczyć, że nabój to {naboje[0]}.")
        else:
            print(f"{self.nazwa} nie ma lupy, więc nie może sprawdzić naboju.")
    def adrenalina(self, cel, rzecz):
        if "andrenalina" in self.pzedmioty:
            cel.przedmioty.remove(rzecz)
            print(f"{self.nazwa} użył adrenaliny, aby zabrać {rzecz} od {cel.nazwa}.")
            self.pzedmioty.append(rzecz)
            self.pzedmioty.remove("andrenalina")
        else:
            print(f"{self.nazwa} nie ma adrenaliny, więc nie może zabrać przedmiotu.")
    def inwenter(self):
        if "inwenter" in self.pzedmioty:
            if naboje[0] == "ostry":
                naboje[0] = "pusty"
            elif naboje[0] == "pusty":
                naboje[0] = "ostry"
        else:
            print(f"{self.nazwa} nie ma inwentera, więc nie może zmienić naboju.")
    def telefon(self):
        if "telefon jednorazowy" in self.pzedmioty:
            lo = randint(1,len(naboje)-1)
            while lo in self.co:
                lo = randint(1,len(naboje)-1)
            self.co.append(lo)
            print(f"Tajemniczy głos mówi do {self.nazwa}: {lo+1+o} nabój to {naboje[lo]} nabój.")
            self.pzedmioty.remove("telefon jednorazowy")
    def tabletki(self):
        if "przeterminowane tabletki" in self.pzedmioty:
            szansa = randint(1,100)
            if szansa <= 75:
                self.zdrowie -= 1
                print(f"{self.nazwa} wziął przeterminowane tabletki i zaszkodziły mu! Stracił 1 zdrowie.")
            else:
                self.zdrowie += 2
                print(f"{self.nazwa} wziął przeterminowane tabletki i wyzdrowiał! Zyskał 2 zdrowia.")
            self.pzedmioty.remove("przeterminowane tabletki")
        else:
            print(f"{self.nazwa} nie ma przeterminowanych tabletek, więc nie może ich wziąć.")
    def kajdanki(self, cel):
        if "kajdanki" in self.pzedmioty:
            print(f"{self.nazwa} użył kajdanek, aby unieruchomić {cel.nazwa} na 2 tury.")
            self.pzedmioty.remove("kajdanki")
            cel.niezakajdankowany = False
        else:
            print(f"{self.nazwa} nie ma kajdanek, więc nie może unieruchomić przeciwnika.")
    def pokaz_przedmioty(self):
        if self.pzedmioty:
            print(f"{self.nazwa} ma następujące przedmioty: {', '.join(self.pzedmioty)}")
        else:
            print(f"{self.nazwa} nie ma żadnych przedmiotów.")
    def czy_zyje(self):
        return self.zdrowie > 0
    def pokaz_stan(self):
        print(f"{self.nazwa} ma {self.zdrowie} zdrowia.")
    def następna(self):
        for i in range(len(self.co)):
            self.co.pop(i)
jak = input("jak chcesz mieć nick: ")
r = 1
while not r == 4:
    if r == 1:
        gracz1 = Postać(jak, 3)
        gracz2 = Postać("DEALER", 3)
    if r == 2:
        gracz1 = Postać(jak,4)
        gracz2 = Postać("DEALER",4)
    if r == 3:
        gracz1 = Postać(jak,5)
        gracz2 = Postać("DEALER",5)
    r1 = randint(1,6)
    for i in range(r1):
        r = randint(1,2)
        if r == 1:
            naboje.append("ostry")
            ostry_naboj += 1
        else:
            naboje.append("pusty")
            pusty_naboj += 1
    naboje.append("ostry")
    ostry_naboj += 1
    naboje.append("pusty")
    pusty_naboj +=1
    print(f"takie są naboje w strzelbie na tę rundę: ostre_naboje: {ostry_naboj},puste_naboje: {pusty_naboj}")
    while not len(naboje) == 0:
        break
    break
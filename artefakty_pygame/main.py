from random import *
import json
import os
import pygame
import time
def usuń_plik(plik):
    try:
        os.remove(plik)
        print("Plik został usunięty.")
    except FileNotFoundError:
        print("Plik nie istnieje.")
def zapisz_gre(stan_gry, plik):
    with open(f"gry/artefakty_pygame/saves/{plik}.json", "w") as f:
        json.dump(stan_gry, f)
    print("Gra zapisana!")
def wczytaj_gre(plik):
    try:
        with open(f"gry/artefakty_pygame/saves/{plik}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Brak zapisu gry.")
        return None
class dodanie_stat:
    def __init__(self, nazwa, obrona, atak, tury, wytrzymałość):
        self.nazwa = nazwa
        self.obrona = obrona
        self.atak = atak
        self.tury = tury
        self.wytrzymałość = wytrzymałość
    def po(self):
        return {"nazwa":self.nazwa,
                "obrona":self.obrona,
                "atak":self.atak,
                "tury":self.tury,
                "wytrzymałość":self.wytrzymałość}
    def wczytaj(self,wnazwa,wobrona,watak,wtury,wwytrzymałość):
        self.nazwa = wnazwa
        self.obrona = wobrona
        self.atak = watak
        self.tury = wtury
        self.wytrzymałość = wwytrzymałość
zbroje_def = {
    "czarno_zbroja": ("czarno zbroja", {"głowa":0, "klatka":20, "lręka":5, "pręka":5, "brzuch":20, "lrzebro":10, "przebro":10, "lnoga":0, "pnoga":0}, 10, 0, (100, 150)),
    "brak_zbroi": ("brak zbroi", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 0, (0, 0)),
    "jasno_zbroja": ("jasno zbroja", {"głowa":20, "klatka":20, "lręka":10, "pręka":10, "brzuch":30, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 0, (100, 120)),
    "łuska_smoka": ("łuska smoka", {"głowa":0, "klatka":300, "lręka":0, "pręka":0, "brzuch":500, "lrzebro":50, "przebro":50, "lnoga":0, "pnoga":0}, 500, 0, (500, 500)),
    "sdz_metalowa_zbroja": ("sdz metalowa zbroja", {"głowa":40, "klatka":50, "lręka":10, "pręka":10, "brzuch":50, "lrzebro":40, "przebro":40, "lnoga":60, "pnoga":60}, 0, 0, (10, 50)),
    "metalowa_zbroja": ("metalowa zbroja", {"głowa":50, "klatka":100, "lręka":70, "pręka":70, "brzuch":120, "lrzebro":100, "przebro":100, "lnoga":80, "pnoga":80}, 0, 0, (100, 150)),
    "zbroja_z_błota_i_liści": ("zbroja z błota i liści", {"głowa":0, "klatka":5, "lręka":0, "pręka":0, "brzuch":10, "lrzebro":1, "przebro":1, "lnoga":5, "pnoga":5}, 0, 0, (10, 20))
}
bronie_def = {
    "brak_broni": ("brak broni", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 0, (0, 0)),
    "łuk": ("łuk", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 50, 0, (50, 100)),
    "topur": ("topur", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 500, (500, 500)),
    "włócznia": ("włócznia", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 20, (100, 200)),
    "ostra_włócznia": ("ostra włócznia", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 50, (100, 150)),
    "cięki_patyk": ("cięki patyk", {"głowa":0, "klatka":0, "lręka":0, "pręka":0, "brzuch":0, "lrzebro":0, "przebro":0, "lnoga":0, "pnoga":0}, 0, 10, (10, 20))
}
def stworz_przedmiot(definicja):
    nazwa, obrona, atak, tury, (min_w, max_w) = definicja
    wartosc = randint(min_w, max_w)
    return dodanie_stat(nazwa, obrona, atak, tury, wartosc)
def daj_zbroje(nazwa):
    return stworz_przedmiot(zbroje_def[nazwa])
def daj_bron(nazwa):
    return stworz_przedmiot(bronie_def[nazwa])
class Postać:
    def __init__(self, istota, imie, głowa, klatka, lręka, pręka, brzuch, lrzebro, przebro, lnoga, pnoga, napojenie,mnapojenie, głód, mgłód, atak, obrona, zbroja, broń,chce_zatakować,musi):
        self.imie = imie
        self.głód = głód
        self.mgłód = mgłód
        self.napojenie = napojenie
        self.mnapojenie = mnapojenie
        self.istota = istota
        self.głowa = głowa  # 20%
        self.klatka = klatka  # 25%
        self.lręka = lręka  # 5%
        self.pręka = pręka
        self.brzuch = brzuch  # 7.5%
        self.lrzebro = lrzebro  # 1.25%
        self.przebro = przebro
        self.lnoga = lnoga  # 17.5%
        self.pnoga = pnoga
        self.artefakty = {1: None, 2: None, 3: None}
        self.za_atak = atak
        self.za_obrona = obrona
        self.atak = atak
        self.obrona = obrona
        self.zbroja = zbroja
        self.broń = broń
        self.umiejętności = []
        self.ciało = głowa + klatka + lręka + pręka + brzuch + lrzebro + przebro + lnoga + pnoga
        self.nczęści_ciała = [self.głowa, self.klatka, self.lręka, self.pręka, self.brzuch, self.lrzebro, self.przebro,self.lnoga, self.pnoga]
        self.części_ciała = ["głowa", "klatka", "lręka", "pręka", "brzuch", "lrzebro", "przebro", "lnoga", "pnoga"]
        self.ogłuszony = False
        self.czas_ogłuszenia = 0
        self.chce = chce_zatakować
        self.musi = musi
        self.tury = broń.tury
        self.drużyna = []
        self.wrogowie = []
        self.ekwipunek = {"ciękie patyki": 0,"kamienie": 0,"kawałki metalu": 0,"siekiera":0}
        self.oszczędzenie = 0
        self.relacje = {}
        # Do obsługi działania artefaktów
        self.wochuk_uses = {}  # przeciwnik: ile razy użyto
        self.cozwoj_uses = 0
    def wczytaj(self,wimie,wgłód,wmgłód,wnapojenie,wmnapojenie,wistota,wgłowa,wklatka,wlręka,wpręka,wbrzuch,wlrzebro,wprzebro,wlnoga,wpnoga,wartefakty,wza_atak,wza_obrona,watak,wobrona,wzbroja,wbronie,wumiejętności,wciało,wnczęści_ciała,wczęści_ciała,wogłuszony,wczas_ogłuszenia,wchce,wmusi,wtury,wdrużyna,wwrogowie,wekwipunek,woszczędzenie,wrelacje,wwochuk_uses,wcozwoj_uses):
        self.imie = wimie
        self.głód = wgłód
        self.mgłód = wmgłód
        self.napojenie = wnapojenie
        self.mnapojenie = wmnapojenie
        self.istota = wistota
        self.głowa = wgłowa
        self.klatka = wklatka
        self.lręka = wlręka
        self.pręka = wpręka
        self.brzuch = wbrzuch
        self.lrzebro = wlrzebro
        self.przebro = wprzebro
        self.lnoga = wlnoga
        self.pnoga = wpnoga
        self.artefakty = wartefakty
        self.za_atak = wza_atak
        self.za_obrona = wza_obrona
        self.atak = watak
        self.obrona = wobrona
        self.zbroja.wczytaj(wzbroja["nazwa"],wzbroja["obrona"],wzbroja["obrona"],wzbroja["tury"],wzbroja["wytrzymałość"])
        self.broń.wczytaj(wbronie["nazwa"],wbronie["obrona"],wbronie["obrona"],wbronie["tury"],wbronie["wytrzymałość"])
        self.umiejętności = wumiejętności
        self.ciało = wciało
        self.nczęści_ciała = wnczęści_ciała
        self.części_ciała = wczęści_ciała
        self.ogłuszony = wogłuszony
        self.czas_ogłuszenia = wczas_ogłuszenia
        self.chce = wchce
        self.musi = wmusi
        self.tury = wtury
        self.drużyna = wdrużyna
        self.wrogowie = wwrogowie
        self.ekwipunek = wekwipunek
        self.oszczędzenie = woszczędzenie
        self.relacje = wrelacje
        self.wochuk_uses = wwochuk_uses
        self.cozwoj_uses = wcozwoj_uses
    def po(self):
        return {
            "imie": self.imie,
            "głód": self.głód,
            "mgłód": self.mgłód,
            "napojenie": self.napojenie,
            "mnapojenie": self.mnapojenie,
            "istota": self.istota,
            "głowa": self.głowa,
            "klatka": self.klatka,
            "lręka": self.lręka,
            "pręka": self.pręka,
            "brzuch": self.brzuch,
            "lrzebro": self.lrzebro,
            "przebro": self.przebro,
            "lnoga": self.lnoga,
            "pnoga": self.pnoga,
            "artefakty": self.artefakty,
            "za_atak": self.za_atak,
            "za_obrona": self.za_obrona,
            "atak": self.atak,
            "obrona": self.obrona,
            "zbroja": self.zbroja.po() if self.zbroja else None,
            "broń": self.broń.po() if self.broń else None,
            "umiejętności": self.umiejętności,
            "ciało": self.ciało,
            "nczęści_ciała": self.nczęści_ciała,
            "części_ciała": self.części_ciała,
            "ogłuszony": self.ogłuszony,
            "czas_ogłuszenia": self.czas_ogłuszenia,
            "chce": self.chce,
            "musi": self.musi,
            "tury": self.tury,
            "drużyna": self.drużyna,
            "wrogowie": self.wrogowie,
            "ekwipunek": self.ekwipunek,
            "oszczędzenie": self.oszczędzenie,
            "relacje": self.relacje,
            "wochuk_uses": self.wochuk_uses,
            "cozwoj_uses": self.cozwoj_uses
        }
    def napraw_zbroje(self,ilość: int):
        if self.zbroja is None or self.zbroja.wytrzymałość == 0:
            print(f"{self.imie} nie ma zbroi do naprawy.")
            return
        if self.zbroja.nazwa in ["metalowa zbroja", "sdz metalowa zbroja"]:
            if self.ekwipunek.get("kawałki metalu", 0) < ilość:
                print(f"{self.imie} nie ma wystarczająco materiału do naprawy.")
                return
            self.ekwipunek["kawałki metalu"] -= ilość
            naprawa = 10 * ilość
            stara_wytrzymałość = self.zbroja.wytrzymałość
            self.zbroja.wytrzymałość = min(self.zbroja.wytrzymałość + naprawa, 150)
            print(f"{self.imie} naprawił zbroję o {naprawa} punktów wytrzymałości({stara_wytrzymałość} → {self.zbroja.wytrzymałość}).")
    def sprawdź_ekwipunek(self):
        print(f"ekwipunek postaci: {self.imie}")
        for przedmiot, ilość in self.ekwipunek.items():
            if ilość > 0:
                print(f"{przedmiot}: {ilość}")
    def zadaj_obrażenia(self, jaka_część: str, ile: int):
        setattr(self, jaka_część, getattr(self, jaka_część) - ile)
    def dodaj_relacje(self, postac, staty_relacji: int):
        if postac in self.relacje.values():
            self.relacje[postac] += staty_relacji
        else:
            self.relacje[postac] = staty_relacji
    def dodaj_wroga(self, wróg):
        self.wrogowie.append(wróg)
    def oszczędzanie(self, o_ile: float):
        self.oszczędzenie += o_ile
    def oszczędzony(self):
        return self.oszczędzenie > 100
    def synchronizacja(self, protokuł: int):

        # synchronizacja hp
        if protokuł == 3:
            self.ciało = sum(self.nczęści_ciała)

        # limity głodu/staminy
        elif protokuł == 2:
            self.głód = max(0, min(self.głód, self.mgłód))
            self.napojenie = max(0, min(self.napojenie, self.mnapojenie))
            self.oszczędzenie = max(0, min(self.oszczędzenie, 100))

        # statystyki
        elif protokuł == 1:

            # reset
            self.obrona = self.za_obrona.copy()
            self.atak = self.za_atak

            # goblin
            if self.istota == "goblin":

                if self.zbroja.nazwa not in ["łuska smoka", "brak zbroi"]:
                    print("Goblin może mieć tylko łuskę smoka!")
                    return

            else:

                if self.zbroja.nazwa == "łuska smoka":
                    print("Tylko goblin może nosić łuskę smoka!")
                    return

            # dodanie obrony zbroi
            if self.zbroja is not None:

                for część in self.obrona:
                    self.obrona[część] += self.zbroja.obrona.get(część, 0)

                self.atak += self.zbroja.atak

            # dodanie ataku broni
            if self.broń is not None:

                if self.broń.nazwa == "łuk" and self.istota == "elf":
                    self.atak += self.broń.atak + 20
                else:
                    self.atak += self.broń.atak
    def dodaj_osobę_do_drużyny_nieoficjalnie(self, p1):
        if p1 not in self.drużyna:
            self.drużyna.append(p1)
    def dodaj_osobę_do_drużyny_oficjalnie(self, p1, p2):
        if p1 not in self.drużyna:
            p2.drużyna.append(p1)
            p1.drużyna.append(p2)
        else:
            print("już jest")
    def dodaj_osoby_do_drużyny_oficjalnie(self, p1, p2, p3):
        if p1 not in p2.drużyna:
            p2.drużyna.append(p1)
        if p3 not in p2.drużyna:
            p2.drużyna.append(p3)
        if p1 not in p3.drużyna:
            p3.drużyna.append(p1)
        if p2 not in p3.drużyna:
            p3.drużyna.append(p2)
        if p3 not in p1.drużyna:
            p1.drużyna.append(p3)
        if p2 not in p1.drużyna:
            p1.drużyna.append(p2)
    def zaatakuj(self, wrog, jaka_czesc: str):
        obrona_czesci = wrog.obrona[jaka_czesc]
        if self.chce or self.musi:
            if wrog in self.drużyna:
                print("chcesz zatakować swojego? co jest z tabą nie tak")
                return
            elif self.broń.tury > 0:
                self.broń.tury -= 1
                return
            elif self.broń.wytrzymałość == 0:
                print(f"{self.imie} nie może zaatakować, bo {self.bronie.nazwa} jest stępiona!")
                return
            elif jaka_czesc == "głowa" and randint(1, 100) != 1:
                print(f"{self.imie} chybił atak w głowę {wrog.imie}!")
                return
            elif wrog.istota == "goblin" and jaka_czesc == "głowa" and randint(1, 1000) != 1:
                print(f"{self.imie} chybił atak w głowę goblina o imieniu {wrog.imie}!")
                return
            elif self.broń.nazwa in ["włócznia", "ostra włócznia"]:
                for i in range(3):
                    obrazenia = max(0, randint(int(self.atak - (self.atak*0.1)), int(self.atak)) - obrona_czesci)
                    obrażenia_obrony = obrona_czesci*0.1
                    self.obrona[jaka_czesc] = max(0, self.obrona[jaka_czesc] - obrażenia_obrony)
                    aktualne_hp = getattr(wrog, jaka_czesc)
                    nowe_hp = max(0, aktualne_hp - obrazenia)
                    setattr(wrog, jaka_czesc, nowe_hp)
                    rzeczywiste_obrazenia = aktualne_hp - nowe_hp
                    wrog.ciało = max(0, wrog.ciało - rzeczywiste_obrazenia)
                    print(f"{wrog.imie} dostał {rzeczywiste_obrazenia} obrażeń w {jaka_czesc}!")
                    print(f"{wrog.imie} ma {nowe_hp} HP w {jaka_czesc}")
                if not self.broń.wytrzymałość == 0:
                    self.broń.wytrzymałość = max(0,self.broń.wytrzymałość - 1)
                if self.broń.wytrzymałość == 0:
                    print(f"{self.imie} nie może zaatakować, ponieważ {self.broń.nazwa} jest stępiona!")
                    return
            else:
                obrazenia = max(0, randint(int(self.atak - (self.atak * 0.1)), int(self.atak)) - obrona_czesci)
                obrażenia_obrony = obrona_czesci*0.1
                self.obrona[jaka_czesc] = max(0, self.obrona[jaka_czesc] - obrażenia_obrony)
                aktualne_hp = getattr(wrog, jaka_czesc)
                nowe_hp = max(0, aktualne_hp - obrazenia)
                setattr(wrog, jaka_czesc, nowe_hp)
                rzeczywiste_obrazenia = aktualne_hp - nowe_hp
                wrog.ciało = max(0, wrog.ciało - rzeczywiste_obrazenia)
                print(f"{wrog.imie} dostał {rzeczywiste_obrazenia} obrażeń w {jaka_czesc}!")
                print(f"{wrog.imie} ma {nowe_hp} HP w {jaka_czesc}")
            if not self.broń.wytrzymałość == 0:
                self.broń.wytrzymałość = max(0,self.broń.wytrzymałość - 1)
        else:
            if not self.chce:
                print("nie chcę atakować")
    def zyje(self):
        return self.ciało > 0 or self.głowa > 0
    def dodaj_artefakt(self, nazwa, wymuszony_slot):
            self.artefakty[wymuszony_slot] = nazwa
    def ma_artefakt(self, nazwa: str):
        return nazwa in self.artefakty.values()
    def użyj_wochuk(self):
        if not self.ma_artefakt("wochuk"):
            return f"{self.imie} nie posiada artefaktu Wochuk."
        for przeciwnik in self.wrogowie:
            użycia = self.wochuk_uses.get(przeciwnik, 0)
            szansa = max(0.5 - (użycia * 0.1), 0)
            if random() < szansa:
                przeciwnik.ogłuszony = True
                print(f"{przeciwnik.imie} został ogłuszony przez Wochuka!")
                self.wochuk_uses[przeciwnik] = użycia + 1
                self.czas_ogłuszenia = 3
            else:
                print(f"{przeciwnik.imie} oparł się działaniu Wochuka.")
    def użyj_cozwój(self, przeciwnik):
        if "cozwój" not in self.artefakty:
            return f"{self.imie} nie posiada artefaktu Cozwój."
        if self.cozwoj_uses >= 10:
            return f"{self.imie} zużył już cały artefakt Cozwój."
        self.cozwoj_uses += 1
        # Cofnięcie rozwoju: brak umiejętności
        przeciwnik.umiejętności = []
        return f"{przeciwnik.imie} został cofnięty do epoki kamienia łupanego!"
    def __str__(self):
        return f"{self.imie}({self.istota}):\n  Życie={self.ciało}\n  Atak={self.atak}\n  Obrona={self.obrona}\n  punkty oszczędzienia = {self.oszczędzenie}\n  broń: {self.bronie.nazwa}\n  zbroja: {self.zbroja.nazwa}"
pos1 = Postać(
    "człowiek", "Tomek",
    200.0, 250.0, 50.0, 10.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    10.0, {"głowa": 10, "klatka": 10, "lręka": 5, "pręka": 0, "brzuch": 10, "lrzebro": 10, "przebro": 10, "lnoga": 5, "pnoga": 5},
    daj_zbroje("zbroja_z_błota_i_liści"),
    daj_bron("cięki_patyk"),
    True, False
)
pos2 = Postać(
    "goblin", "Buzg",
    200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000.0, 175000.0,
    200.0, 300.0, 50.0, 100,
    0.0, {"głowa": 100, "klatka": 200, "lręka": 150, "pręka": 150, "brzuch": 200, "lrzebro": 50, "przebro": 50, "lnoga": 300, "pnoga": 300, "ogon": 500},
    daj_zbroje("brak_zbroi"),
    daj_bron("topur"),
    False, True
)
pos3 = Postać(
    "elf", "Elenor",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False
)
pos4 = Postać(
    "elf", "Romeo",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("czarno_zbroja"),
    daj_bron("łuk"),
    True, False
)
pos5 = Postać(
    "elf", "Rukur",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True
)
pos6 = Postać(
    "elf", "Rokil",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, {"głowa": 1, "klatka": 5, "lręka": 2, "pręka": 2, "brzuch": 10, "lrzebro": 5, "przebro": 5, "lnoga": 5, "pnoga": 5},
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True
)
pos1.dodaj_relacje(pos3.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos1.dodaj_relacje("gracz", {"zaufanie": 0, "decyzje": []})
pos1.synchronizacja(1)
pos1.ekwipunek["ciękie patyki"] += 1
pos1.ekwipunek["kawałki metalu"] += 10
pos2.ogon = 1000000.0
pos2.części_ciała.append("ogon")
pos2.nczęści_ciała.append(pos2.ogon)
pos2.synchronizacja(3)
pos2.synchronizacja(1)
pos2.ekwipunek["siekiera"] += 1
pos3.dodaj_relacje(pos1.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos4.synchronizacja(1)
pos5.synchronizacja(1)
pos6.synchronizacja(1)
def gra():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    x = 100
    y = 100
    speed = 3  # pixel po pixelu
    stamina = 100
    frame = 0
    player_idle1 = pygame.image.load("gry/artefakty_pygame/Tomek.png").convert_alpha()
    player_idle2 = pygame.image.load("gry/artefakty_pygame/Tomek5.png").convert_alpha()
    player_walk1 = pygame.image.load("gry/artefakty_pygame/Tomek1.png").convert_alpha()
    player_walk2 = pygame.image.load("gry/artefakty_pygame/Tomek2.png").convert_alpha()
    player_walk3 = pygame.image.load("gry/artefakty_pygame/Tomek3.png").convert_alpha()
    player_walk4 = pygame.image.load("gry/artefakty_pygame/Tomek4.png").convert_alpha()
    

    player_idle1 = pygame.transform.scale(player_idle1, (200, 200))
    player_idle2 = pygame.transform.scale(player_idle2, (200, 200))
    player_walk1 = pygame.transform.scale(player_walk1, (200, 200))
    player_walk2 = pygame.transform.scale(player_walk2, (200, 200))
    player_walk3 = pygame.transform.scale(player_walk3, (200, 200))
    player_walk4 = pygame.transform.scale(player_walk4, (200, 200))
    font = pygame.font.SysFont(None, 36)
    player = player_idle1
    while True:
        keys = pygame.key.get_pressed()
        lista = [keys[pygame.K_w],keys[pygame.K_UP],keys[pygame.K_s],keys[pygame.K_DOWN],keys[pygame.K_a],keys[pygame.K_RIGHT],keys[pygame.K_d],keys[pygame.K_LEFT]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if not any(lista):
            frame = 0
            if player in [player_walk1, player_walk2]:
                player = player_idle1
            elif player in [player_walk3, player_walk4]:
                player = player_idle2
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y += speed

            frame += 1

            if frame < 5:
                player = player_walk1
            if frame > 5:
                player = player_walk2
            if frame >= 10:
                frame = 0
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            y -= speed

            frame += 1

            if frame < 5:
                player = player_walk3
            if frame > 5:
                player = player_walk4
            if frame >= 10:
                player = player_walk3
                frame = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x += speed
        if keys[pygame.K_q]:
            pygame.quit()
            exit()
        if stamina >= 100:
            stamina = 100
        if stamina <= 0:
            stamina = 0
        if keys[pygame.K_LSHIFT] and stamina > 0 and any(lista):
            speed = 8
            stamina -= 1
        if (not keys[pygame.K_LSHIFT] or stamina <= 0):
            speed = 3
            stamina += 1
        screen.fill((0, 255, 0))
        screen.blit(player, (x, y))
        # tło paska
        pygame.draw.rect(screen,(100, 100, 100), (10, 50, 200, 20))

        # aktualna stamina
        pygame.draw.rect(screen, (0, 0, 255), (10, 50, 2 * stamina, 20))
        pygame.display.update()
        clock.tick(60)
gra()
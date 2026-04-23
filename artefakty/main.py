from random import *
import json
import os
def usuń_plik(plik):
    try:
        os.remove(plik)
        print("Plik został usunięty.")
    except FileNotFoundError:
        print("Plik nie istnieje.")
def zapisz_gre(stan_gry, plik):
    with open(f"gry/artefakty/saves/{plik}.json", "w") as f:
        json.dump(stan_gry, f)
    print("Gra zapisana!")
def wczytaj_gre(plik):
    try:
        with open(f"gry/artefakty/saves/{plik}.json", "r") as f:
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
mapa = {"miejsce treningowe1": ("\033[38;5;240m           ________________________\n"
                                " |    2   |                       |     3    |\n"
                                " |        |                       |          |\n"
                                " /\033[48;5;22m   \033[0m     ######################### \033[38;5;240m         \\\n"
                                "/  \033[48;5;22m \\  \033[0m \033[38;5;240m                        \033[0mElenor \033[38;5;240m        |     \\\n"
                                "|     |              \033[0mTomek      |\033[38;5;240m              |\n"
                                "|     /               \033[0m||       |||1\033[38;5;240m            |\n"
                                "|                               \033[0m|\033[38;5;240m              |\n"
                                "|                          /                   |\033[0m\n"
                                "\033[38;5;240m##########\033[48;5;22m#####\033[0m\033[38;5;240m################################\033[0m"),
        "miejsce treningowe2":("\033[38;5;240m           ________________________\n"
                                " |    1   |                       |     2    |\n"
                                " |        |                       |          |\n"
                                " /\033[48;5;22m   \033[0m     ######################### \033[38;5;240m         \\\n"
                                "/  \033[48;5;22m \\  \033[0m \033[38;5;240m                                       |     \\\n"
                                "|     |              \033[0mTomek    \033[0mElenor \033[38;5;240m\033[38;5;240m          |\n"
                                "|     /               \033[0m||       -||-\033[38;5;240m            |\n"
                                "|                               \033[0m\033[38;5;240m               |\n"
                                "\033[38;5;240m##########\033[48;5;22m#####\033[0m\033[38;5;240m################################\033[0m"),
        "miejsce treningowe3":("\033[38;5;240m           ________________________\n"
                                " |    1   |                       |     2    |\n"
                                " |        |                       |          |\n"
                                " /\033[48;5;22m   \033[0m     ######################### \033[38;5;240m         \\\n"
                                "/  \033[48;5;22m \\  \033[0m \033[38;5;240m                                       |     \\\n"
                                "|     |              \033[0mTomek      \033[38;5;240m               |\n"
                                "|     /               \033[0m||\033[38;5;240m                       |\n"
                                "|                                              |\n"
                                "|                          /                   |\033[0m\n"
                                "\033[38;5;240m###############################################\033[0m")
}
print(mapa["miejsce treningowe1"])
zbroje_def = {
    "czarno_zbroja": ("czarno zbroja", 20, 10, 0, (100, 150)),
    "brak_zbroi": ("brak zbroi", 0, 0, 0, (0, 0)),
    "jasno_zbroja": ("jasno zbroja", 20, 0, 0, (100, 120)),
    "łuska_smoka": ("łuska smoka", 500, 500, 0, (500, 500)),
    "sdz_metalowa_zbroja": ("sdz metalowa zbroja", 50, 0, 0, (10, 50)),
    "metalowa_zbroja": ("metalowa zbroja", 100, 0, 0, (100, 150)),
}
bronie_def = {
    "brak_broni": ("brak broni", 0, 0, 0, (0, 0)),
    "łuk": ("łuk", 0, 50, 0, (50, 100)),
    "topur": ("topur", 0, 500, 3, (500, 500)),
    "włócznia": ("włócznia", 0, 20, 0, (100, 200)),
    "ostra_włócznia": ("ostra włócznia", 0, 50, 0, (100, 150)),
}
patyki_def = {
    "cięki_patyk": ("cięki patyk", 0, 10, 0, (1, 15))
}
def stworz_przedmiot(definicja):
    nazwa, obrona, atak, tury, (min_w, max_w) = definicja
    wartosc = randint(min_w, max_w)
    return dodanie_stat(nazwa, obrona, atak, tury, wartosc)
def daj_zbroje(nazwa):
    return stworz_przedmiot(zbroje_def[nazwa])
def daj_bron(nazwa):
    return stworz_przedmiot(bronie_def[nazwa])
def daj_patyk(nazwa):
    return stworz_przedmiot(patyki_def[nazwa])
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
        self.zbroja = self.zbroja.wczytaj(wzbroja["nazwa"],wzbroja["obrona"],wzbroja["obrona"],wzbroja["tury"],wzbroja["wytrzymałość"])
        self.broń = self.broń.wczytaj(wbronie["nazwa"],wbronie["obrona"],wbronie["obrona"],wbronie["tury"],wbronie["wytrzymałość"])
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
    def dodaj_relacje(self, postac: Postać, staty_relacji: int):
        if postac in self.relacje.values():
            self.relacje[postac] += staty_relacji
        else:
            self.relacje[postac] = staty_relacji
    def dodaj_wroga(self, wróg: Postać):
        self.wrogowie.append(wróg)
    def oszczędzanie(self, o_ile: float):
        self.oszczędzenie += o_ile
    def oszczędzony(self):
        return self.oszczędzenie > 100
    def synchronizacja(self, protokuł: int):
        if protokuł == 4:
            self.ciało = sum(self.nczęści_ciała)
        elif protokuł == 5:
            self.głód = max(0, min(self.głód, self.mgłód))
            self.napojenie = max(0, min(self.napojenie, self.mnapojenie))
            self.oszczędzenie = max(0,min(self.oszczędzenie,100))
        elif self.istota == "goblin":
            if protokuł == 1:
                self.obrona = self.atak
            elif protokuł == 2:
                self.atak = self.obrona
            elif protokuł == 3:
                self.obrona = self.za_obrona
                self.atak = self.za_atak
                if self.zbroja.nazwa != "łuska smoka":
                    if self.zbroja.nazwa == "brak_zbroi":
                        pass
                    else:
                        print("Nie da się dać na goblina oprócz łuski smoka")
                else:
                    self.obrona += self.zbroja.obrona
                    self.atak += self.zbroja.atak
                    if self.broń and self.broń.nazwa in [b[0] for b in bronie_def.values()] + [p[0] for p in patyki_def.values()]:
                        self.atak += self.broń.atak
        else:
            if protokuł == 3:
                self.obrona = self.za_obrona
                self.atak = self.za_atak
                if self.zbroja.nazwa != "łuska smoka":
                    self.obrona += self.zbroja.obrona
                    self.atak += self.zbroja.atak
                else:
                    print("Chcesz dać komuś innemu niż goblinowi łuskę smoka. Co jest z tobą nie tak?")
                if self.broń and self.broń.nazwa in ["włócznia", "ostra włócznia"]:
                    if self.broń is not None:
                        if self.broń.nazwa == "łuk" and self.istota == "elf":
                            self.atak += self.broń.atak + 20
                        else:
                            self.atak += self.broń.atak
    def dodaj_osobę_do_drużyny_nieoficjalnie(self, p1: Postać):
        if p1 not in self.drużyna:
            self.drużyna.append(p1)
    def dodaj_osobę_do_drużyny_oficjalnie(self, p1: Postać, p2: Postać):
        if p1 not in self.drużyna:
            p2.drużyna.append(p1)
            p1.drużyna.append(p2)
        else:
            print("już jest")
    def dodaj_osoby_do_drużyny_oficjalnie(self, p1: Postać, p2: Postać, p3: Postać):
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
    def zaatakuj(self, wrog: Postać, jaka_czesc: str):
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
                    obrazenia = max(0, randint(int(self.atak - 20), int(self.atak)) - wrog.obrona)
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
                obrazenia = max(0, randint(int(self.atak - 20), int(self.atak)) - wrog.obrona)
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
    def użyj_cozwój(self, przeciwnik: Postać):
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
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    10.0, 20.0,
    daj_zbroje("brak_zbroi"),
    daj_patyk("cięki_patyk"),
    True, False
)

pos2 = Postać(
    "goblin", "Buzg",
    200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000.0, 175000.0,
    200.0, 300.0, 50.0, 100,
    0.0, 0.0,
    daj_zbroje("brak_zbroi"),
    daj_bron("topur"),
    False, True
)

pos3 = Postać(
    "elf", "Elenor",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 10.0, 100.0,
    5.0, 60.0,
    daj_zbroje("brak_zbroi"),
    daj_bron("brak_broni"),
    False, False
)

pos4 = Postać(
    "elf", "Romeo",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    5.0, 60.0,
    daj_zbroje("czarno_zbroja"),
    daj_bron("łuk"),
    True, False
)

pos5 = Postać(
    "elf", "Rukur",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 10.0, 100.0,
    5.0, 60.0,
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True
)

pos6 = Postać(
    "elf", "Rokil",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 10.0, 100.0,
    5.0, 60.0,
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True
)
pos1.dodaj_relacje(pos3.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos1.dodaj_relacje("gracz", {"zaufanie": 0, "decyzje": []})
pos1.synchronizacja(3)
pos1.ekwipunek["ciękie patyki"] += 1
pos1.ekwipunek["kawałki metalu"] += 10
pos2.ogon = 1000000.0
pos2.części_ciała.append("ogon")
pos2.nczęści_ciała.append(pos2.ogon)
pos2.synchronizacja(4)
pos2.synchronizacja(3)
pos2.synchronizacja(1)
pos2.ekwipunek["siekiera"] += 1
pos3.dodaj_relacje(pos1.imie, {"zaufanie": 20, "atak": 0, "decyzje": []})
pos4.synchronizacja(3)
pos5.synchronizacja(3)
class Gra:
    def __init__(self):
        pass
    def walka2(self):
        global liczba_fabuły
        if liczba_fabuły == 3:
            strażnik1_aktywny = pos5.zyje() or not pos5.oszczędzony()
            strażnik2_aktywny = pos6.zyje() or not pos6.oszczędzony()
            while pos1.zyje() or (strażnik1_aktywny and strażnik2_aktywny):
                wybor = input("1.zaatakuj\n2.czyn\n")
                if wybor == "1":
                    jaka_część = 0
                    while not jaka_część in pos5.części_ciała:
                        jaka_część = input("napisz jaką część ciała chcesz zaatakować: ")
                    pos1.zaatakuj(pos5,jaka_część)
                elif wybor == "2":
                    wybor = input("1.porozmawiaj\n2.uciekaj\n3.proś go o litość\n")
                    if wybor == "1":
                        input("Gracz: możemy porozmawiać?")
                        input("Strażnik: nie ma mowy. muszę cię złapać jesteś celem rządów manreda")
                        input("Gracz: co? dlaczego?")
                        input("strażnik: każdy człowiek jest celem. muszę cię złapać lub zabić(muwi to jagby chciałby przeprosić)")
                    elif wybor == "2":
                        input("uciekasz")
                        input("ale są za szybcy")
                        input("niestety nie udało ci się")
                    
                while True:
                    a = choice(pos1.części_ciała)
                    if not getattr(pos1, a) == 0:
                        break
                pos5.zaatakuj(pos1,a)
                while True:
                    b = choice(pos1.części_ciała)
                    if not getattr(pos1, b) == 0:
                        break
                pos6.zaatakuj(pos1,b)
        else:
            while pos1.zyje() and pos2.zyje():
                break
    def przygoda1(self):
        global liczba_fabuły
        if liczba_fabuły == 1:
            print(mapa["miejsce treningowe2"])
        elif liczba_fabuły == 2:
            print(mapa["miejsce treningowe1"])
        elif liczba_fabuły == 3:
            print(mapa["miejsce treningowe3"])
        wybor = input("wybierz gdzie chcesz iść: ")
        if wybor == "1":
            if liczba_fabuły == 2:
                input("dlaczego mnie zatakowałeś? bolało mnie to")
                wybor = input("1.uderzyłem cie, bo mi kazałaś\n2.przepraszam\n3.pozwól Tomkowi powiedzieć\n4.powiedz w prost że Elenor jest w grze\n")
                if wybor == "1":
                    input("Gracz: uderzyłem cie, bo mi kazałaś")
                    input("Elenor: aha, czyli…… to moja wina że mnie uderzyłeś? to chyba nie jest w porządku")
                    input("Tomek(myśli): dlaczego to powiedziała? przecież to nie prawda")
                    liczba_fabuły = 5
                elif wybor == "2":
                    input("Gracz: przepraszam")
                    input("Elenor: przeprosiny nic nie zmienią. to co zrobiłeś było złe")
                    input("Tomek(myśli): wiem……, ale jak to nic nie powiedziałem?")
                    liczba_fabuły = 3
                elif wybor == "3":
                    input("Tomek: coś mną sterowało. nie wiem co, ale to nie była moja wina")
                    input("Elenor: czyli to kogoś innego wina? ta napewno nie twoja")
                    input("Elenor: przeprosiny nic nie zmienią. to co zrobiłeś było złe")
                    input("Gracz: przepraszam")
                    input("Elenor: przeprosiny nic nie zmienią. to co zrobiłeś było złe")
                    input("wiem……, ale na serio byłem kontrolowany")
                    input("mówisz to na serio? nie mogę tego zaprzeczyć, ale to twoje ciało, a nie kogoś(mówi jakby powiętpywała samiej sobie)")
                    liczba_fabuły = 6
                elif wybor == "4":
                    input("Gracz: Elenor jesteś w grze i to wszystko jest zmyślone, a ty nie jesteś prawdziwa")
                    input("Elenor: co? to znaczy że to prawda? nie to nie możliwe. ja muszę być prawdziwa. tak?")
                    input("Tomek(myśli): co? jak to możliwe? ja nie istnieje? a co z Elenor?")
                    input("Elenor: nie mogę w to uwierzyć. muszę się stąd wydostać")
                    input("Gracz: Elenor jest to nie możliwe, bo jesteś częścią gry.")
                    input("niestety")
                    liczba_fabuły = 4
            else:
                print("jesteś przy ścianie i masz opcje")
                wybor = input("1.nasłuchuj\n2.idź do wyjścia\n3.poczekaj\n")
                if wybor == "1":
                    print("słyszysz dwóch strażników którzy rozmawiają o nowych rządach manreda i na to narzekają")
                    wybor = input("1.idź do wyjścia\n2.poczekaj\n")
                    if wybor == "1":
                        input("idziesz do wyjścia")
                        input("strażnik: hej ty! gdzie idziesz?")
                        input("biegniesz do wyjścia")
                        input("ale są za szybcy")
                        self.walka2()
    def walka1(self):
        r = 0
        while not pos3.oszczędzony():
            if r == 0:
                print("do na starcie nauczmy cię walczyć wręcz.\npo prostu mnie walnij.")
                while not r == 1:
                    wybor = input("1.zaatakuj\n2.czyn\n")
                    if wybor == "1":
                        jaka_cześć = 0
                        while not jaka_cześć in pos3.części_ciała:
                            jaka_cześć = input("napisz jaką część ciała chcesz zaatakować: ")
                        pos1.zaatakuj(pos3,jaka_cześć)
                        input("Elenor: Udało ci... ej, czekaj. Co? Dlaczego mnie? Przecież znamy się od urodzenia... No, nieważne — udało ci się, więc\ndobrze.")
                        input("Tomek(myśli): Dlaczego ją uderzyłem...? Co jest ze mną nie tak?")
                        pos3.relacje["Tomek"]["atak"] += 1
                        r += 1
                    elif wybor == "2":
                        print("Elenor:dziękuję że nie chcesz mnie uderzyć tylko porozmawiać, ale w tych czasach niestety trzeba")
                        pos3.oszczędzanie(pos3.relacje["Tomek"]["zaufanie"] - pos3.relacje["Tomek"]["atak"])
                        pos3.synchronizacja(5)
                        while not r == 1:
                            wybor = input("1.zaatakuj\n")
                            if wybor == "1":
                                jaka_cześć = 0
                                while not jaka_cześć in pos3.części_ciała:
                                    jaka_cześć = input("napisz jaką część ciała chcesz zaatakować: ")
                                pos1.zaatakuj(pos3,jaka_cześć)
                                input("Elernor: udało ci się")
                                r += 1
            elif r == 1:
                input("Elenor: no dobrze teraz naucze cię oszczędzać")
                if not pos3.oszczędzenie == 0:
                    input("Tomek: przecież umiem")
                    input("Elenor: no tak to już nie musimy")
                    pos3.oszczędzanie(100)
                else:
                    input("Tomek: dobra")
                    input("Tomek(myśli): ale na pradę. dlaczego ją uderzyłem? i to tak odrazu?")
                    input("Elenor: dobrze to teraz oszczędź mnie")
                    wybor = input("1.uderz\n2.czyn\n")
                    if wybor == "1":
                        print("Elenor: jej dlaczego znowu mnie uderzyłeś?")
                        input("Tomek(myśli): dlaczego to zrobiłem? i ta tak odrazu?")
                        input("Elenor: dobra już uciekam. pa(mówi to z żalem i nienawiścią).")
                        pos3.relacje["Tomek"]["atak"] += 1
                        break
                    elif wybor == "2":
                        print("Elenor: brawo że mnie oszczędziłeś")
                        pos3.oszczędzanie(100)
                        pos3.synchronizacja(5)
        pos3.oszczędzenie = 0
    def samouczek(self):
        q = 0
        input("Elenor: o już jesteś")
        input("Tomek: tak jestem. Jak chcesz mi pomóc?")
        input("Elenor: pokaże ci jak waczyć z wieloma wrogami, czyli walkę wrecz lub oszczędzenie")
        while True:
            q = input("Elenor: gotowy?\n1.tak\n2.nie\n")
            if q == "1":
                print("Elenor: dobrze")
                self.walka1()
                break
            elif q == "2":
                print("Elenor: jak to nie jesteś gotowy? boisz się(mówi to z troską).\n, ale musimy niestety")
                pos3.oszczędzanie(pos3.relacje['Tomek']["zaufanie"] - pos3.relacje["Tomek"]["atak"])
                self.walka1()
                break
    def menu(self):
        input("do Tomka Kowalskiego")
        input("hej Tomek przyjdziesz do mojej wioski, bo w tych czasach jest trochę trudno.")
        input("wiele się dzieje, ale wiem że to nie wasza wina")
        input("i chcę ci pomóc w tych trudnych czasach.")
        input("z umiłowaniem że to przeczytałeś:\nElenor\n")
        
        while True:
            self.men = input("1.sprawdź fabułę\n""2.wczytaj\n""3.rozpocznij gre\n")
            if self.men == "1":
                print("Fabularna tajemnica! Nie dostaniesz spoilerów tak łatwo 😉")
            elif self.men == "2":
                wcz = input("jak nazywa się zapis?")
                we = wczytaj_gre(wcz)
                if we is None:
                    continue
                global pos1, pos2, pos3, pos4, pos5, pos6, liczba_fabuły
                pos1.wczytaj(we["pos1"]["imie"],we["pos1"]["głód"],we["pos1"]["mgłód"],we["pos1"]["napojenie"],we["pos1"]["mnapojenie"],we["pos1"]["istota"],we["pos1"]["głowa"],we["pos1"]["klatka"],we["pos1"]["lręka"],we["pos1"]["pręka"],we["pos1"]["brzuch"],we["pos1"]["lrzebro"],we["pos1"]["przebro"],we["pos1"]["lnoga"],we["pos1"]["pnoga"],we["pos1"]["artefakty"],we["pos1"]["za_atak"],we["pos1"]["za_obrona"],we["pos1"]["atak"],we["pos1"]["obrona"],we["pos1"]["zbroja"],we["pos1"]["broń"],we["pos1"]["umiejętności"],we["pos1"]["ciało"],we["pos1"]["nczęści_ciała"],we["pos1"]["części_ciała"],we["pos1"]["ogłuszony"],we["pos1"]["czas_ogłuszenia"],we["pos1"]["chce"],we["pos1"]["musi"],we["pos1"]["tury"],we["pos1"]["drużyna"],we["pos1"]["wrogowie"],we["pos1"]["ekwipunek"],we["pos1"]["oszczędzenie"],we["pos1"]["relacje"],we["pos1"]["wochuk_uses"],we["pos1"]["cozwoj_uses"])
                pos2.wczytaj(we["pos2"]["imie"],we["pos2"]["głód"],we["pos2"]["mgłód"],we["pos2"]["napojenie"],we["pos2"]["mnapojenie"],we["pos2"]["istota"],we["pos2"]["głowa"],we["pos2"]["klatka"],we["pos2"]["lręka"],we["pos2"]["pręka"],we["pos2"]["brzuch"],we["pos2"]["lrzebro"],we["pos2"]["przebro"],we["pos2"]["lnoga"],we["pos2"]["pnoga"],we["pos2"]["artefakty"],we["pos2"]["za_atak"],we["pos2"]["za_obrona"],we["pos2"]["atak"],we["pos2"]["obrona"],we["pos2"]["zbroja"],we["pos2"]["broń"],we["pos2"]["umiejętności"],we["pos2"]["ciało"],we["pos2"]["nczęści_ciała"],we["pos2"]["części_ciała"],we["pos2"]["ogłuszony"],we["pos2"]["czas_ogłuszenia"],we["pos2"]["chce"],we["pos2"]["musi"],we["pos2"]["tury"],we["pos2"]["drużyna"],we["pos2"]["wrogowie"],we["pos2"]["ekwipunek"],we["pos2"]["oszczędzenie"],we["pos2"]["relacje"],we["pos2"]["wochuk_uses"],we["pos2"]["cozwoj_uses"])
                pos3.wczytaj(we["pos3"]["imie"],we["pos3"]["głód"],we["pos3"]["mgłód"],we["pos3"]["napojenie"],we["pos3"]["mnapojenie"],we["pos3"]["istota"],we["pos3"]["głowa"],we["pos3"]["klatka"],we["pos3"]["lręka"],we["pos3"]["pręka"],we["pos3"]["brzuch"],we["pos3"]["lrzebro"],we["pos3"]["przebro"],we["pos3"]["lnoga"],we["pos3"]["pnoga"],we["pos3"]["artefakty"],we["pos3"]["za_atak"],we["pos3"]["za_obrona"],we["pos3"]["atak"],we["pos3"]["obrona"],we["pos3"]["zbroja"],we["pos3"]["broń"],we["pos3"]["umiejętności"],we["pos3"]["ciało"],we["pos3"]["nczęści_ciała"],we["pos3"]["części_ciała"],we["pos3"]["ogłuszony"],we["pos3"]["czas_ogłuszenia"],we["pos3"]["chce"],we["pos3"]["musi"],we["pos3"]["tury"],we["pos3"]["drużyna"],we["pos3"]["wrogowie"],we["pos3"]["ekwipunek"],we["pos3"]["oszczędzenie"],we["pos3"]["relacje"],we["pos3"]["wochuk_uses"],we["pos3"]["cozwoj_uses"])
                pos4.wczytaj(we["pos4"]["imie"],we["pos4"]["głód"],we["pos4"]["mgłód"],we["pos4"]["napojenie"],we["pos4"]["mnapojenie"],we["pos4"]["istota"],we["pos4"]["głowa"],we["pos4"]["klatka"],we["pos4"]["lręka"],we["pos4"]["pręka"],we["pos4"]["brzuch"],we["pos4"]["lrzebro"],we["pos4"]["przebro"],we["pos4"]["lnoga"],we["pos4"]["pnoga"],we["pos4"]["artefakty"],we["pos4"]["za_atak"],we["pos4"]["za_obrona"],we["pos4"]["atak"],we["pos4"]["obrona"],we["pos4"]["zbroja"],we["pos4"]["broń"],we["pos4"]["umiejętności"],we["pos4"]["ciało"],we["pos4"]["nczęści_ciała"],we["pos4"]["części_ciała"],we["pos4"]["ogłuszony"],we["pos4"]["czas_ogłuszenia"],we["pos4"]["chce"],we["pos4"]["musi"],we["pos4"]["tury"],we["pos4"]["drużyna"],we["pos4"]["wrogowie"],we["pos4"]["ekwipunek"],we["pos4"]["oszczędzenie"],we["pos4"]["relacje"],we["pos4"]["wochuk_uses"],we["pos4"]["cozwoj_uses"])
                pos5.wczytaj(we["pos5"]["imie"],we["pos5"]["głód"],we["pos5"]["mgłód"],we["pos5"]["napojenie"],we["pos5"]["mnapojenie"],we["pos5"]["istota"],we["pos5"]["głowa"],we["pos5"]["klatka"],we["pos5"]["lręka"],we["pos5"]["pręka"],we["pos5"]["brzuch"],we["pos5"]["lrzebro"],we["pos5"]["przebro"],we["pos5"]["lnoga"],we["pos5"]["pnoga"],we["pos5"]["artefakty"],we["pos5"]["za_atak"],we["pos5"]["za_obrona"],we["pos5"]["atak"],we["pos5"]["obrona"],we["pos5"]["zbroja"],we["pos5"]["broń"],we["pos5"]["umiejętności"],we["pos5"]["ciało"],we["pos5"]["nczęści_ciała"],we["pos5"]["części_ciała"],we["pos5"]["ogłuszony"],we["pos5"]["czas_ogłuszenia"],we["pos5"]["chce"],we["pos5"]["musi"],we["pos5"]["tury"],we["pos5"]["drużyna"],we["pos5"]["wrogowie"],we["pos5"]["ekwipunek"],we["pos5"]["oszczędzenie"],we["pos5"]["relacje"],we["pos5"]["wochuk_uses"],we["pos5"]["cozwoj_uses"])
                pos6.wczytaj(we["pos6"]["imie"],we["pos6"]["głód"],we["pos6"]["mgłód"],we["pos6"]["napojenie"],we["pos6"]["mnapojenie"],we["pos6"]["istota"],we["pos6"]["głowa"],we["pos6"]["klatka"],we["pos6"]["lręka"],we["pos6"]["pręka"],we["pos6"]["brzuch"],we["pos6"]["lrzebro"],we["pos6"]["przebro"],we["pos6"]["lnoga"],we["pos6"]["pnoga"],we["pos6"]["artefakty"],we["pos6"]["za_atak"],we["pos6"]["za_obrona"],we["pos6"]["atak"],we["pos6"]["obrona"],we["pos6"]["zbroja"],we["pos6"]["broń"],we["pos6"]["umiejętności"],we["pos6"]["ciało"],we["pos6"]["nczęści_ciała"],we["pos6"]["części_ciała"],we["pos6"]["ogłuszony"],we["pos6"]["czas_ogłuszenia"],we["pos6"]["chce"],we["pos6"]["musi"],we["pos6"]["tury"],we["pos6"]["drużyna"],we["pos6"]["wrogowie"],we["pos6"]["ekwipunek"],we["pos6"]["oszczędzenie"],we["pos6"]["relacje"],we["pos6"]["wochuk_uses"],we["pos6"]["cozwoj_uses"])
                liczba_fabuły = we["liczba_fabuły"]
                break
            elif self.men == "3":
                self.samouczek()
                break
gra = Gra()
gra.menu()
if not gra.men == "2":
    if pos3.relacje["Tomek"]["atak"] == 0:
        liczba_fabuły = 1
    elif pos3.relacje["Tomek"]["atak"] == 1:
        liczba_fabuły = 2
    elif pos3.relacje["Tomek"]["atak"] >= 2:
        liczba_fabuły = 3
    zapis = {"pos1":pos1.__dict__,"pos2":pos2.__dict__,"pos3":pos3.__dict__,"pos4":pos4.__dict__,"pos5":pos5.__dict__,"pos6":pos6.__dict__,"liczba_fabuły": liczba_fabuły}
    save = input("jak nazwać zapis? (domyślnie 'save') ")
    zapisz_gre(zapis, save)
else:
    pass
if liczba_fabuły <= 3:
    gra.przygoda1()
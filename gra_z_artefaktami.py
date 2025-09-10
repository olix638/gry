from random import *
import json
def zapisz_gre(stan_gry, plik):
    with open(f"{plik}.json", "w") as f:
        json.dump(stan_gry, f)
    print("Gra zapisana!")
def wczytaj_gre(plik):
    try:
        with open(f"{plik}.json", "r") as f:
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
                                "|     |              \033[0mTomek    \033[0mElenor \033[38;5;240m\033[38;5;240m        |\n"
                                "|     /               \033[0m||       -||-\033[38;5;240m            |\n"
                                "|                               \033[0m\033[38;5;240m               |\n"
                                "/  \033[48;5;22m \\  \033[0m \033[38;5;240m                                      |     \\\n"
                                "|     |              \033[0mTomek      \033[0mElenor \033[38;5;240m       |\n"
                                "|     /               \033[0m||       -||-\033[38;5;240m           |\n"
                                "|                               \033[0m\033[38;5;240m              |\n"
                                "|                          /                  |\033[0m\n"
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
                                "\033[38;5;240m###############################################\033[0m"),}
zbroje = {"czarno_zbroja": dodanie_stat("czarno zbroja", 20, 10,0,randint(100, 150)), "brak_zbroi": dodanie_stat("brak zbroi", 0, 0,0,0),"jasno_zbroja": dodanie_stat("jasno zbroja", 20, 0,0,randint(100, 120)), "łuska_smoka": dodanie_stat("łuska smoka", 500, 500,0,500),"metalowa_zbroja":dodanie_stat("metalowa zbroja",500,0,0,100)}
bronie = {"brak_broni": dodanie_stat("brak broni", 0, 0,0,0), "łuk": dodanie_stat("łuk",0,50,0,randint(50, 100)),"topur": dodanie_stat("topur", 0, 500,3,500)}
patyki = {"cięki_patyk":dodanie_stat("cięki patyk", 0, 10, 0, randint(1, 15))}
class Postać:
    def __init__(self, istota, imie, głowa, klatka, lręka, pręka, brzuch, lrzebro, przebro, lnoga, pnoga, napojenie,mnapojenie, głód, mgłód, atak, obrona, zbroja, bronie,chce_zatakować,musi):
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
        self.bronie = bronie
        self.umiejętności = []
        self.ciało = głowa + klatka + lręka + pręka + brzuch + lrzebro + przebro + lnoga + pnoga
        self.nczęści_ciała = [self.głowa, self.klatka, self.lręka, self.pręka, self.brzuch, self.lrzebro, self.przebro,self.lnoga, self.pnoga]
        self.części_ciała = ["głowa", "klatka", "lręka", "pręka", "brzuch", "lrzebro", "przebro", "lnoga", "pnoga"]
        self.ogłuszony = False
        self.chce = chce_zatakować
        self.musi = musi
        self.drużyna = []
        self.wrogowie = []
        self.ekwipunek = {"ciękie patyki": 0,"kamienie": 0,"kawałki metalu": 0,"siekiera":0}
        self.oszczędzenie = 0
        self.dodatkowe_obrarzenia = 0
        self.relacje = {}
        # Do obsługi działania artefaktów
        self.wochuk_uses = {}  # przeciwnik: ile razy użyto
        self.cozwoj_uses = 0
    def sprawdź_ekwipunek(self):
        print(f"ekwipunek postaci: {self.imie}")
        for przedmiot, ilość in self.ekwipunek.items():
            if ilość > 0:
                print(f"{przedmiot}: {ilość}")


    def zadaj_obrażenia(self, jaka_część, ile):
        setattr(self, jaka_część, getattr(self, jaka_część) - ile)

    def dodaj_relacje(self, postac, staty_relacji):
        if postac in self.relacje:
            self.relacje[postac] += staty_relacji
        else:
            self.relacje[postac] = staty_relacji
    
    def dodaj_wroga(self, wróg):
        self.wrogowie.append(wróg)
    
    def oszczędzanie(self, o_ile):
        self.oszczędzenie += o_ile
    
    def oszczędzony(self):
        return self.oszczędzenie > 100
    
    def synchronizacja(self, protokuł):
        if protokuł == 4:
            self.ciało = sum(self.nczęści_ciała)
        elif protokuł == 5:
            self.głód = max(0, min(self.głód, self.mgłód))
            self.napojenie = max(0, min(self.napojenie, self.mnapojenie))
            self.oszczędzenie1 = max(0,min(self.oszczędzenie,100))
        elif self.istota == "goblin":
            if protokuł == 1:
                self.obrona = self.atak
            elif protokuł == 2:
                self.atak = self.obrona
            elif protokuł == 3:
                self.obrona = self.za_obrona
                self.atak = self.za_atak
                if self.zbroja != zbroje["łuska_smoka"]:
                    if self.zbroja == zbroje["brak_zbroi"]:
                        pass
                    else:
                        print("Nie da się dać na goblina oprócz łuski smoka")
                else:
                    self.obrona += self.zbroja.obrona
                    self.atak += self.zbroja.atak
                if self.bronie in bronie.values() or patyki.values():
                    self.atak += self.bronie.atak
        else:
            if protokuł == 3:
                self.obrona = self.za_obrona
                self.atak = self.za_atak
                if self.zbroja != zbroje["łuska_smoka"]:
                    self.obrona += self.zbroja.obrona
                    self.atak += self.zbroja.atak
                else:
                    print("Chcesz dać komuś innemu niż goblinowi łuskę smoka. Co jest z tobą nie tak?")
                if self.bronie in bronie.values() or patyki.values():
                    if self.bronie == bronie["łuk"] and self.istota == "elf":
                        self.atak += self.bronie.atak + 20
                    else:
                        self.atak += self.bronie.atak
    
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
    
    def zaatakuj(self, wrog, jaka_czesc):
        if self.chce or self.musi:
            if wrog in self.drużyna:
                print("chcesz zatakować swojego? co jest z tabą nie tak")
                return
            if not hasattr(wrog, jaka_czesc):
                print(f"nie ma części ciała: {jaka_czesc}")
                return
            obrazenia = max(0, randint(self.atak - 20, self.atak) - wrog.obrona)
            aktualne_hp = getattr(wrog, jaka_czesc)
            nowe_hp = max(0, aktualne_hp - obrazenia)
            setattr(wrog, jaka_czesc, nowe_hp)
            rzeczywiste_obrazenia = aktualne_hp - nowe_hp
            wrog.ciało = max(0, wrog.ciało - rzeczywiste_obrazenia)
            print(f"{wrog.imie} dostał {rzeczywiste_obrazenia} obrażeń w {jaka_czesc}!")
            print(f"{wrog.imie} ma {nowe_hp} HP w {jaka_czesc}")
            if not wrog.bronie.wytrzymałość == 0:
                self.bronie.wytrzymałość = max(0,wrog.bronie.wytrzymałość - 1)
        else:
            if not self.chce:
                print("nie chcę atakować")
    
    def zyje(self):
        return self.ciało > 0
    
    def dodaj_artefakt(self, nazwa, wymuszony_slot):
            self.artefakty[wymuszony_slot] = nazwa

    def ma_artefakt(self, nazwa):
        return nazwa in self.artefakty.values()
    
    def użyj_wochuk(self, przeciwnik):
        if "wochuk" not in self.artefakty:
            return f"{self.imie} nie posiada artefaktu Wochuk."
        if przeciwnik not in self.wochuk_uses:
            self.wochuk_uses[przeciwnik] = 0
        użycia = self.wochuk_uses[przeciwnik]
        szansa = 0.5 - (użycia * 0.1)
        self.wochuk_uses[przeciwnik] += 1
        if random() < szansa:
            przeciwnik.ogłuszony = True
            return f"{przeciwnik.imie} został ogłuszony przez Wochuka!"
        else:
            return f"{przeciwnik.imie} oparł się działaniu Wochuka."
    
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
pos1 = Postać("człowiek", "Tomek", 200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175, 175, 100, 100, 100, 100, 10, 20,zbroje["brak_zbroi"], patyki['cięki_patyk'],True,False)
pos2 = Postać("goblin", "Buzg", 200000.0, 250000.0, 44800.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000, 175000, 200,300, 50, 100, 0, 0, zbroje["brak_zbroi"], bronie["topur"],False,True)
pos3 = Postać("elf", "Elenor", 200000.0, 250000.0, 50000.0, 50000.0, 75000.0, 12500.0, 12500.0, 175000, 175000, 100,100, 10, 100, 5, 10, zbroje["brak_zbroi"], bronie["brak_broni"],False,False)
pos4 = Postać("elf", "Romeo", 200000.0, 250000.0, 50000.0, 50000.0, 75000.0, 12500.0, 12500.0, 50000, 100000, 100, 100,100, 100, 5, 10, zbroje["czarno_zbroja"], bronie["łuk"],True,False)
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
def walka1():
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
                    print("Elenor: jej dlacze znowu mnie uderzyłeś?")
                    input("Tomek(myśli): dlaczego to zrobiłem? i ta tak odrazu?")
                    input("Elenor: dobra już uciekam. pa(mówi to z żalem i nienawiścią).")
                    pos3.relacje["Tomek"]["atak"] += 5
                    break
                elif wybor == "2":
                    print("Elenor: brawo że mnie oszczędziłeś")
                    pos3.oszczędzanie(100)
                    pos3.synchronizacja(5)
    pos3.oszczędzenie = 0
def samouczek():
    q = 0
    input("Elenor: o już jesteś")
    input("Tomek: tak jestem. Jak chcesz mi pomóc?")
    input("Elenor: pokaże ci jak waczyć z wieloma wrogami, czyli walkę wrecz lub oszczędzenie")
    while True:
        q = input("Elenor: gotowy?\n1.tak\n2.nie\n")
        if q == "1":
            print("Elenor: dobrze")
            walka1()
            break
        elif q == "2":
            print("Elenor: jak to nie jesteś gotowy? boisz się(mówi to z troską).\n, ale musimy niestety")
            pos3.oszczędzanie(pos3.relacje['Tomek']["zaufanie"] - pos3.relacje["Tomek"]["atak"])
            walka1()
            break
def menu():
    input("do Tomka Kowalskiego")
    input("hej Tomek przyjdziesz do mojej wioski, bo w tych czasach jest trochę trudno.")
    input("wiele się dzieje, ale wiem że to nie wasza wina")
    input("i chcę ci pomóc w tych trudnych czasach.")
    input("z umiłowaniem że to przeczytałeś:\nElenor\n")
    while True:
        men = input("1.sprawdź fabułę\n""2.wczytaj\n""3.rozpocznij gre\n")
        if men == "1":
            print("Fabularna tajemnica! Nie dostaniesz spoilerów tak łatwo 😉")
        elif men == "2":
            print("jeszcze nie ma wczytywania")
        elif men == "3":
            samouczek()
            break
print(mapa["miejsce treningowe3"])
if pos3.relacje['Tomek']["atak"] == 0:
    liczba_fabuły = 1
elif pos3.relacje['Tomek']["atak"] == 1:
    liczba_fabuły = 2
elif pos3.relacje['Tomek']["atak"] >= 5:
    liczba_fabuły = 3
zapis = {"pos1":{"imie": pos1.imie, 
                 "głód": pos1.głód, 
                 "mgłód": pos1.mgłód, 
                 "napojenie": pos1.napojenie, 
                 "mnapojenie": pos1.mnapojenie, 
                 "ciało": pos1.ciało, "atak": pos1.atak, 
                 "obrona": pos1.obrona, 
                 "zbroja": pos1.zbroja.nazwa, 
                 "broń": pos1.bronie.nazwa, 
                 "artefakty": pos1.artefakty, 
                 "relacje": pos1.relacje, 
                 "ekwipunek": pos1.ekwipunek},
        "pos2":{"imie": pos2.imie, 
                "głód": pos2.głód, 
                "mgłód": pos2.mgłód, 
                "napojenie": pos2.napojenie, 
                "mnapojenie": pos2.mnapojenie, 
                "ciało": pos2.ciało, 
                "atak": pos2.atak, 
                "obrona": pos2.obrona, 
                "zbroja": pos2.zbroja.nazwa,
                "broń": pos2.bronie.nazwa, 
                "artefakty": pos2.artefakty, 
                "relacje": pos2.relacje, 
                "ekwipunek": pos2.ekwipunek},
        "pos3":{"imie": pos3.imie, 
                "głód": pos3.głód, 
                "mgłód": pos3.mgłód, 
                "napojenie": pos3.napojenie, 
                "mnapojenie": pos3.mnapojenie, "ciało": 
                pos3.ciało, "atak": pos3.atak, 
                "obrona": pos3.obrona, 
                "zbroja": pos3.zbroja.nazwa, 
                "broń": pos3.bronie.nazwa, 
                "artefakty": pos3.artefakty, 
                "relacje": pos3.relacje, 
                "ekwipunek": pos3.ekwipunek},
        "pos4":{"imie": pos4.imie, 
                "głód": pos4.głód, 
                "mgłód": pos4.mgłód, 
                "napojenie": pos4.napojenie, 
                "mnapojenie": pos4.mnapojenie, 
                "ciało": pos4.ciało, 
                "atak": pos4.atak, 
                "obrona": pos4.obrona, 
                "zbroja": pos4.zbroja.nazwa, 
                "broń": pos4.bronie.nazwa, 
                "artefakty": pos4.artefakty, 
                "relacje": pos4.relacje, 
                "ekwipunek": pos4.ekwipunek},
                "liczba_fabuły": liczba_fabuły}
zapisz_gre(zapis, "zapis")
def przygoda1():
    global liczba_fabuły
    if liczba_fabuły == 1:
        print(mapa["miejsce treningowe2"])
    elif liczba_fabuły == 2:
        print(mapa["miejsce treningowe1"])
    elif liczba_fabuły == 3:
        print(mapa["miejsce treningowe3"])
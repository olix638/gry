from random import *
import json
import os
import pygame
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
    "czarno_zbroja": ("czarno zbroja", 20, 10, 0, (100, 150)),
    "brak_zbroi": ("brak zbroi", 0, 0, 0, (0, 0)),
    "jasno_zbroja": ("jasno zbroja", 20, 0, 0, (100, 120)),
    "łuska_smoka": ("łuska smoka", 500, 500, 0, (500, 500)),
    "sdz_metalowa_zbroja": ("sdz metalowa zbroja", 50, 0, 0, (10, 50)),
    "metalowa_zbroja": ("metalowa zbroja", 100, 0, 0, (100, 150)),
    "zbroja z błota i liści": ("zbroja z błota i liści",5,0,0,(10,20))
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
                    if self.zbroja.nazwa == "brak zbroi":
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
                    obrazenia = max(0, randint(int(self.atak - (self.atak*0.1)), int(self.atak)) - wrog.obrona)
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
                obrazenia = max(0, randint(int(self.atak - (self.atak * 0.1)), int(self.atak)) - wrog.obrona)
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
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
    10.0, 20.0,
    daj_zbroje("zbroja z błota i liści"),
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
    100.0, 100.0, 100.0, 100.0,
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
    100.0, 100.0, 100.0, 100.0,
    5.0, 60.0,
    daj_zbroje("metalowa_zbroja"),
    daj_bron("włócznia"),
    False, True
)
pos6 = Postać(
    "elf", "Rokil",
    200.0, 250.0, 50.0, 50.0, 75.0, 12.5, 12.5, 175.0, 175.0,
    100.0, 100.0, 100.0, 100.0,
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
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
x = 100
y = 100
speed = 3  # pixel po pixelu
stamina = 100
player = pygame.image.load("gry/artefakty_pygame/Tomek.png").convert_alpha()
player = pygame.transform.scale(player, (200, 200))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_s]:
        y += speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_q]:
        pygame.quit()
        exit()
    if keys[pygame.K_LSHIFT] and not stamina <= 0:
        speed = 8
        stamina -= 1
    elif not keys[pygame.K_LSHIFT] or stamina <= 0:
        speed = 3
        stamina += 0.1
    screen.fill((0, 255, 0))
    screen.blit(player, (x, y))
    pygame.display.update()
    clock.tick(60)
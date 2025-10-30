from random import randint

class Czołg:
    def __init__(self, nazwa, zdrowie, pancerz, celność, kaliber, ostrość_pocisku,
                 prędkość_pojazdu, prędkość_pocisku):
        self.nazwa = nazwa
        self.zdrowie = zdrowie
        self.pancerz = pancerz
        self.celność = celność              # 0–100 (im wyżej, tym lepiej)
        self.siła_ognia = kaliber * ostrość_pocisku
        self.prędkość_pojazdu = prędkość_pojazdu    # im szybciej cel, tym trudniej trafić
        self.prędkość_pocisku = prędkość_pocisku    # im szybciej pocisk, tym łatwiej trafić

    def żyje(self):
        return self.zdrowie > 0

    def _policz_szansę(self, cel):
        # bazowo 50%, modyfikatory:
        # + celność * 0.4
        # + prędkość_pocisku * 0.2
        # - prędkość_pojazdu celu * 0.3
        sz = 50 + self.celność * 0.4 + self.prędkość_pocisku * 0.2 - cel.prędkość_pojazdu * 0.3
        # przytnij do 5–95% żeby zawsze była jakaś szansa
        return max(5, min(95, int(sz)))

    def atakuj(self, inny_czołg):
        szansa = self._policz_szansę(inny_czołg)
        rzut = randint(1,100)
        if rzut <= szansa:
            obrażenia = max(0, self.siła_ognia - inny_czołg.pancerz)
            inny_czołg.zdrowie -= obrażenia
            print(f"{self.nazwa} trafił {inny_czołg.nazwa} (szansa {szansa}%, rzut {rzut}) "
                  f"za {obrażenia} dmg. Zdrowie celu: {max(0, inny_czołg.zdrowie)}")
        else:
            print(f"{self.nazwa} chybił (szansa {szansa}%, rzut {rzut}).")

# --- Minimalna „gra” 1v1 ---
    # zrób dwa proste czołgi
p = Czołg("Gracz",610,100,60,20, 2.0,20,70)

e = Czołg("Wróg",200,5,30,120,1.5,90,0)

tura = 1
print("Pojedynek czołgów! Każdy oddaje jeden strzał na turę.\n")
while p.żyje() and e.żyje():
        print(f"\n--- Tura {tura} ---")
        # Gracz strzela
        p.atakuj(e)
        if not e.żyje():
            print("\nWróg zniszczony! Wygrywasz!")
            break
        # Wróg strzela
        e.atakuj(p)
        if not p.żyje():
            print("\nTwój czołg został zniszczony. Przegrana.")
            break
        tura += 1

from random import randint
import math
import os

# --- USTAWIENIA MAPY ---
W, H = 13, 11
LICZBA_PRZESZKOD = 18
OBSTACLE_RESIST = 50  # odporność # dla AP

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sign(x): return 0 if x == 0 else (1 if x > 0 else -1)
def w_bounds(x, y): return 0 <= x < W and 0 <= y < H

def losuj_przeszkody(ile, zajete):
    blokady = set()
    próby = 0
    while len(blokady) < ile and próby < 20000:
        próby += 1
        x, y = randint(0, W-1), randint(0, H-1)
        if (x, y) not in zajete:
            blokady.add((x, y))
    return blokady

def rysuj(p1, p2, blokady, komunikat=""):
    clear()
    board = [['.' for _ in range(W)] for __ in range(H)]
    for (bx, by) in blokady: board[by][bx] = '#'
    if w_bounds(p1.x, p1.y): board[p1.y][p1.x] = p1.symbol
    if w_bounds(p2.x, p2.y): board[p2.y][p2.x] = p2.symbol
    for y in range(H): print(''.join(board[y]))
    print()
    print(f"{p1.nazwa}({p1.symbol}): HP={p1.hp}, Ruchy={p1.ruchy}/{p1.ruchy_bazowe}, Ostatni ruch: {p1.ostatni_ruch}")
    print(f"{p2.nazwa}({p2.symbol}): HP={p2.hp}, Ruchy={p2.ruchy}/{p2.ruchy_bazowe}, Ostatni ruch: {p2.ostatni_ruch}")
    if komunikat: print("\n" + komunikat)

class Czolag:
    def __init__(self, nazwa, hp, pancerz, celnosc, kaliber, ostrosc,
                 v_poj, v_poc, x=0, y=0, symbol='P', ruchy_bazowe=2):
        # statystyki
        self.nazwa = nazwa
        self.hp = hp
        self.pancerz = pancerz
        self.celnosc = celnosc
        self.kaliber = kaliber
        self.ostrosc = ostrosc
        self.sila_ognia = kaliber * ostrosc
        self.v_poj = v_poj
        self.v_poc = v_poc
        # pozycja
        self.x = x
        self.y = y
        self.symbol = symbol
        # ruch
        self.ruchy_bazowe = ruchy_bazowe
        self.ruchy = ruchy_bazowe
        self.ostatni_ruch = "brak"
        # stan tury
        self.strzal_bonus_uzyty = False  # (nie używamy już bonusu do puli, zostawione na przyszłość)

    # --- podstawy ---
    def zyje(self): return self.hp > 0
    def dystans_do(self, ix, iy): return math.hypot(self.x - ix, self.y - iy)

    # --- ruch ---
    def resetuj_ruchy(self):
        self.ruchy = self.ruchy_bazowe
        self.ostatni_ruch = "brak"
        self.strzal_bonus_uzyty = False

    def zuzyj_ruch(self):
        if self.ruchy > 0:
            self.ruchy -= 1
            return True
        return False

    def moze_wejsc(self, nx, ny, blokady, pos_drugiego):
        return w_bounds(nx, ny) and (nx, ny) not in blokady and (nx, ny) != pos_drugiego

    def _wykonaj_ruch_na(self, nx, ny, blokady, pos_drugiego, opis):
        if self.moze_wejsc(nx, ny, blokady, pos_drugiego):
            self.x, self.y = nx, ny
            self.ostatni_ruch = opis
            return True
        else:
            print(f"{self.nazwa}: ruch zablokowany.")
            return False

    def rusz(self, kierunek, blokady, pos_drugiego):
        """Normalny ruch: kosztuje 1 punkt 'ruchy'."""
        if self.ruchy <= 0:
            print(f"{self.nazwa}: brak punktów ruchu!")
            return False
        nx, ny = self.x, self.y
        if kierunek in ('w','i'):
            ny -= 1; opis = "północ"
        elif kierunek in ('s','k'):
            ny += 1; opis = "południe"
        elif kierunek in ('a','j'):
            nx -= 1; opis = "zachód"
        elif kierunek in ('d','l'):
            nx += 1; opis = "wschód"
        else:
            return False
        if self._wykonaj_ruch_na(nx, ny, blokady, pos_drugiego, opis):
            self.zuzyj_ruch()
            print(f"{self.nazwa} ruszył się na {opis}.")
            return True
        return False

    def krok_po_strzale(self, kierunek, blokady, pos_drugiego):
        """Dokładnie JEDEN krok po strzale – bez kosztu 'ruchy'. (Jeśli brak/niepoprawny – przepada.)"""
        if not kierunek:
            return False
        nx, ny = self.x, self.y
        if kierunek in ('w','i'):
            ny -= 1; opis = "północ"
        elif kierunek in ('s','k'):
            ny += 1; opis = "południe"
        elif kierunek in ('a','j'):
            nx -= 1; opis = "zachód"
        elif kierunek in ('d','l'):
            nx += 1; opis = "wschód"
        else:
            return False
        ok = self._wykonaj_ruch_na(nx, ny, blokady, pos_drugiego, opis)
        if ok:
            print(f"{self.nazwa} (krok po strzale) ruszył się na {opis}.")
        return ok

    # --- walka ---
    def szansa_trafienia(self, target, dist):
        sz = 50 + self.celnosc * 0.4 + self.v_poc * 0.15 - target.v_poj * 0.25
        sz -= dist * 2
        return max(5, min(95, int(sz)))

    def policz_obrazenia(self, target, dist, dmg_factor=1.0):
        optimal = 3.0
        range_factor = 1.0 if dist <= optimal else max(0.3, 1.0 - (dist - optimal) * 0.15)
        return max(0, int(self.sila_ognia * range_factor * dmg_factor - target.pancerz))

    # WYCHYLENIA: jeśli # na N/E/S/W, próbujemy startów z narożników
    def _peek_origins(self, blokady):
        origins = [("TU", (self.x, self.y))]
        if (self.x, self.y-1) in blokady:   # N
            for p in [(self.x+1,self.y-1),(self.x-1,self.y-1)]:
                if w_bounds(*p) and p not in blokady: origins.append(("NE/NW", p))
        if (self.x+1, self.y) in blokady:   # E
            for p in [(self.x+1,self.y-1),(self.x+1,self.y+1)]:
                if w_bounds(*p) and p not in blokady: origins.append(("NE/SE", p))
        if (self.x, self.y+1) in blokady:   # S
            for p in [(self.x+1,self.y+1),(self.x-1,self.y+1)]:
                if w_bounds(*p) and p not in blokady: origins.append(("SE/SW", p))
        if (self.x-1, self.y) in blokady:   # W
            for p in [(self.x-1,self.y-1),(self.x-1,self.y+1)]:
                if w_bounds(*p) and p not in blokady: origins.append(("NW/SW", p))
        uniq, seen = [], set()
        for lab,pos in origins:
            if pos not in seen:
                uniq.append((lab,pos)); seen.add(pos)
        return uniq

    def _simulate_shot_from(self, ox, oy, target, blokady, typ, label):
        dx, dy = sign(target.x - ox), sign(target.y - oy)
        if dx == 0 and dy == 0: return False
        x, y = ox + dx, oy + dy
        while w_bounds(x,y):
            # trafienie
            if (x,y) == (target.x,target.y):
                dist = math.hypot(ox-x, oy-y)
                sz   = self.szansa_trafienia(target, dist)
                r    = randint(1,100)
                if r <= sz:
                    dmg = self.policz_obrazenia(target, dist)
                    target.hp -= dmg
                    print(f"{self.nazwa} TRAFIA {target.nazwa} ({label}) sz {sz}% → {dmg} dmg (HP {target.hp})")
                    return True
                else:
                    print(f"{self.nazwa} chybił ({label}) sz {sz}%, rzut {r}")
                    return False
            # przeszkoda
            if (x,y) in blokady:
                if typ == 'ap':
                    pen = self.sila_ognia * (0.8 + randint(0,40)/100.0)
                    if pen >= OBSTACLE_RESIST:
                        x += dx; y += dy; continue
                    else:
                        return False
                elif typ == 'he':
                    cx, cy = x + dx, y + dy
                    for ex in range(cx-1, cx+2):
                        for ey in range(cy-1, cy+2):
                            if (ex,ey) == (target.x,target.y):
                                distc = math.hypot(ox-ex, oy-ey)
                                dmg = self.policz_obrazenia(target, distc, dmg_factor=0.6)
                                if dmg > 0: target.hp -= dmg; return True
                    return False
                else:
                    return False
            x += dx; y += dy
        return False

    def strzel_w_cel(self, target, blokady, typ='ap'):
        origins = self._peek_origins(blokady)
        for lab,(ox,oy) in origins:
            if self._simulate_shot_from(ox,oy,target,blokady,typ,lab):
                return True
        print(f"{self.nazwa}: pudło.")
        return False

# --- GRA ---
if __name__ == "__main__":
    # PRZYKŁAD: pancernik wolniejszy (2), niszczyciel szybszy (3)
    p1 = Czolag("Pancernik (G1)", 610, 100, 60, 20, 2.0, 20, 70, 2, H//2, 'P', 3)
    p2 = Czolag("Niszczyciel (G2)", 200, 5, 30, 120, 1.5, 90, 90, W-3, H//2, 'E', 6)

    blokady = losuj_przeszkody(LICZBA_PRZESZKOD, {(p1.x,p1.y),(p2.x,p2.y)})

    tura_p1 = True
    komunikat = ""
    while p1.zyje() and p2.zyje():
        aktywny   = p1 if tura_p1 else p2
        przeciwnik= p2 if tura_p1 else p1

        aktywny.resetuj_ruchy()

        # pętla tury: możesz robić ruchy; strzał kończy turę po JEDNYM kroku
        tura_trwa = True
        while tura_trwa and aktywny.ruchy > 0 and p1.zyje() and p2.zyje():
            rysuj(p1, p2, blokady, komunikat)
            komunikat = ""
            print(f"Tura: {aktywny.nazwa}  |  Ruchy: {aktywny.ruchy}/{aktywny.ruchy_bazowe}")
            if aktywny is p1:
                print("w/a/s/d = ruch (koszt 1), f [ap|he] = STRZAŁ (po nim 1 krok i KONIEC tury), koniec = zakończ turę, q = wyjście")
            else:
                print("i/j/k/l = ruch (koszt 1), h [ap|he] = STRZAŁ (po nim 1 krok i KONIEC tury), koniec = zakończ turę, q = wyjście")

            wej = input("> ").strip().lower().split()
            if not wej: continue
            cmd = wej[0]

            if cmd == 'q':
                print("Koniec gry."); exit(0)

            if cmd == 'koniec':
                break

            # ruchy
            if aktywny is p1 and cmd in ('w','a','s','d'):
                aktywny.rusz(cmd, blokady, (przeciwnik.x,przeciwnik.y))
                continue
            if aktywny is p2 and cmd in ('i','j','k','l'):
                aktywny.rusz(cmd, blokady, (przeciwnik.x,przeciwnik.y))
                continue

            # STRZAŁ → JEDEN krok → KONIEC TURY
            if (aktywny is p1 and cmd == 'f') or (aktywny is p2 and cmd == 'h'):
                typ = 'ap'
                if len(wej) >= 2 and wej[1] in ('ap','he'): typ = wej[1]
                aktywny.strzel_w_cel(przeciwnik, blokady, typ=typ)

                # 1 krok po strzale (nie kosztuje 'ruchy'), jeśli gracz poda kierunek
                if aktywny is p1:
                    kier = input("Krok po strzale (w/a/s/d). Enter = pomiń: ").strip().lower()
                else:
                    kier = input("Krok po strzale (i/j/k/l). Enter = pomiń: ").strip().lower()
                aktywny.krok_po_strzale(kier, blokady, (przeciwnik.x,przeciwnik.y))

                # KONIEC TURY niezależnie od pozostałych punktów ruchu
                tura_trwa = False
                break

            komunikat = "Nieznana komenda."

        # zmiana tury
        tura_p1 = not tura_p1

        if not p1.zyje() or not p2.zyje(): break

    rysuj(p1, p2, blokady)
    print(f"\nZwycięzca: {'Gracz 1' if p1.zyje() else 'Gracz 2'}")

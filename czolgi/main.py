# 2-graczy hot-seat — auto-celowanie, AP/HE, blokady ruchu
# + WYCHYLENIA: jeśli jest blokada N/E/S/W przy strzelającym, symulujemy start z (tu) i dwóch narożników
from random import randint
import math
import os

# --- USTAWIENIA ---
W, H = 13, 11          # rozmiar planszy
LICZBA_PRZESZKOD = 18  # ile losowych blokad
OBSTACLE_RESIST = 50   # odporność blokady na przebicie AP

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sign(x):
    return 0 if x == 0 else (1 if x > 0 else -1)

def losuj_przeszkody(ile, zajete):
    blokady = set()
    proby = 0
    while len(blokady) < ile and proby < 20000:
        proby += 1
        x = randint(0, W-1)
        y = randint(0, H-1)
        if (x, y) in zajete:
            continue
        blokady.add((x, y))
    return blokady

def w_bounds(x, y): return 0 <= x < W and 0 <= y < H

def rysuj(p1, p2, blokady, komunikat=""):
    clear()
    board = [['.' for _ in range(W)] for __ in range(H)]
    for (bx, by) in blokady:
        board[by][bx] = '#'
    if w_bounds(p1.x, p1.y): board[p1.y][p1.x] = p1.symbol
    if w_bounds(p2.x, p2.y): board[p2.y][p2.x] = p2.symbol
    for y in range(H):
        print(''.join(board[y]))
    print()
    print("Strzał automatycznie celuje w przeciwnika. Typy: ap (przebija), he (eksplozja za blokadą).")
    print(f"{p1.nazwa}({p1.symbol}): HP={p1.hp}  Pos=({p1.x},{p1.y})")
    print(f"{p2.nazwa}({p2.symbol}): HP={p2.hp}  Pos=({p2.x},{p2.y})")
    if komunikat:
        print("\n" + komunikat)

class Czolag:
    def __init__(self, nazwa, hp, pancerz, celnosc, kaliber, ostrosc,
                 v_poj, v_poc, x=0, y=0, symbol='P'):
        self.nazwa = nazwa
        self.hp = hp
        self.pancerz = pancerz
        self.celnosc = celnosc
        self.kaliber = kaliber
        self.ostrosc = ostrosc
        self.sila_ognia = kaliber * ostrosc
        self.v_poj = v_poj
        self.v_poc = v_poc
        self.x = x
        self.y = y
        self.symbol = symbol

    def zyje(self): return self.hp > 0
    def dystans_do(self, ix, iy): return math.hypot(self.x - ix, self.y - iy)

    def moze_wejsc(self, nx, ny, blokady, pos_drugiego):
        return w_bounds(nx, ny) and (nx, ny) not in blokady and (nx, ny) != pos_drugiego

    def rusz(self, kierunek, blokady, pos_drugiego):
        nx, ny = self.x, self.y
        if kierunek == 'w': ny -= 1
        elif kierunek == 's': ny += 1
        elif kierunek == 'a': nx -= 1
        elif kierunek == 'd': nx += 1
        elif kierunek == 'i': ny -= 1
        elif kierunek == 'k': ny += 1
        elif kierunek == 'j': nx -= 1
        elif kierunek == 'l': nx += 1
        else: return
        if self.moze_wejsc(nx, ny, blokady, pos_drugiego):
            self.x, self.y = nx, ny

    def szansa_trafienia(self, target, dist):
        sz = 50 + self.celnosc * 0.4 + self.v_poc * 0.15 - target.v_poj * 0.25
        sz -= dist * 2
        return max(5, min(95, int(sz)))

    def policz_obrazenia(self, target, dist, dmg_factor=1.0):
        optimal = 3.0
        range_factor = 1.0 if dist <= optimal else max(0.3, 1.0 - (dist - optimal) * 0.15)
        return max(0, int(self.sila_ognia * range_factor * dmg_factor - target.pancerz))

    def _simulate_shot_from(self, ox, oy, target, blokady, typ, label):
        """Symuluje lot pocisku startującego z (ox,oy) w stronę targetu (auto-kierunek)."""
        dx = sign(target.x - ox)
        dy = sign(target.y - oy)
        if dx == 0 and dy == 0:
            print(f"{self.nazwa}: Cel na tej samej pozycji ({label}).")
            return False

        x, y = ox + dx, oy + dy
        while w_bounds(x, y):
            # trafienie w przeciwnika
            if (x, y) == (target.x, target.y):
                dist = math.hypot(ox - x, oy - y)
                sz = self.szansa_trafienia(target, dist)
                r = randint(1, 100)
                if r <= sz:
                    dmg = self.policz_obrazenia(target, dist)
                    target.hp -= dmg
                    print(f"{self.nazwa} TRAFIA {target.nazwa} ({label}) odl {dist:.2f}, sz {sz}% → {dmg} dmg. HP {target.nazwa}={max(0,target.hp)}")
                    return True
                else:
                    print(f"{self.nazwa} chybił ({label}) sz {sz}%, rzut {r}.")
                    return False

            # przeszkoda na torze
            if (x, y) in blokady:
                if typ == 'ap':
                    penetracja = self.sila_ognia * (0.8 + randint(0, 40) / 100.0)
                    if penetracja >= OBSTACLE_RESIST:
                        print(f"AP przebił # na ({x},{y}) ({label}), pen {penetracja:.1f} ≥ {OBSTACLE_RESIST}.")
                        x += dx; y += dy
                        continue
                    else:
                        print(f"AP zablokowany na ({x},{y}) ({label}), pen {penetracja:.1f} < {OBSTACLE_RESIST}.")
                        return False
                elif typ == 'he':
                    print(f"HE eksploduje przy # na ({x},{y}) ({label}).")
                    cx, cy = x + dx, y + dy
                    dmg_any = 0
                    for ex in range(cx-1, cx+2):
                        for ey in range(cy-1, cy+2):
                            if (ex, ey) == (target.x, target.y):
                                dist_center = math.hypot(ox - ex, oy - ey)
                                dmg = self.policz_obrazenia(target, dist_center, dmg_factor=0.6)
                                if dmg > 0:
                                    target.hp -= dmg
                                    dmg_any += dmg
                    if dmg_any > 0:
                        print(f"HE zraniło cel za # o {dmg_any} dmg ({label}). HP {target.nazwa}={max(0,target.hp)}")
                        return True
                    else:
                        print(f"HE nie dosięgło celu ({label}).")
                        return False
                else:
                    print("Nieznany typ amunicji.")
                    return False

            x += dx
            y += dy

        print(f"Pocisk opuścił planszę bez trafienia ({label}).")
        return False

    def _peek_origins(self, blokady):
        """
        Zwraca listę (label, (ox,oy)) pozycji startowych:
        - (Here, (x,y)) zawsze
        - jeśli # na N:  dodaj (NE) (x+1,y-1) i (NW) (x-1,y-1)
        - jeśli # na E:  dodaj (NE) (x+1,y-1) i (SE) (x+1,y+1)
        - jeśli # na S:  dodaj (SE) (x+1,y+1) i (SW) (x-1,y+1)
        - jeśli # na W:  dodaj (NW) (x-1,y-1) i (SW) (x-1,y+1)
        (tylko jeśli w granicach i nie są #)
        """
        origins = [("HERE", (self.x, self.y))]
        # N
        if (self.x, self.y-1) in blokady:
            for lab, (ox, oy) in [("NE", (self.x+1, self.y-1)), ("NW", (self.x-1, self.y-1))]:
                if w_bounds(ox, oy) and (ox, oy) not in blokady:
                    origins.append((lab, (ox, oy)))
        # E
        if (self.x+1, self.y) in blokady:
            for lab, (ox, oy) in [("NE", (self.x+1, self.y-1)), ("SE", (self.x+1, self.y+1))]:
                if w_bounds(ox, oy) and (ox, oy) not in blokady:
                    origins.append((lab, (ox, oy)))
        # S
        if (self.x, self.y+1) in blokady:
            for lab, (ox, oy) in [("SE", (self.x+1, self.y+1)), ("SW", (self.x-1, self.y+1))]:
                if w_bounds(ox, oy) and (ox, oy) not in blokady:
                    origins.append((lab, (ox, oy)))
        # W
        if (self.x-1, self.y) in blokady:
            for lab, (ox, oy) in [("NW", (self.x-1, self.y-1)), ("SW", (self.x-1, self.y+1))]:
                if w_bounds(ox, oy) and (ox, oy) not in blokady:
                    origins.append((lab, (ox, oy)))
        # usuń duplikaty zachowując kolejność
        seen = set()
        uniq = []
        for lab, pos in origins:
            if pos not in seen:
                uniq.append((lab, pos))
                seen.add(pos)
        return uniq

    def strzel_w_cel(self, target, blokady, typ='ap'):
        """
        Strzał bez wyboru kierunku — auto-cel w przeciwnika.
        Jeśli przy strzelającym jest # N/E/S/W, symulujemy wyjście z narożników (NE/NW, NE/SE, SE/SW, NW/SW).
        Próbujemy po kolei wszystkie pozycje startowe; jeśli któraś trafi — koniec akcji.
        """
        origins = self._peek_origins(blokady)
        for lab, (ox, oy) in origins:
            if (ox, oy) == (self.x, self.y):
                label = "TU"
            else:
                label = f"SYM {lab}"
            if self._simulate_shot_from(ox, oy, target, blokady, typ, label):
                return True
        # jeśli żadna symulacja nie trafiła:
        print(f"{self.nazwa}: żadna ścieżka (TU / narożniki) nie dała trafienia.")
        return False

# --- GRA ---
if __name__ == "__main__":
    p1 = Czolag("Gracz 1", hp=610, pancerz=100, celnosc=60, kaliber=20,  ostrosc=2.0,
                v_poj=20, v_poc=70, x=2,   y=H//2, symbol='P')
    p2 = Czolag("Gracz 2", hp=200, pancerz=5,   celnosc=30, kaliber=120, ostrosc=1.5,
                v_poj=90, v_poc=90, x=W-3, y=H//2, symbol='E')

    blokady = losuj_przeszkody(LICZBA_PRZESZKOD, {(p1.x, p1.y), (p2.x, p2.y)})

    tura_p1 = True
    komunikat = ""
    while p1.zyje() and p2.zyje():
        rysuj(p1, p2, blokady, komunikat)
        if tura_p1:
            print("\nTura: Gracz 1 [ruch: w/a/s/d, strzał: f [ap|he], wyjście: q]")
            wej = input("> ").strip().lower().split()
            if not wej:
                komunikat = "Brak komendy."
                continue
            cmd = wej[0]
            if cmd == 'q':
                print("Koniec gry.")
                break
            if cmd in ('w','a','s','d'):
                p1.rusz(cmd, blokady, (p2.x, p2.y))
                komunikat = "Gracz 1 ruszył się."
            elif cmd == 'f':
                typ = 'ap' if len(wej) < 2 else ('he' if wej[1] == 'he' else 'ap')
                p1.strzel_w_cel(p2, blokady, typ=typ)
                komunikat = f"Gracz 1 strzelił typ={typ}."
                tura_p1 = False
            else:
                komunikat = "Nieznana komenda Gracza 1."
        else:
            print("\nTura: Gracz 2 [ruch: i/j/k/l, strzał: h [ap|he], wyjście: q]")
            wej = input("> ").strip().lower().split()
            if not wej:
                komunikat = "Brak komendy."
                continue
            cmd = wej[0]
            if cmd == 'q':
                print("Koniec gry.")
                break
            if cmd in ('i','j','k','l'):
                p2.rusz(cmd, blokady, (p1.x, p1.y))
                komunikat = "Gracz 2 ruszył się."
            elif cmd == 'h':
                typ = 'ap' if len(wej) < 2 else ('he' if wej[1] == 'he' else 'ap')
                p2.strzel_w_cel(p1, blokady, typ=typ)
                komunikat = f"Gracz 2 strzelił typ={typ}."
                tura_p1 = True
            else:
                komunikat = "Nieznana komenda Gracza 2."

        # zwycięstwo?
        if not p2.zyje():
            rysuj(p1, p2, blokady)
            print("\nGracz 2 zniszczony! Wygrywa Gracz 1.")
            break
        if not p1.zyje():
            rysuj(p1, p2, blokady)
            print("\nGracz 1 zniszczony! Wygrywa Gracz 2.")
            break

    print("\nKONIEC BITWY.")

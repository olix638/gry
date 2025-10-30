# 2-graczy hot-seat — auto-celowanie, AP/HE, blokady ruchu i strzał "zza przeszkody" (peek)
from random import randint
import math
import os

# --- USTAWIENIA ---
W, H = 13, 11          # rozmiar planszy
LICZBA_PRZESZKOD = 18  # ile losowych blokad
OBSTACLE_RESIST = 50   # odporność blokady na przebicie AP

# Kary/bonusy dla "wychylenia" (peek)
PEEK_ACC_PENALTY = 12     # -12 punktów procentowych do trafienia
PEEK_DMG_FACTOR  = 0.85   # obrażenia x0.85

# --- POMOCNICZE ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sign(x):
    return 0 if x == 0 else (1 if x > 0 else -1)

def adjacent(ax, ay, bx, by):
    # sąsiad po królu (8 kierunków)
    return max(abs(ax - bx), abs(ay - by)) == 1

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

def rysuj(p1, p2, blokady, komunikat=""):
    clear()
    board = [['.' for _ in range(W)] for __ in range(H)]
    for (bx, by) in blokady:
        board[by][bx] = '#'
    if 0 <= p1.x < W and 0 <= p1.y < H:
        board[p1.y][p1.x] = p1.symbol
    if 0 <= p2.x < W and 0 <= p2.y < H:
        board[p2.y][p2.x] = p2.symbol
    for y in range(H):
        print(''.join(board[y]))
    print()
    print("Strzał automatycznie celuje w przeciwnika. Typy: ap (przebija), he (eksplozja za blokadą).")
    print(f"{p1.nazwa}({p1.symbol}): HP={p1.hp}  Pos=({p1.x},{p1.y})")
    print(f"{p2.nazwa}({p2.symbol}): HP={p2.hp}  Pos=({p2.x},{p2.y})")
    if komunikat:
        print("\n" + komunikat)

# --- LOGIKA CZOŁGU ---
class Czolag:
    def __init__(self, nazwa, hp, pancerz, celnosc, kaliber, ostrosc,
                 v_poj, v_poc, x=0, y=0, symbol='P'):
        self.nazwa = nazwa
        self.hp = hp
        self.pancerz = pancerz
        self.celnosc = celnosc     # 0-100
        self.kaliber = kaliber     # mm
        self.ostrosc = ostrosc
        self.sila_ognia = kaliber * ostrosc
        self.v_poj = v_poj
        self.v_poc = v_poc
        self.x = x
        self.y = y
        self.symbol = symbol

    def zyje(self):
        return self.hp > 0

    def dystans_do(self, inx, iny):
        return math.hypot(self.x - inx, self.y - iny)

    def moze_wejsc(self, nx, ny, blokady, pozycja_drugiego):
        if not (0 <= nx < W and 0 <= ny < H):
            return False
        if (nx, ny) in blokady:
            return False
        if (nx, ny) == pozycja_drugiego:
            return False
        return True

    def rusz(self, kierunek, blokady, pozycja_drugiego):
        nx, ny = self.x, self.y
        if kierunek == 'w': ny -= 1
        elif kierunek == 's': ny += 1
        elif kierunek == 'a': nx -= 1
        elif kierunek == 'd': nx += 1
        elif kierunek == 'i': ny -= 1
        elif kierunek == 'k': ny += 1
        elif kierunek == 'j': nx -= 1
        elif kierunek == 'l': nx += 1
        else:
            return
        if self.moze_wejsc(nx, ny, blokady, pozycja_drugiego):
            self.x, self.y = nx, ny

    def szansa_trafienia(self, target, dist):
        # bazowa + modyfikatory statystyk
        sz = 50 + self.celnosc * 0.4 + self.v_poc * 0.15 - target.v_poj * 0.25
        sz -= dist * 2  # kara za dystans
        return max(5, min(95, int(sz)))

    def policz_obrazenia(self, target, dist, dmg_factor=1.0):
        # spadek obrażeń z dystansem (poza zasięgiem optymalnym)
        optimal = 3.0
        if dist <= optimal:
            range_factor = 1.0
        else:
            range_factor = max(0.3, 1.0 - (dist - optimal) * 0.15)
        dmg = max(0, int(self.sila_ognia * range_factor * dmg_factor - target.pancerz))
        return dmg

    def strzel_w_cel(self, target, blokady, typ='ap'):
        """
        Auto-celowanie w przeciwnika. Pocisk idzie wektorowo (dx=sign, dy=sign).
        Mechanika 'peek': jeśli pierwsza napotkana przeszkoda # jest TUŻ OBOK strzelca,
        ignorujemy ją (tylko tę jedną) z karą do celności i obrażeń.
        Dalsze przeszkody: AP próbuje przebić, HE eksploduje (obszar za przeszkodą).
        """
        dx = sign(target.x - self.x)
        dy = sign(target.y - self.y)
        if dx == 0 and dy == 0:
            print(f"{self.nazwa}: Cel na tej samej pozycji — brak strzału.")
            return False

        x, y = self.x + dx, self.y + dy
        peek_used = False        # czy wykorzystano „wychylenie”
        extra_acc_penalty = 0    # kara do trafienia z peek
        extra_dmg_factor  = 1.0  # redukcja obrażeń z peek

        while 0 <= x < W and 0 <= y < H:
            # trafienie w cel (jeśli doszliśmy do jego pola)
            if (x, y) == (target.x, target.y):
                dist = self.dystans_do(x, y)
                sz = self.szansa_trafienia(target, dist) - extra_acc_penalty
                sz = max(5, min(95, sz))
                r = randint(1, 100)
                if r <= sz:
                    dmg = self.policz_obrazenia(target, dist, dmg_factor=extra_dmg_factor)
                    target.hp -= dmg
                    info_peek = " (peek)" if peek_used else ""
                    print(f"{self.nazwa} TRAFIA {target.nazwa}{info_peek} (odl {dist:.2f}, sz {sz}%) → {dmg} dmg. HP {target.nazwa}={max(0,target.hp)}")
                    return True
                else:
                    info_peek = " z peek" if peek_used else ""
                    print(f"{self.nazwa} chybił{info_peek} (sz {sz}%, rzut {r}).")
                    return False

            # przeszkoda na torze
            if (x, y) in blokady:
                # 1) Peek: jeśli to PIERWSZA przeszkoda i jest sąsiednia do strzelającego
                if not peek_used and adjacent(self.x, self.y, x, y):
                    peek_used = True
                    extra_acc_penalty += PEEK_ACC_PENALTY
                    extra_dmg_factor  *= PEEK_DMG_FACTOR
                    # "przejdź" przez tę jedną przeszkodę
                    x += dx
                    y += dy
                    continue

                # 2) Dalsze przeszkody — normalna logika AP/HE
                if typ == 'ap':
                    penetracja = self.sila_ognia * (0.8 + randint(0, 40) / 100.0)  # 0.8–1.2x
                    if penetracja >= OBSTACLE_RESIST:
                        print(f"AP przebił przeszkodę na ({x},{y}) (pen {penetracja:.1f} ≥ {OBSTACLE_RESIST}).")
                        x += dx; y += dy
                        continue
                    else:
                        print(f"AP zablokowany na ({x},{y}) (pen {penetracja:.1f} < {OBSTACLE_RESIST}).")
                        return False

                elif typ == 'he':
                    print(f"HE eksploduje przy przeszkodzie na ({x},{y}).")
                    # centrum eksplozji: pole ZA przeszkodą
                    cx, cy = x + dx, y + dy
                    dmg_any = 0
                    for ex in range(cx-1, cx+2):
                        for ey in range(cy-1, cy+2):
                            if (ex, ey) == (target.x, target.y):
                                dist_center = self.dystans_do(ex, ey)
                                dmg = self.policz_obrazenia(target, dist_center, dmg_factor=0.6 * extra_dmg_factor)
                                if dmg > 0:
                                    target.hp -= dmg
                                    dmg_any += dmg
                    if dmg_any > 0:
                        print(f"HE zraniło cel zza przeszkody o {dmg_any} dmg. HP {target.nazwa}={max(0,target.hp)}")
                        return True
                    else:
                        print("HE eksplozja nie dosięgła celu.")
                        return False

                else:
                    print("Nieznany typ amunicji. Użyj 'ap' lub 'he'.")
                    return False

            # brak przeszkody — leć dalej
            x += dx
            y += dy

        print("Pocisk opuścił planszę bez trafienia.")
        return False

# --- GRA ---
if __name__ == "__main__":
    # Przykładowe statystyki dwóch różnych czołgów
    p1 = Czolag("Gracz 1", hp=610, pancerz=100, celnosc=60, kaliber=20,  ostrosc=2.0,
                v_poj=20, v_poc=70, x=2,    y=H//2, symbol='P')
    p2 = Czolag("Gracz 2", hp=200, pancerz=5,   celnosc=30, kaliber=120, ostrosc=1.5,
                v_poj=90, v_poc=90, x=W-3,  y=H//2, symbol='E')

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

        # sprawdzenie zwycięstwa
        if not p2.zyje():
            rysuj(p1, p2, blokady)
            print("\nGracz 2 zniszczony! Wygrywa Gracz 1.")
            break
        if not p1.zyje():
            rysuj(p1, p2, blokady)
            print("\nGracz 1 zniszczony! Wygrywa Gracz 2.")
            break

    print("\nKONIEC BITWY.")

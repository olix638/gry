# Gra: czołgi z przeszkodami (#) które blokują ruch i ostrzał (linia strzału)
from random import randint, choice, seed
import math
import os

W, H = 13, 11                 # rozmiar planszy
LICZBA_PRZESZKOD = 18         # ile losowych blokad postawić

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def bresenham(x0, y0, x1, y1):
    """Zwraca punkty na prostej między (x0,y0) a (x1,y1), bez końców (start, cel)."""
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy
        # nie dodawaj punktu celu ani startu
        if not (x == x1 and y == y1) and not (x == x0 and y == y0):
            points.append((x, y))
    return points

class Czołg:
    def __init__(self, nazwa, zdrowie, pancerz, celność,
                 kaliber, ostrość_pocisku, prędkość_pojazdu, prędkość_pocisku,
                 x=0, y=0):
        self.nazwa = nazwa
        self.zdrowie = zdrowie
        self.pancerz = pancerz
        self.celność = celność
        self.kaliber = kaliber
        self.ostrość_pocisku = ostrość_pocisku
        self.siła_ognia = kaliber * ostrość_pocisku
        self.prędkość_pojazdu = prędkość_pojazdu
        self.prędkość_pocisku = prędkość_pocisku
        self.x = x
        self.y = y

    def żyje(self):
        return self.zdrowie > 0

    def dystans_do(self, inny):
        return math.hypot(self.x - inny.x, self.y - inny.y)

    def linia_czysta(self, cel, przeszkody):
        """Sprawdza, czy między czołgami nie ma przeszkody (#)."""
        for px, py in bresenham(self.x, self.y, cel.x, cel.y):
            if (px, py) in przeszkody:
                return False
        return True

    def policz_szanse(self, cel):
        # bazowo i modyfikatory
        sz = 50 + self.celność * 0.4 + self.prędkość_pocisku * 0.15 - cel.prędkość_pojazdu * 0.25
        # kara za dystans
        sz -= self.dystans_do(cel) * 2
        return max(5, min(95, int(sz)))

    def policz_obrażenia(self, cel):
        # spadek obrażeń z dystansem (prosty model)
        optimal = 3.0
        dist = self.dystans_do(cel)
        if dist <= optimal:
            factor = 1.0
        else:
            factor = max(0.3, 1.0 - (dist - optimal) * 0.15)
        dmg = max(0, int(self.siła_ognia * factor - cel.pancerz))
        return dmg, dist, factor

    def atakuj(self, cel, przeszkody):
        # sprawdź linię strzału najpierw
        if not self.linia_czysta(cel, przeszkody):
            print(f"{self.nazwa}: strzał ZABLOKOWANY przez przeszkodę!")
            return False, 0, None, None, self.dystans_do(cel), None

        szansa = self.policz_szanse(cel)
        rzut = randint(1, 100)
        if rzut <= szansa:
            dmg, dist, factor = self.policz_obrażenia(cel)
            cel.zdrowie -= dmg
            print(f"{self.nazwa} TRAFIA {cel.nazwa} (szansa {szansa}%, rzut {rzut}) "
                  f"odl {dist:.2f}, mnożnik {factor:.2f} → {dmg} dmg. HP {cel.nazwa}={max(0,cel.zdrowie)}")
            return True, dmg, szansa, rzut, dist, factor
        else:
            print(f"{self.nazwa} CHYBIŁ (szansa {szansa}%, rzut {rzut}). Odległość {self.dystans_do(cel):.2f}")
            return False, 0, szansa, rzut, self.dystans_do(cel), None

    def rusz(self, kierunek, przeszkody):
        nx, ny = self.x, self.y
        if kierunek == 'w' and self.y > 0:
            ny -= 1
        elif kierunek == 's' and self.y < H - 1:
            ny += 1
        elif kierunek == 'a' and self.x > 0:
            nx -= 1
        elif kierunek == 'd' and self.x < W - 1:
            nx += 1
        # nie wchodź na przeszkodę
        if (nx, ny) not in przeszkody:
            self.x, self.y = nx, ny

def generuj_przeszkody(ile, zajęte):
    przeszkody = set()
    próby = 0
    while len(przeszkody) < ile and próby < 10000:
        próby += 1
        x = randint(0, W - 1)
        y = randint(0, H - 1)
        if (x, y) in zajęte:
            continue
        przeszkody.add((x, y))
    return przeszkody

def rysuj(plr, enemy, przeszkody):
    clear()
    board = [['.' for _ in range(W)] for __ in range(H)]
    for (ox, oy) in przeszkody:
        board[oy][ox] = '#'
    board[plr.y][plr.x] = 'P'
    board[enemy.y][enemy.x] = 'E'
    for y in range(H):
        print(''.join(board[y]))
    print(f"\n{plr.nazwa}: HP={plr.zdrowie}  Pos=({plr.x},{plr.y})")
    print(f"{enemy.nazwa}: HP={enemy.zdrowie}  Pos=({enemy.x},{enemy.y})")

def ai_action(enemy, plr, przeszkody):
    # jeśli jest czysta linia i szansa sensowna → strzel
    if enemy.linia_czysta(plr, przeszkody):
        sz = enemy.policz_szanse(plr)
        if sz >= 30 and randint(1, 100) <= 80:
            return 'fire'

    # spróbuj zbliżyć się redukując dystans, omijając # (proste heurystyki)
    kierunki = []
    if enemy.x < plr.x: kierunki.append('d')
    if enemy.x > plr.x: kierunki.append('a')
    if enemy.y < plr.y: kierunki.append('s')
    if enemy.y > plr.y: kierunki.append('w')

    # przetasuj priorytet (losowy wybór z „dobrych”)
    for k in kierunki + ['w','a','s','d']:
        nx, ny = enemy.x, enemy.y
        if k == 'w': ny -= 1
        if k == 's': ny += 1
        if k == 'a': nx -= 1
        if k == 'd': nx += 1
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in przeszkody:
            return k
    return choice(['w','a','s','d'])

# --- Gra ---
if __name__ == "__main__":
    # seed(0)  # opcjonalnie stała losowość
    gracz = Czołg("Pancernik", 610, 100, 60, 20, 2.0, 20, 70, x=2, y=5)
    wróg   = Czołg("Niszczyciel", 200, 5, 30, 120, 1.5, 90, 90, x=W-3, y=5)

    # wygeneruj przeszkody, nie stawiaj na pozycjach czołgów
    zajęte = {(gracz.x, gracz.y), (wróg.x, wróg.y)}
    przeszkody = generuj_przeszkody(LICZBA_PRZESZKOD, zajęte)

    tura = 1
    while gracz.żyje() and wróg.żyje():
        rysuj(gracz, wróg, przeszkody)
        print(f"\nTura {tura}. Komendy: w/a/s/d=ruch, f=ogień, q=wyjście")
        cmd = input("> ").strip().lower()
        if cmd == 'q':
            print("Koniec gry.")
            break
        if cmd in ('w', 'a', 's', 'd'):
            gracz.rusz(cmd, przeszkody)
        elif cmd == 'f':
            gracz.atakuj(wróg, przeszkody)
        else:
            print("Nieznana komenda.")

        if not wróg.żyje():
            print("\nWróg zniszczony! Wygrałeś.")
            break

        # Ruch/akcja wroga
        akcja = ai_action(wróg, gracz, przeszkody)
        if akcja == 'fire':
            wróg.atakuj(gracz, przeszkody)
        else:
            wróg.rusz(akcja, przeszkody)

        if not gracz.żyje():
            print("\nTwój czołg został zniszczony. Przegrana.")
            break

        input("Enter, aby kontynuować...")
        tura += 1

    print("\nKONIEC BITWY.")

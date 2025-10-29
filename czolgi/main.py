#!/usr/bin/env python3
"""
Terminalowa gra "Czołgi" w Pythonie (jednoplatformowa, bez zewnętrznych bibliotek).
Plik: terminal_tanks.py

Instrukcje:
- Uruchom: python3 terminal_tanks.py
- Sterowanie (po każdej turze wpisz komendę i naciśnij Enter):
    w - ruch w górę
    s - ruch w dół
    a - ruch w lewo
    d - ruch w prawo
    f - ogień
    q - zakończ grę

Opis:
- Gracz steruje czołgiem oznaczonym "P".
- Wrogowie oznaczeni są literą "E" i poruszają się losowo.
- Pociski: "*" (gracza i przeciwników).
- Przeszkody: "#" (nieprzebijalne)
- Celem: przetrwać i zniszczyć przeciwników.

Kod jest prosty i łatwy do rozbudowy: AI przeciwników, bonusy, mapa z plików, tryb wieloosobowy.
"""

import os
import random
import time
from dataclasses import dataclass
from typing import List, Tuple

WIDTH = 30
HEIGHT = 15
NUM_ENEMIES = 4
NUM_OBSTACLES = 40
TICK_DELAY = 0.08  # opóźnienie między ruchami pocisków (sekundy) - gra krokowa, można zmienić


@dataclass
class Entity:
    x: int
    y: int


@dataclass
class Tank(Entity):
    hp: int
    symbol: str
    is_player: bool = False


@dataclass
class Bullet(Entity):
    dx: int
    dy: int
    owner: str  # 'player' lub 'enemy'


class Game:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.player = Tank(w // 2, h - 2, hp=3, symbol='P', is_player=True)
        self.enemies: List[Tank] = []
        self.bullets: List[Bullet] = []
        self.obstacles: List[Tuple[int, int]] = []
        self.turn = 0
        self.spawn_enemies(NUM_ENEMIES)
        self.place_obstacles(NUM_OBSTACLES)

    def spawn_enemies(self, n: int):
        for _ in range(n):
            while True:
                x = random.randint(1, self.w - 2)
                y = random.randint(1, max(2, self.h // 3))
                if not self.is_occupied(x, y):
                    self.enemies.append(Tank(x, y, hp=1, symbol='E'))
                    break

    def place_obstacles(self, n: int):
        for _ in range(n):
            while True:
                x = random.randint(1, self.w - 2)
                y = random.randint(2, self.h - 3)
                if not self.is_occupied(x, y):
                    self.obstacles.append((x, y))
                    break

    def is_occupied(self, x: int, y: int) -> bool:
        if (x, y) in self.obstacles:
            return True
        if self.player.x == x and self.player.y == y:
            return True
        for e in self.enemies:
            if e.x == x and e.y == y:
                return True
        return False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self):
        board = [[' ' for _ in range(self.w)] for __ in range(self.h)]
        # borders
        for x in range(self.w):
            board[0][x] = '-'
            board[self.h - 1][x] = '-'
        for y in range(self.h):
            board[y][0] = '|'
            board[y][self.w - 1] = '|'
        # obstacles
        for (ox, oy) in self.obstacles:
            board[oy][ox] = '#'
        # bullets
        for b in self.bullets:
            if 0 < b.x < self.w - 1 and 0 < b.y < self.h - 1:
                board[b.y][b.x] = '*'
        # enemies
        for e in self.enemies:
            if 0 < e.x < self.w - 1 and 0 < e.y < self.h - 1:
                board[e.y][e.x] = e.symbol
        # player
        board[self.player.y][self.player.x] = self.player.symbol

        self.clear_screen()
        print(f"Tura: {self.turn}   HP: {self.player.hp}   Enemies: {len(self.enemies)}")
        for row in board:
            print(''.join(row))
        print("Sterowanie: w/a/s/d - ruch, f - ogień, q - wyjscie")

    def step_bullets(self):
        new_bullets: List[Bullet] = []
        for b in self.bullets:
            b.x += b.dx
            b.y += b.dy
            # check bounds
            if not (0 < b.x < self.w - 1 and 0 < b.y < self.h - 1):
                continue
            # hit obstacle?
            if (b.x, b.y) in self.obstacles:
                continue
            # hit enemy?
            if b.owner == 'player':
                hit = None
                for e in self.enemies:
                    if e.x == b.x and e.y == b.y:
                        hit = e
                        break
                if hit:
                    self.enemies.remove(hit)
                    continue
            else:
                # bullet from enemy -> player
                if self.player.x == b.x and self.player.y == b.y:
                    self.player.hp -= 1
                    continue
            # friendly fire (enemy to enemy) ignored
            new_bullets.append(b)
        self.bullets = new_bullets

    def enemies_action(self):
        for e in list(self.enemies):
            # simple AI: chance to fire if aligned with player
            if e.x == self.player.x and random.random() < 0.3 and e.y < self.player.y:
                self.bullets.append(Bullet(e.x, e.y + 1, 0, 1, owner='enemy'))
            else:
                # move randomly but not into obstacles or other enemies
                dx, dy = random.choice([(0,1),(0,-1),(1,0),(-1,0),(0,0)])
                nx, ny = e.x + dx, e.y + dy
                if 0 < nx < self.w - 1 and 0 < ny < self.h - 1 and not self.is_occupied(nx, ny):
                    e.x, e.y = nx, ny

    def player_fire(self):
        # fire upwards from player
        bx, by = self.player.x, self.player.y - 1
        if (bx, by) in self.obstacles:
            return
        self.bullets.append(Bullet(bx, by, 0, -1, owner='player'))

    def handle_input(self, cmd: str) -> bool:
        cmd = cmd.strip().lower()
        if cmd == 'q':
            return False
        if cmd == 'w':
            nx, ny = self.player.x, self.player.y - 1
            if 0 < ny and (nx, ny) not in self.obstacles:
                self.player.y = max(1, ny)
        elif cmd == 's':
            nx, ny = self.player.x, self.player.y + 1
            if ny < self.h - 1 and (nx, ny) not in self.obstacles:
                self.player.y = min(self.h - 2, ny)
        elif cmd == 'a':
            nx, ny = self.player.x - 1, self.player.y
            if nx > 0 and (nx, ny) not in self.obstacles:
                self.player.x = max(1, nx)
        elif cmd == 'd':
            nx, ny = self.player.x + 1, self.player.y
            if nx < self.w - 1 and (nx, ny) not in self.obstacles:
                self.player.x = min(self.w - 2, nx)
        elif cmd == 'f':
            self.player_fire()
        # ignore unknown commands but keep playing
        return True

    def spawn_more_enemies_if_needed(self):
        # podstawowa mechanika: od czasu do czasu pojawia się nowy przeciwnik
        if len(self.enemies) < NUM_ENEMIES and random.random() < 0.05:
            self.spawn_enemies(1)

    def run(self):
        alive = True
        while alive and self.player.hp > 0:
            self.turn += 1
            self.draw()
            # get player command
            try:
                cmd = input('> ')
            except EOFError:
                cmd = 'q'
            alive = self.handle_input(cmd)
            # enemies act
            self.enemies_action()
            # move bullets multiple times for smoother travel
            self.step_bullets()
            # enemy bullets can hit player at position (already handled in step_bullets)
            self.spawn_more_enemies_if_needed()
            # small pause so game isn't instant; adjust if needed
            time.sleep(TICK_DELAY)

        self.clear_screen()
        if self.player.hp <= 0:
            print('Twój czołg został zniszczony. Koniec gry.')
        else:
            print('Koniec gry. Dzięki za grę!')


if __name__ == '__main__':
    random.seed()
    g = Game(WIDTH, HEIGHT)
    g.run()

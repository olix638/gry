import pygame
import sys

# ---------- POSTAĆ ----------
class Postać:
    def __init__(self, imie, zdrowie, pancerz, charyzma, siła, inteligencja, zręczność, Mądrość, ruch, biegłość, dla_kogo: list):
        self.imie = imie
        self.siła = siła
        self.zręczność = zręczność
        self.inteligencja = inteligencja
        self.Mądrość = Mądrość
        self.charyzma = charyzma
        self.ruch = ruch
        self.biegłość = biegłość
        self.pancerz = pancerz
        self.zdrowie = zdrowie

        self.akrobatyka = zręczność + (biegłość if "akrobatyka" in dla_kogo else 0)
        self.perswazja = charyzma + (biegłość if "perswazja" in dla_kogo else 0)
        self.Percepcja = Mądrość + (biegłość if "percepcja" in dla_kogo else 0)

        self.naajedzenie = 10
        self.nawodnienie = 10
        self.sen = 8


# ---------- GRACZ ----------
class GraczSprite:
    def __init__(self, postac):
        self.postac = postac
        self.x = 400
        self.y = 300
        self.size = 32

    def ruch(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.postac.ruch
        if keys[pygame.K_d]:
            self.x += self.postac.ruch
        if keys[pygame.K_w]:
            self.y -= self.postac.ruch
        if keys[pygame.K_s]:
            self.y += self.postac.ruch

    def rysuj(self, screen):
        pygame.draw.rect(screen, (0, 150, 255),
                         (self.x, self.y, self.size, self.size))


# ---------- INIT ----------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG 2D – Prototype")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ---------- POSTAĆ GRACZA ----------
gracz = Postać(
    imie="Aren",
    zdrowie=100,
    pancerz=12,
    charyzma=3,
    siła=4,
    inteligencja=2,
    zręczność=5,
    Mądrość=3,
    ruch=5,
    biegłość=2,
    dla_kogo=["percepcja", "akrobatyka", "perswazja"]
)

sprite = GraczSprite(gracz)

# ---------- HUD ----------
def rysuj_hud():
    teksty = [
        f"Imię: {gracz.imie}",
        f"Zdrowie: {gracz.zdrowie}",
        f"Pancerz: {gracz.pancerz}",
        f"Percepcja: {gracz.Percepcja}",
        f"Perswazja: {gracz.perswazja}"
    ]
    for i, txt in enumerate(teksty):
        surface = font.render(txt, True, (255, 255, 255))
        screen.blit(surface, (10, 10 + i * 22))


# ---------- PĘTLA GRY ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    sprite.ruch(keys)

    screen.fill((30, 30, 30))
    sprite.rysuj(screen)
    rysuj_hud()

    pygame.display.flip()
    clock.tick(60)

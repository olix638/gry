from random import *
class Postać:
    def __init__(self, imie, życie, atak, obrona):
        self.imie = imie
        self.życie = życie
        self.atak = int(atak * (90/100))
        self.atak_obrony = int(atak * (10/100))
        self.obrona = obrona

    def zaatakuj(self, wrog):
        obrażenia = max(0, randint(self.atak - 20, self.atak) - wrog.obrona)
        obrażenia_obrony = max(0,wrog.obrona - randint(self.atak_obrony - 5, self.atak_obrony))
        wrog.życie -= obrażenia
        wrog.obrona -= obrażenia_obrony
        print(f"{self.imie} zadaje {obrażenia} obrażeń {wrog.imie}!")

    def żyje(self):
        return self.życie > 0

    def zwiększ_obronę(self, o_ile):
        self.obrona += o_ile

    def zmiejsz_obronę(self, o_ile):
        self.obrona -= o_ile

    def zwiększ_atak(self, o_ile):
        self.atak += o_ile

    def zmiejsz_atak(self, o_ile):
        self.atak -= o_ile

    def zwiększ_życie(self, o_ile):
        self.życie += o_ile

    def zmiejsz_życie(self, o_ile):
        self.życie -= o_ile

    def __str__(self):
        return f"{self.imie}: Życie={self.życie}, Atak={self.atak}, Obrona={self.obrona}"

Tehar = Postać("Tehar", 100, 10, 0)
Hocrona = Postać("Hocrona", 100, 50, 50)

# Przykładowa tura
Tehar.zaatakuj(Hocrona)
Hocrona.zaatakuj(Tehar)

print(Tehar)
print(Hocrona)
import json
import os
def usun_plik(plik):
    try:
        os.remove(plik)  # nazwa pliku do usunięcia
        print("Plik został usunięty.")
    except FileNotFoundError:
        print("Plik nie istnieje.")

def zapisz_gre(stan_gry, plik):
    with open(f"gry/zwierzak/saves/{plik}.json", "w") as f:
        json.dump(stan_gry, f)
    print("Gra zapisana!")
def wczytaj_gre(plik):
    try:
        with open(f"{plik}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Brak zapisu gry.")
        return None
class Zwierzak:
    def __init__(self,imie,glod,zadowolenie,zmęczenie):
        self.imie = imie
        self.glod = glod
        self.zadowolenie = zadowolenie
        self.zmęczenie = zmęczenie
    def nakarm(self):
        self.glod =max(0,self.glod - 3.0) 
        self.zadowolenie = max(self.zadowolenie - 1.0)
        self.zmęczenie = max(self.zmęczenie-0.5)
    def baw_sie(self):
        self.zadowolenie = max(0,self.zadowolenie + 3.0)
        self.glod = max(0,self.glod - 1.0)
        self.zmęczenie =max(0,self.zmęczenie + 5.0)
    def daj_spać(self):
        self.zmęczenie =max(0,self.zmęczenie - 5.0)
        self.glod = max(0,self.glod + 1.0)
    def stan(self):
        return f"Imie:{self.imie}, Głód:{self.glod}, Zadowolenie:{self.zadowolenie}, Zmęczenie:{self.zmęczenie}"
karol = Zwierzak("Karol",5.0,5.0,0.0)
while karol.glod < 10 and karol.zadowolenie > 0 and karol.zmęczenie < 20:
    print(karol.stan())
    print("0. wczytaj gre")
    print("1. Nakarm zwierzaka")
    print("2. Baw się ze zwierzakiem")
    print("3. Daj zwierzakowi spać")
    print("4.zapisz gre i skończ gre")
    wybor = input("Wybierz opcję: ")
    if wybor == "0":
        zapis = wczytaj_gre("gry/zwierzak/zapis_gry")
        if zapis is None:
            continue
        karol.imie = zapis["imie"]
        karol.glod = zapis["glod"]
        karol.zadowolenie = zapis["zadowolenie"]
        karol.zmęczenie = zapis["zmęczenie"]
    if wybor == "1":
        karol.nakarm()
    elif wybor == "2":
        karol.baw_sie()
    elif wybor == "3":
        karol.daj_spać()
    elif wybor == "4":
        zapisz_gre({
            "imie": karol.imie,
            "glod": karol.glod,
            "zadowolenie": karol.zadowolenie,
            "zmęczenie": karol.zmęczenie
        }, "gry/zwierzak/zapis_gry")
        break
    elif wybor not in ["0","1","2","3","4"]:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
if karol.glod >=10 and karol.zadowolenie <= 0 and karol.zmęczenie >= 20:
    usun_plik("gry/zwierzak/zapis_gry.json")
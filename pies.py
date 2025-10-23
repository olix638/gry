class Zwierzak:
    def __init__(self,imie,glod,zadowolenie,zmęczenie):
        self.imie = imie
        self.glod = glod
        self.zadowolenie = zadowolenie
        self.zmęczenie = zmęczenie
    def nakarm(self):
        self.glod += 1
        self.zadowolenie -= 1
        self.zmęczenie += 0.5
    def baw_sie(self):
        self.zadowolenie += 1
        self.glod -= 1
        self.zmęczenie += 5
    def daj_spać(self):
        self.zmęczenie -= 5
        self.glod += 1
    def stan(self):
        return f"Imie:{self.imie}, Głód:{self.glod}, Zadowolenie:{self.zadowolenie}, Zmęczenie:{self.zmęczenie}"
karol = Zwierzak("Karol",5,5,0)
while karol.glod < 10 and karol.zadowolenie > 0 and karol.zmęczenie < 10:
    print(karol.stan())
    print("1. Nakarm zwierzaka")
    print("2. Baw się ze zwierzakiem")
    print("3. Daj zwierzakowi spać")
    wybor = input("Wybierz opcję: ")
    if wybor == "1":
        karol.nakarm()
    elif wybor == "2":
        karol.baw_sie()
    elif wybor == "3":
        karol.daj_spać()
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
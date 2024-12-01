class Igra:
    def __init__(self, n):
        self.n = n  # str. tabele
        self.tabla = self.napraviTablu(n)  # niz sa koordinatama table
        self.gumice = []  # lista listi svih razvučenih gumica
        self.trouglici = {'X': [], 'O': []}  # lista zauzetih trouglića, mora da razgranicimo X i O zbog stampanja kasnije
        self.rezultat = {'X': 0, 'O': 0}  # rezultat igre
        self.na_potezu = 'X'  # prvi igrač
        self.covek_na_potezu = True # defaultno prvo igra covek, false da prvi igra racunar

    def napraviTablu(self, n):
        tabla = []  

        for q in range(1, n + 2):  # (gornji deo šestougla)
            for r in range(1, n + q + 1):
                tabla.append((q,r))
                
        for q in range(n + 2, 2 * n + 2):  #  (donji deo šestougla)
            for r in range(1, 3*n - q + 3):  
                tabla.append((q,r))
                

        return tabla

    def prikaziStanje(self):
        max_red = max(red for red, _ in self.tabla)
        prikaz = []
        razmak_izmedju_tacaka = 6

        # Priprema horizontalnih gumica
        horizontalne_gumice = set()
        dijagonalne_gumice = []

        for gumica in self.gumice:
            if gumica[0][0] == gumica[1][0]:  # horizontalna gumica (-)
                red, kolona1 = gumica[0]
                _, kolona2 = gumica[1]
                for kolona in range(min(kolona1, kolona2), max(kolona1, kolona2)):
                    horizontalne_gumice.add((red, kolona, kolona + 1))
            elif gumica[0][1] == gumica[1][1]:  # dijagonalna gumica (/)
                dijagonalne_gumice.append(gumica)

        for red in range(1, max_red + 1):
            kolone = sorted(kolona for r, kolona in self.tabla if r == red)

            if red <= max_red // 2 + 1:
                razmaci = max_red - red  # gornji deo
            else:
                razmaci = red - (max_red // 2 - 2)  # donji deo

            red_prikaza = ' ' * (razmaci * razmak_izmedju_tacaka // 2)  # prazan prostor na pocetku
            razmak_red = list(' ' * (len(red_prikaza) + (len(kolone) - 1) * razmak_izmedju_tacaka))  # linija za razmak

            # iscrtavanje tacaka
            for i, kolona in enumerate(kolone):
                red_prikaza += '●'
                if i < len(kolone) - 1:  # dodaj crtice između tacaka (horizontalne gumice (-))
                    if (red, kolona, kolone[i + 1]) in horizontalne_gumice:
                        red_prikaza += '-' * razmak_izmedju_tacaka
                    else:
                        red_prikaza += ' ' * razmak_izmedju_tacaka

            prikaz.append(red_prikaza.rstrip())

            # provera za dijagonalne gumice (/)
            for gumica in dijagonalne_gumice:
                pocetak, kraj = gumica
                if pocetak[0] <= red < kraj[0]:  # ako smo u opsegu dijagonalne gumice
                    trenutna_kolona = pocetak[1]
                    razmak_do_pocetka = razmaci * (razmak_izmedju_tacaka // 2) + (trenutna_kolona - kolone[0]) * razmak_izmedju_tacaka - razmak_izmedju_tacaka // 2
                    if 0 <= razmak_do_pocetka < len(razmak_red):
                        razmak_red[razmak_do_pocetka] = '  /'

            prikaz.append(''.join(razmak_red).rstrip())  # dodaj prazan red ili red s dijagonalnim gumicama

        # Prikazivanje rezultata
        for red in prikaz:
            print(red)

    def postaviPocetnoStanje(self, n):
        self.__init__(n)
        print(f"Igra je resetovana za tablu veličine {self.n}. Početno stanje je postavljeno.")

    def proveriKrajIgre(self):
        ukupno_trouglica = self.izracunajUkupanBrojTrouglica()
        if self.rezultat['X'] > ukupno_trouglica / 2:  #recimo 28 > (54/2) za n=3
            return True, 'X'  # Pobedio je X
        elif self.rezultat['O'] > ukupno_trouglica / 2:
            return True, 'O'  # Pobedio je O
        elif (self.rezultat['X'] + self.rezultat['O']) == ukupno_trouglica: #nereseno je 
            return True, 'Nerešeno'

        # igra nije završena
        return False, None

    def izracunajUkupanBrojTrouglica(self):
        return self.n * self.n * 6 # n=3 -> 54, n=4 -> 96, n=5 -> 150 ...

    def proveriPotez(self, potez):
        if not isinstance(potez, tuple) or len(potez) != 2:
            print("Neispravan format poteza. Očekuje se ((q, r), smer).")
            return False

        pozicija, smer = potez

        # provera formata pozicije (q, r)
        if not isinstance(pozicija, tuple) or len(pozicija) != 2:
            print("Neispravan format pozicije. Očekuje se (q, r).")
            return False

        q, r = pozicija

        # provera da li su koordinate celobrojne
        if not isinstance(q, int) or not isinstance(r, int):
            print("Koordinate (q, r) moraju biti celi brojevi.")
            return False

        # provera da li postoje takve koordinate na tabli
        if pozicija not in self.tabla:
            print(f"Pozicija {pozicija} nije validna za tablu velicine {self.n}")
            return False
        
        # if pozicija in self.tabla:
        #     print(self.tabla) #ovo ti je ako ces da pogledas koordinate 

        # provera validnosti smera
        validni_smerovi = {'D', 'DL', 'DD'}
        if smer not in validni_smerovi:
            print(f"Smer '{smer}' nije validan. Dozvoljeni smerovi su: {validni_smerovi}.")
            return False

        return True



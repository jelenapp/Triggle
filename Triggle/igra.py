class Igra:
    def __init__(self, n):
        self.n = n  # str. tabele
        self.tabla = self.napraviTablu(n)  # dictionary gde su kljucevi koordinate stubica, vrednosti info o tom stubicu
        self.gumice = []  # lista svih razvučenih gumica
        self.trouglici = []  # lista zauzetih trouglića
        self.rezultat = {'X': 0, 'O': 0}  # rezultat igre
        self.na_potezu = 'X'  # prvi igrač

    def napraviTablu(self, n):
        tabla = {} #dictionary
        for q in range(-n + 1, n): #koordinate stubića u heksagonalnom koordinatnom sistemu (koristi se za šestougaone table)
            for r in range(max(-n + 1, -q - n + 1), min(n, -q + n)): #opseg šestougaone table po jednoj osi.
                tabla[(q, r)] = {'gumice': [], 'trouglici': []}
        return tabla

    def prikaziStanje(self):
        print("Trenutno stanje igre:")
        for (q, r), podaci in self.tabla.items():
            print(f"Stubić ({q}, {r}): Gumice {podaci['gumice']}, Trouglici {podaci['trouglici']}")
        print(f"Rezultat: X - {self.rezultat['X']}, O - {self.rezultat['O']}")


    def postaviPocetnoStanje(self):
        self.tabla = self.napraviTablu(self.n)
        self.gumice = []
        self.trouglici = []
        self.rezultat = {'X': 0, 'O': 0}

        print(f"Igra je resetovana za tablu veličine {self.n}. Početno stanje je postavljeno.")

    def proveriKrajIgre(self):
        ukupno_trouglića = self.izracunajUkupanBrojTrouglica()
        if self.rezultat['X'] > ukupno_trouglića // 2:
            return True, 'X'  # Pobedio je X
        elif self.rezultat['O'] > ukupno_trouglića // 2:
            return True, 'O'  # Pobedio je O

        if not self.daLiImaPoteza():
            if self.rezultat['X'] > self.rezultat['O']:
                return True, 'X'  # Pobedio je X
            elif self.rezultat['O'] > self.rezultat['X']:
                return True, 'O'  # Pobedio je O
            else:
                return True, 'Nerešeno'

        # igra nije završena
        return False, None

    def izracunajUkupanBrojTrouglica(self):
        return 3 * self.n * (self.n - 1)

    def daLiImaPoteza(self):
        for (q, r), stubić in self.tabla.items():
            if len(stubić['gumice']) < 3:  # maksimalno tri gumice po stubiću
                return True
        return False

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

        # provera da li je pozicija unutar opsega table
        if pozicija not in self.tabla:
            print(f"Pozicija {pozicija} nije validna na tabli veličine {self.n}.")
            return False

        # provera validnosti smera
        validni_smerovi = {'D', 'DL', 'DD'}
        if smer not in validni_smerovi:
            print(f"Smer '{smer}' nije validan. Dozvoljeni smerovi su: {validni_smerovi}.")
            return False

        return True


igra = Igra(4)
print(igra.tabla[(0, 0)])
igra.tabla[(0, 0)]['gumice'].append('gumica1')
igra.tabla[(0, 0)]['trouglici'].append('trougao1')
print(igra.tabla[(0, 0)])


igra = Igra(4)
igra.postaviPocetnoStanje()

igra.rezultat['X'] = 29  # više od polovine (28 je polovina za n=4)
igra.rezultat['O'] = 5
kraj, pobednik = igra.proveriKrajIgre()
print(f"Kraj igre: {kraj}, Pobednik: {pobednik}")

print(igra.proveriPotez(((0, 0), 'D')))   # True
print(igra.proveriPotez(((10, 10), 'D'))) #  False (pozicija van table)
print(igra.proveriPotez(((0, 0), 'X')))   #  False (nevalidan smer)
print(igra.proveriPotez((0, 'D')))        #  False (neispravan format poteza)
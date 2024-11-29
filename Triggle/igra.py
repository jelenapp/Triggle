class Igra:
    def __init__(self, n):
        self.n = n  # str. tabele
        self.tabla = self.napraviTablu(n)  # dictionary gde su kljucevi koordinate stubica, vrednosti info o tom stubicu
        self.gumice = []  # lista svih razvučenih gumica
        self.trouglici = []  # lista zauzetih trouglića
        self.rezultat = {'X': 0, 'O': 0}  # rezultat igre
        self.na_potezu = 'X'  # prvi igrač

    def napraviTablu(self, n):
        tabla = {}  # Rečnik za šestougaonu tablu

        for q in range(1, n + 2):  # (gornji deo šestougla)
            for r in range(1, n + q + 1):
                tabla[(q, r)] = {'gumice': [], 'trouglici': []}
                
        for q in range(n + 2, 2 * n + 2):  #  (donji deo šestougla)
            for r in range(1, 3*n - q + 3):  
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


# igra = Igra(4)
# print(igra.tabla[(1, 1)])
# igra.tabla[(1, 1)]['gumice'].append('gumica1')
# igra.tabla[(1, 1)]['trouglici'].append('trougao1')
# print(igra.tabla[(1, 1)])


igra = Igra(3)
igra.postaviPocetnoStanje()

igra.rezultat['X'] = 29  # više od polovine (28 je polovina za n=4)
igra.rezultat['O'] = 5
kraj, pobednik = igra.proveriKrajIgre()
print(f"Kraj igre: {kraj}, Pobednik: {pobednik}")

print(igra.proveriPotez(((3, 6), 'D')))   # True
print(igra.proveriPotez(((2, 2), 'D'))) #  true
print(igra.proveriPotez(((8, 5), 'X')))   # false
print(igra.proveriPotez((0, 'D')))        #  False (neispravan format poteza)



# - Pogledaj na prezentaciji kako su prikazali sestougao. Na osnovu toga sam napravio for petlju u napraviTablu fju, osim sto nisam koristio slova za redove
# - Ne svidja mi se sto trenutno za svaku koordinatu imamo gumice[] i trouglice[]. Nema smisla jer prvo te koordinate su stubici i nije nesto mnogo korisno 
# da za svaki stubic cuvamo neke gumice ili trouglice koji nisu ni deo stubica.
# - Moj predlog je da gumice cuvamo tako sto za svaku gumicu pamtimu izmedju kojih koordinata se nalazi. npr gumice[ [(1,1),(1,4)], [(4,1), (4,4)] ]
# taman tako mozemo da napravimo da D,DL,DD automatski generisu tu drugu koordinatu. 
# - npr postaviGumicu(1,1,'D') bi u listu gumice stavilo odma gumicu [(1,1),(1,4)] preko neke simple formule
# - za trouglove nisam nesto detaljno gledao jos kako bismo mogli ali I guess da svaki trougao moze da ima 3 tacke tj 3 koordinate 
# i onda po nekoj formuli na kraju svakog poteza ako se pozicije svih trenutnih gumica poklope tako da formiraju trougao ili trouglove, taj igrac koji je igrao dobija poen/poene
# - trouglove mozemo da cuvamo kao niz i onda tek nakon sto se utvrdi da je trougao 'formiran', stavljamo u niz trouglovi[] koordinate tog trougla
#  da ne bi opet mogao da se zauzme u nekom drugom potezu. to nam je dobro kasnije za stampanje interfejsa

# - u principu mi cemo svakako da pratimo poene live ono posle svakog poteza tkd ne moramo nesto da brojimo kasnije te trouglove iz niza trouglovi[] 
# nego cisto zbog stampe ce nam sluzi i da se spreci da se ne zauzmu vec zauzeti, simple
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

    def prikaziStanje(self): #interfejs
        max_red = max(red for red, _ in self.tabla)
        prikaz = []
        
        for red in range(1, max_red + 1):
            kolone = sorted(kolona for r, kolona in self.tabla if r == red)
            
            if red <= max_red // 2 + 1:  
                razmaci = max_red - red
            else: 
                razmaci = red - (max_red // 2 - (self.n-1)) 
            
            red_prikaza = ' ' * (razmaci * 2)  
            
            for kolona in kolone:
                red_prikaza += '●   '
            
            prikaz.append(red_prikaza.rstrip())
        
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

        if len(self.trouglici) == ukupno_trouglica:
            if self.rezultat['X'] > self.rezultat['O']:
                return True, 'X'  # Pobedio je X
            elif self.rezultat['O'] > self.rezultat['X']:
                return True, 'O'  # Pobedio je O
            else:
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
        #     print(self.tabla) ovo ti je ako ces da pogledas koordinate 

        # provera validnosti smera
        validni_smerovi = {'D', 'DL', 'DD'}
        if smer not in validni_smerovi:
            print(f"Smer '{smer}' nije validan. Dozvoljeni smerovi su: {validni_smerovi}.")
            return False

        return True




print("=============== Igra - n=3 =====================")


igra = Igra(3)

# igra.prikaziStanje() ovo ti je da stampa u konzoli sestougao, proveri slobodno i za n=4,5,6 blabla radi sve

print(igra.izracunajUkupanBrojTrouglica()) #doso sam do formule da za n stranice ima n^2 * 6 trouglica, ovu fju koristimo gore u proveriKrajIgre
print(igra.proveriPotez(((1, 5), 'D')))  # nije moguc za tablu stranice n=3 (False)
igra.gumice.append([(1,1),(1,4)]) #dodajem gumice da vidim da li se posle resetuje kako treba
print(f"gumice:{igra.gumice}")
igra.trouglici['X'] = [[(1,2),(2,2),(2,3)]] #dodajem trouglice isto ono da vidim kasnije da li resetuje lepo
print(f"trouglici:{igra.trouglici}")

print("=============== Igra - n=4 =====================")

igra.postaviPocetnoStanje(4) #ovo je reset i uz reset moze da se postavi nova velicina stranice (sad je n=4)
print(igra.izracunajUkupanBrojTrouglica()) # ukupan broj trouglica je sada drugaciji zbog n=4 (bio je 54 sad je 96)
print(f"gumice:{igra.gumice}") #gumice su isto vracene na prazan niz
print(igra.proveriPotez(((1, 5), 'D')))  # sada je ovaj potez moguc jer je tabla veca (True)

print("===============Provere pobednika=====================")

igra.rezultat['X'] = 49  # više od polovine (49 > (96/2))
igra.rezultat['O'] = 5
kraj, pobednik = igra.proveriKrajIgre()
print(f"Kraj igre: {kraj}, Pobednik: {pobednik}")


print("===============Provere poteza=====================")

print(igra.proveriPotez(((1, 5), 'D')))   # True
print(igra.proveriPotez(((1, 6), 'D'))) #  false
print(igra.proveriPotez(((1, 1), 'X')))   # false
print(igra.proveriPotez((0, 'D')))        #  False (neispravan format poteza)



# - Idemo redom: prvo ubaceno je gore self.covek_na_potezu = True i to je ono iz uslova zadatka da se bira ko prvi igra covek ili racunar
# i ako je covek onda je True ako nije onda False, mada ne znam iskreno sta ce nam to ovde u prvoj fazi ali dobro
# - Tabla je sada niz koordinata, vise ne cuvamo one gluposti gumice i trouglove za svaku koordinatu (stubic) <-- napraviTablu fja
# - Prikazi stanje funkcija je u procesu jos i trenutno sam uspeo samo da napravim sestougao u konzoli na osnovu koordinata iz tabla[]
# mozes da probas da odkomentarises u 'mainu' dole 'igra.prikaziStanje()' i da vidis sta se stampa, i isto mozes da probas i za Igra(4) ili bilo 
# koju velicinu stranice, stampa ga lepo 
# Btw to za interfejs nisam bio ni siguran da li treba da se pravi, ali kapiram valjda da treba da se pravi u konzoli da se prikaze, jer ne bi stavljali 
# one slajdove mrtve sa interfejsom a mnogo je zajebano da se crta tako u konzoli
# Tkd za to prikazi stanje tj crtanje treba da se doradi da se crtaju gumice i trouglici za neko proizvoljno stanje
# tkd jebavao bih se sa tim sutra pa ako uspem uspeo sam, svakako nema nista drugo vise da se radi tolko
# - Dalje imamo da su trouglici postali dictionary da bismo mogli da pratimo trouglice posebno za X i O jer kad stampas u konzoli jebiga 
# ne stampas trouglice nego stampas 'X' i 'O' za svakog igraca posebno, tkd mora tako
# - Ostale stvari, malo sam nesto doradio, skapirao sam formulu kako da se odredi broj trouglica na osnovu velicine stranice sestougla, imas sve gore


# E sad osim tog interfejsa koji treba da iscrtam nekako, nema toliko nista spec vise da se radi
# Oni su stavljali u ovim zahtevima za fazu 1 kao izbor ko prvi igra, unos poteza ali bez odigravanja poteza itd, tkd ja kapiram da ne treba 
#da postoji nikakva ono live interakcija u konzoli jos gde korisnik bira ko igra prvi itd nego sve to ide preko funkcija za sad, testiranje samo
# Ako mislis da ipak treba nesto preko, pogledaj zahteve, uporedi code, i kazi mi.
from igra import Igra

def main(): 
    print("=============== Igra - n=3 =====================")

    igra = Igra(3)

    print(f"Ukupan broj mogucih trouglica: {igra.izracunajUkupanBrojTrouglica()}") #doso sam do formule da za n stranice ima n^2 * 6 trouglica, ovu fju koristimo gore u proveriKrajIgre
    print(igra.proveriPotez(((1, 5), 'D')))  # nije moguc za tablu stranice n=3 (False)
    igra.gumice.append([(1,1),(1,4)]) #dodajem gumice da vidim da li se posle resetuje kako treba
    print(f"gumice:{igra.gumice}")
    igra.trouglici['X'] = [[(1,2),(2,2),(2,3)]] #dodajem trouglice isto ono da vidim kasnije da li resetuje lepo
    print(f"trouglici:{igra.trouglici}")

    print("=============== Igra - n=4 =====================")

    igra.postaviPocetnoStanje(4) #ovo je reset i uz reset moze da se postavi nova velicina stranice (sad je n=4)
    print(f"Ukupan broj mogucih trouglica: {igra.izracunajUkupanBrojTrouglica()}")# ukupan broj trouglica je sada drugaciji zbog n=4 (bio je 54 sad je 96)
    print(f"gumice:{igra.gumice}") #gumice su isto vracene na prazan niz
    print(igra.proveriPotez(((1, 5), 'D')))  # sada je ovaj potez moguc jer je tabla veca (True)

    print("===============Provere pobednika=====================")

    igra.rezultat['X'] = 49  # više od polovine (49 > (96/2))
    igra.rezultat['O'] = 5
    kraj, pobednik = igra.proveriKrajIgre()
    print(f"Kraj igre: {kraj}, Pobednik: {pobednik}")

    igra.rezultat['X'] = 40
    igra.rezultat['O'] = 40
    kraj, pobednik = igra.proveriKrajIgre()
    print(f"Kraj igre: {kraj}, Pobednik: {pobednik}") #false zato sto je 40:40, jos se igra

    igra.rezultat['X'] = 48
    igra.rezultat['O'] = 48
    kraj, pobednik = igra.proveriKrajIgre()
    print(f"Kraj igre: {kraj}, Pobednik: {pobednik}")  #true zato sto je dostignut krajnji rezultat
    # u praksi jedino kada je rezultat['X'] + rezultat['O'] = broj trouglica je kad je rezultat neresen (48:48 -> 48+48=96 - kraj)
    # u svakom drugom slucaju gde rezultat prelazi 48 i biva recimo 49:47, 49:35, 49:10...igra se zavrsava jer je pobednik vec poznat
    # simple: neko od igraca presao polovinu trouglica? kraj igre. nijedan nije presao polovinu trouglica? nije kraj igre. 
    # oba nisu presli polovinu trouglica a zbir poena je max broj trouglica? kraj igre - nereseno

    print("===============Provere poteza=====================")

    print(igra.proveriPotez(((1, 5), 'D')))   # True
    print(igra.proveriPotez(((1, 6), 'D'))) #  false
    print(igra.proveriPotez(((1, 1), 'X')))   # false
    print(igra.proveriPotez((0, 'D')))        #  False (neispravan format poteza)

    print("==========Prikaz test=================")
    igra.postaviPocetnoStanje(3) #n=3
    igra.gumice = [ #proizvoljno stanje gumica
        [(1, 1), (1, 4)],  # Horizontalna gumica (-) - kod njih imamo da x1=x2, i y2>y1 (1=1 i 4>1 u ovom primeru)
        [(4, 1), (4, 4)],  # Horizontalna gumica (-) - kod njih imamo da x1=x2, i y2>y1 (4=4 i 4>1 u ovom primeru)
        [(1, 2), (4, 2)],  # Dijagonalna gumica (/) - kada pocinju i zavrsavaju se u gornjem delu sestougla vazi uslov x2>x1 i y1=y2 (4>1, 2=2, u ovom primeru)
        [(1,3), (4,3)],    # Dijagonalna gumica (/) - isto kao prethodna
        [(2,4), (5,3)], # ovo je isto dijagonalna gumica (/) samo sto prelazi u donji deo sestougla i tu pravilo odozgo vise ne vazi vec vazi da je x2==x1+3 and y2<y1 (ili samo x2>x1, y2<y1)
        [(3,5), (6,3)], # isto vazi i ovde
    ]

    igra.prikaziStanje()


    #Problem: crtanje dijagonalnih gumica koje prelaze u donji deo sestougla. To su ove gore (2,4)->(5,3) i (3,5)->(6,3)
    # Uslov za prepoznavanje takve gumice je izvucen iz posmatranja svih mogucih takvih gumica, tj:
    #     # 2,2 -> 5,1 |  2,3 -> 5,2 | 2,4 -> 5,3 | 2,5 -> 5,4
    #     # 3,3 -> 6,1 |  3,4 -> 6,2 | 3,5 -> 6,3 | 3,6 -> 6,4
    #     # 4,4 -> 7,1 |  4,5 -> 7,2 | 4,6 -> 7,3 | 4,7 -> 7,4
    # zato vazi:x2==x1+3 and y2<y1 ali verovatno je dovoljno i samo x2>x1, y2<y1

    #Takodje fali crtanje DD dijagonalnih tj (\) i naravno trouglica



if __name__ == "__main__":  
    main()



    # Za izvestaj: 
    # Ideja je da kada se izabere Pocetna koordinata i smer, da se odmah na osnovu toga napravi gumica koju cine pocetna i krajnja koordinata
    # Primer za to bi bio igra.proveriPotez(((1, 1), 'D')))  koji bi kreirao gumicu koja pocinje od (1,1) i zavrsava se u (1,4)
    # Tako bi se u listu gumice dodala gumica [(1,1),(1,4)]... isto ce da vazi i za ostale smerove u zavisnosti od smera
    # Nakon sto se bude odigrao potez tj dodale gumice, proverice se po nekoj formuli da li je formiran trougao i ako jeste cuva se u dict trouglici za tog igraca koji je odigrao potez
    # Naravno taj igrac dobija i poen za taj trouglic i partija se nastavlja.
    # Interfejs treba da isprati to dodavanje gumica i zauzimanje trouglica za X ili O igraca 
    # Provera kraja igre je jednostavna. Ako je igrac premasio polovinu od maksimalnog moguceg broja trouglica, on je vec pobedio
    # Ukoliko se desi da je zbir poena X i O jednak maksimalnom broju trouglica, partija se prekida jer je nereseno (27:27 za n=3)
    # U svakom drugom slucaju, recimo gde je 27:26, 27:0, 11:11 blabla partija se nastavlja
    # Broj maks mogucih trouglica za zauzimanje po partiji se racuna kao n*n*6 za n = velicina str sestougla
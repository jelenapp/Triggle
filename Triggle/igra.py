import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class Triggle:
    def __init__(self, n):
        self.n = n
        self.tabla = self.napraviTablu(n)
        self.gumice = []
        self.preseci = []
        self.trouglici = {'X': [], 'O': []}
        self.rezultat = {'X': 0, 'O': 0}
        self.na_potezu = 'X'
        self.selected_points = []
        self.fig, self.ax = plt.subplots()
        self.status_ax = None

    def napraviTablu(self, n):
        tabla = []
        max_points = 2 * n + 2  # Maksimalni broj tačaka u redu
        for q in range(1, max_points):
            num_points = max_points - abs(n + 1 - q)
            for r in range(1, num_points):
                tabla.append((q, r))
        return tabla

    def draw_table(self):
        self.ax.clear()
        max_row = max([q for q, _ in self.tabla])
        for q, r in self.tabla:
            x = r - (max_row - abs(q - (self.n + 1))) / 2
            y = -(q - 1)
            self.ax.plot(x, y, 'o', color='black')
            

        for gumica in self.gumice:
            x_coords = [
                gumica[0][1] - (max_row - abs(gumica[0][0] - (self.n + 1))) / 2,
                gumica[1][1] - (max_row - abs(gumica[1][0] - (self.n + 1))) / 2,
            ]
            y_coords = [-(gumica[0][0] - 1), -(gumica[1][0] - 1)]
            self.ax.plot(x_coords, y_coords, '-', color='blue', linewidth=2)

        for player, triangles in self.trouglici.items():
            for triangle in triangles:
                points = [
                    (
                        p[1] - (max_row - abs(p[0] - (self.n + 1))) / 2,
                        -(p[0] - 1)
                    ) for p in triangle
                ]
                x_coords = [p[0] for p in points] + [points[0][0]]
                y_coords = [p[1] for p in points] + [points[0][1]]
                
                # Crtanje trougla
                self.ax.fill(x_coords, y_coords, color='lightgray', alpha=0.5)
                
                # Izračunavanje centroida
                centroid_x = sum(x_coords[:-1]) / 3
                centroid_y = sum(y_coords[:-1]) / 3
                
                # Tekst u trouglu sa odgovarajućom bojom
                text_color = 'red' if player == 'X' else 'green'
                self.ax.text(
                    centroid_x, centroid_y, player, fontsize=12, ha='center', va='center', color=text_color
                )

                # Podešavanje izgleda osovine
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        self.update_status()

    def update_status(self):
        if not self.status_ax:
            self.status_ax = self.fig.add_axes([0.1, 0.9, 0.8, 0.05])  # Status bar
        self.status_ax.clear()
        if self.na_potezu == "X":
            self.status_ax.text(0.5, 0.5, " Igrač na potezu: X", fontsize=12, ha='center', va='center', color='red')
        else:
            self.status_ax.text(0.5, 0.5, " Igrač na potezu: O", fontsize=12, ha='center', va='center', color='green')
        self.status_ax.text(
            0.1, 0.2, f"X={self.rezultat['X']}", fontsize=12, ha='left', va='center', color='red'
        )
        self.status_ax.text(
            0.9, 0.2, f"O={self.rezultat['O']}", fontsize=12, ha='right', va='center', color='green'
        )
        self.status_ax.axis('off')


    def onclick(self, event):
        if event.inaxes != self.ax:
            return
        x, y = event.xdata, event.ydata
        max_row = max([q for q, _ in self.tabla])

        # Pronađi najbližu tačku na tabli
        closest = min(
            self.tabla,
            key=lambda p: (
                (p[1] - (max_row - abs(p[0] - (self.n + 1))) / 2 - x) ** 2
                + (-(p[0] - 1) - y) ** 2
            ),
        )
        if closest not in self.selected_points:
            self.selected_points.append(closest)
        if len(self.selected_points) == 2:
            # Proveri validnost gumice (veličina 3)
            if self.valid_gumica(self.selected_points[0], self.selected_points[1]):
                # Obrni tuple ako je potrebno i dodaj gumicu
                start, end = self.selected_points
                if (end < start):  # Obrni ako je krajnja tačka "manja"
                    start, end = end, start

                if not self.presek_tacaka(start, end):  # Proveri da li gumica već postoji
                    print("Gumica već postoji ili je vec obuhvacena!")
                else:
                    # print("Presek tacaka:", self.preseci)
                    self.gumice.append((start, end))
                    # print(f"Nacrtana gumica između tačaka {start} i {end}")
                    # print("Sve gumice:", self.gumice)
                    # print("Svi trouglici:", self.trouglici)
                    if self.proveriKrajIgre():
                        if self.rezultat['X'] > self.rezultat['O']:
                            pobednik = 'Pobedio je X'
                        elif self.rezultat['X'] < self.rezultat['O']:
                            pobednik = 'Pobedio je O'
                        else:
                            pobednik = 'Nereseno je'

                        print(pobednik)

                        
                    self.switch_player()
            else:
                print("Nevalidna gumica!")

            self.selected_points.clear()

        self.update_display()

    def presek_tacaka(self, start, end):
        q1, r1 = start
        q2, r2 = end
        presecitemp = self.preseci[:] #cuvamo trenutnu vrednost liste preseci da bismo posle videli da li je doslo do promene, ako nije to znaci da se sve duzi gumice vec nalaze u preseci i samim tim gumica nije validna
        promenjenipreseci = True
        # Horizontalna gumica
        if q1 == q2:
            for r in range(r1, r2):
                duz = ((q1, r), (q1, r + 1))
                if duz not in self.preseci:
                    self.preseci.append(duz)
                    self.check_new_triangle(duz)

        # Dijagonalne gumice 
        elif q2 - q1 == 3:
            if q2 <= self.n+1: #gornja polovina
                if r2 == r1:  # dole levo
                    for step in range(3):
                        duz = ((q1 + step, r1), (q1 + step + 1, r1)) #raste q1, r1 ostaje isto
                        if duz not in self.preseci:
                            self.preseci.append(duz)
                            self.check_new_triangle(duz)
            
                elif r2 == r1 + 3:  # dole desno
                    for step in range(3):
                        duz = ((q1 + step, r1 + step), (q1 + step + 1, r1 + step + 1)) #rastu q1 i r1
                        if duz not in self.preseci:
                            self.preseci.append(duz)
                            self.check_new_triangle(duz)

            elif q1 >= self.n+1: #donja polovina
                if r2 == r1:  # dole desno
                    for step in range(3):
                        duz = ((q1 + step, r1), (q1 + step + 1, r1)) #raste q1, r1 ostaje isto
                        if duz not in self.preseci:
                            self.preseci.append(duz)
                            self.check_new_triangle(duz)

                elif r2 == r1 - 3:  # dole levo
                    for step in range(3):
                        duz = ((q1 + step, r1 - step), (q1 + step + 1, r1 - step - 1)) #raste q1, r1 se smanjuje
                        if duz not in self.preseci:
                            self.preseci.append(duz)
                            self.check_new_triangle(duz)

            elif (q1<(self.n+1) and q2>(self.n+1)): #pocelo na gornjoj polovini i zavrsilo se na donjoj
                temp = 0
                if r2 == r1+((self.n+1)-q1):  # dole desno
                    for step in range(3):
                        if q1+step == self.n + 1:
                            temp = r1 + step #cuva se taj r1 + step u trenutku prelaska polovine

                        duz = ((q1 + step, r1 + step if temp == 0 else temp), (q1 + step + 1, r1 + step + 1 if temp == 0 else temp )) #raste q1, r1 raste do polovina a onda ostaje isto
    
                        if duz not in self.preseci:
                            self.preseci.append(duz)
                            self.check_new_triangle(duz)

                elif r2 == r1-(q2-(self.n+1)):  # dole levo
                    for step in range(3):
                        duz = ((q1 + step, r1 if temp==0 else temp-step), (q1 + step + 1, r1 if temp==0 else temp-step-1)) #raste q1, r1 ostaje isto do polovine a onda se smanjuje 
                        if q1+step+1 == self.n + 1:
                            temp = r1+step+1  #cuva r1+step+1 u trenutku prelaska polovine

                        if duz not in self.preseci:
                            self.preseci.append(duz)
                            self.check_new_triangle(duz)
        
        if self.preseci == presecitemp:
            promenjenipreseci = False

        return promenjenipreseci

    def valid_gumica(self, start, end):
        q1, r1 = start 
        q2, r2 = end 
        
        if(q2<q1 or (q2==q1 and r1>r2)): #ako se rastegne gumica gore levo, gore desno, levo onda odmah obrcemo q1,r1 i q2,r2 tako da ako je gumica (4,1)->(1,1) to postaje (1,1)->(4,1)
            temp = q2, r2
            q2, r2 = start
            q1, r1 = temp


        # Horizontalna gumica (fiksna dužina 3)
        if (q1 == q2 and r2 == r1+3):
            return True

        # Dijagonalna (fiksna dužina 3)
        if q2 == q1 + 3:
            if (q2 <= self.n+1 and (r2 == r1+3 or r2==r1)):
                return True
            elif (q1 >= self.n+1 and (r2==r1 or  r2 == r1-3)):
                return True
            elif (q1<(self.n+1) and q2>(self.n+1) and (r2 == r1+((self.n+1)-q1) or r2 == r1-(q2-(self.n+1)))):
                return True
           
        return False

    def check_new_triangle(self, new_edge):
        """
        Proverava da li nova duž formira trougao sa postojećim dužima u preseku.
        Ako trougao postoji, dodaje ga trenutnom igraču.
        """
        q1, r1 = new_edge[0]
        q2, r2 = new_edge[1]

        # Iteriraj kroz sve postojeće duži u preseku
        for edge in self.preseci:
            q3, r3 = edge[0]
            q4, r4 = edge[1]

            # Proveri zajedničke tačke između nove duži i postojeće
            common_points = set([(q1, r1), (q2, r2)]).intersection(set([(q3, r3), (q4, r4)]))
            if len(common_points) == 1:  # Ako postoji tačno jedna zajednička tačka
                shared_point = common_points.pop()

                # Pronađi treću tačku trougla (ona koja nije zajednička)
                remaining_points = list(set([(q1, r1), (q2, r2), (q3, r3), (q4, r4)]) - {shared_point})
                if len(remaining_points) == 2:
                    # Formiraj treću duž i proveri da li postoji u preseku
                    third_edge = tuple(sorted(remaining_points))
                    if third_edge in self.preseci or third_edge[::-1] in self.preseci:
                        # Formiraj trougao s tri tačke
                        triangle = tuple(sorted([shared_point, remaining_points[0], remaining_points[1]]))
                        if triangle not in self.trouglici['X'] and triangle not in self.trouglici['O']:
                            self.trouglici[self.na_potezu].append(triangle)
                            self.rezultat[self.na_potezu] += 1


    def inicijalizuj_preseke(self):
        for gumica in self.gumice:
            self.presek_tacaka(gumica[0], gumica[1])
            self.switch_player()

    def switch_player(self):
        self.na_potezu = 'O' if self.na_potezu == 'X' else 'X'

    def proveriKrajIgre(self):
        ukupno_trouglica = self.n * self.n * 6  #ukupan broj mogucih trouglica
        if (self.rezultat['X'] > ukupno_trouglica / 2) or (self.rezultat['O'] > ukupno_trouglica / 2) or ((self.rezultat['X'] + self.rezultat['O']) == ukupno_trouglica): #recimo 28 > (54/2) za n=3
            return True  # Pobedio je X 
        # igra nije završena
        return False

    def update_display(self):
        self.draw_table()
        self.fig.canvas.draw_idle()

    def start_game(self):
        self.inicijalizuj_preseke()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.update_display()
        plt.show()


# Pokretanje igre
igra = Triggle(n=3)
# dodas ovo i dobijes partiju pri kraju -> igra.gumice = [((1, 1), (4, 4)), ((1, 4), (4, 4)), ((3, 1), (3, 4)), ((1, 2), (4, 5)), ((2, 5), (5, 4)), ((4, 2), (4, 5)), ((2, 1), (5, 3)), ((2, 3), (5, 2)), ((5, 1), (5, 4)), ((3, 3), (6, 4)), ((3, 5), (6, 3)), ((1, 4), (4, 7)), ((1, 3), (4, 6)), ((3, 3), (3, 6)), ((1, 1), (1, 4)), ((1, 1), (4, 1)), ((2, 1), (2, 4)), ((1, 3), (4, 3)), ((6, 1), (6, 4)), ((3, 1), (6, 2)), ((4, 1), (7, 1)), ((4, 4), (7, 1)), ((2, 3), (5, 5)), ((3, 6), (6, 4)), ((4, 7), (7, 4)), ((1, 2), (4, 2)), ((2, 2), (2, 5)), ((5, 3), (5, 6)), ((4, 1), (4, 4))]
igra.start_game()


#treba ono za kraj igre da se sredi da se ispise ispod sestougla pobednik i da se onemoguci postavljanje gumica nakon kraja igre
#i da dodam dugme za restart igre koje postavlja sve na inicijalnu vrednost
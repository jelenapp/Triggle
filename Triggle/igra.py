import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import messagebox

class Triggle:
    def __init__(self, n, na_potezu):
        self.n = n
        self.tabla = self.napraviTablu(n)
        self.gumice = []
        self.preseci = []
        self.trouglici = {'X': [], 'O': []}
        self.rezultat = {'X': 0, 'O': 0}
        self.na_potezu = na_potezu
        self.selected_points = []
        self.fig, self.ax = plt.subplots(facecolor='#1E1E1E') 
        self.status_ax = None
        self.message_ax = None 
        self.restart_ax = None
        self.temp_line = None  
        self.game_over = False
        self.restart_button = None


    def restart_game(self, event=None):

        self.tabla = self.napraviTablu(self.n)
        self.gumice = []
        self.preseci = []
        self.trouglici = {'X': [], 'O': []}
        self.rezultat = {'X': 0, 'O': 0}
        self.na_potezu = self.na_potezu
        self.game_over = False  
        self.restart_button = None 
                
        self.restart_ax.clear()
        self.restart_ax.axis("off")

        self.ax.clear()
        if self.status_ax:
            self.status_ax.clear()
        if self.message_ax:
            self.message_ax.clear()
            self.message_ax.axis('off')
        
        self.inicijalizuj_preseke()
        self.update_display()
        

    def create_restart_button(self):
        if self.restart_button:
            plt.delaxes(self.restart_button.ax)
        
        self.restart_ax = plt.axes([0.7, 0.02, 0.2, 0.05], facecolor='#2C2C2C')
        self.restart_button = Button(self.restart_ax, 'Igraj', color='#2C2C2C', hovercolor='#404040')
        self.restart_button.label.set_color('white')
        self.restart_button.on_clicked(self.restart_game)

    def napraviTablu(self, n):
        tabla = []
        max_points = 2 * n + 2  # max broj tacaka u redu
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
            self.ax.plot(x, y, 'o', color='black', markeredgecolor='white', markeredgewidth=1.5)            

        for gumica in self.gumice:
            x_coords = [
                gumica[0][1] - (max_row - abs(gumica[0][0] - (self.n + 1))) / 2,
                gumica[1][1] - (max_row - abs(gumica[1][0] - (self.n + 1))) / 2,
            ]
            y_coords = [-(gumica[0][0] - 1), -(gumica[1][0] - 1)]
            self.ax.plot(x_coords, y_coords, '-', color='white', linewidth=2)

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
                
                #crtanje trougla
                self.ax.fill(x_coords, y_coords, color='black', alpha=0.3)
            
                # racunanje centroida
                centroid_x = sum(x_coords[:-1]) / 3
                centroid_y = sum(y_coords[:-1]) / 3
                
                # text u trouglu sa odg bojom
                text_color = '#FFD700' if player == 'X' else '#00FF7F'
                self.ax.text(
                    centroid_x, centroid_y, player, fontsize=12, 
                    ha='center', va='center', color=text_color, 
                    fontweight='bold'
                )

        self.ax.set_aspect('equal')
        self.ax.axis('off')

        #granice za gumice kad se crtaju da se ne prelazi mnogo levo desno gore dole od sestougla nego da se ide samo do odr velicine sestougla
        x_points = [r - (max_row - abs(q - (self.n + 1))) / 2 for q, r in self.tabla]
        y_points = [-(q - 1) for q, _ in self.tabla]
        
        margin = 0.5  # dodaj malo margine oko ivica
        self.ax.set_xlim(min(x_points) - margin, max(x_points) + margin)
        self.ax.set_ylim(min(y_points) - margin, max(y_points) + margin)


        self.update_status()

    def update_status(self):
        if not self.status_ax:
            self.status_ax = self.fig.add_axes([0.1, 0.9, 0.8, 0.05])  
        self.status_ax.clear()
        self.status_ax.text(
            0.5, 0.5, f"Igrač na potezu: {self.na_potezu}", fontsize=12, ha='center', va='center',
            color='white', fontweight='bold'
        )
        self.status_ax.text(
            0.1, 0.2, f"X={self.rezultat['X']}", fontsize=16, ha='left', va='center', color='#FFD700'
        )
        self.status_ax.text(
            0.9, 0.2, f"O={self.rezultat['O']}", fontsize=16, ha='right', va='center', color='#00FF7F'
        )
        
        self.status_ax.axis('off')

    def show_message(self, message):
        if not self.message_ax:
            self.message_ax = self.fig.add_axes([0.1, 0.05, 0.8, 0.05])  
        self.message_ax.clear()
        self.message_ax.text(0.5, 0.5, message, fontsize=12, ha='center', va='center', color='white')
        self.message_ax.axis('off')

    def onclick(self, event):
        if self.game_over:
            return

        if event.inaxes != self.ax:
            return
        
        if event.button == 3:
            self.onrightclick(event)
            return

        x, y = event.xdata, event.ydata
        max_row = max([q for q, _ in self.tabla])

        # nadji najblizu tacku na tabli
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
            # proveri validnost gumice
            if self.valid_gumica(self.selected_points[0], self.selected_points[1]):
                # obrni tuple ako je potrebno i dodaj gumicu
                start, end = self.selected_points
                if (end < start):  # obrni ako je krajnja tacka manja (znaci da se nije DL,DD,D nego GD, GL, L ali mi ga obrnemo i postane to i tako se cuva kao i sve druge)
                    start, end = end, start

                if self.presek_tacaka(start, end):  # ako je update-ovan presek tacaka znaci da se deo gumice "primio" i znaci da je gumica 100% validna (nije vec obuhvacena nekim drugim gumicama)
                    self.gumice.append((start, end))
                    
                    if self.temp_line:
                        self.temp_line.remove()
                        self.temp_line = None

                    if self.proveriKrajIgre():
                        self.game_over = True
                        if self.rezultat['X'] > self.rezultat['O']:
                            self.show_message('Pobedio je X')
                        elif self.rezultat['X'] < self.rezultat['O']:
                            self.show_message('Pobedio je O')
                        else:
                            self.show_message('Nereseno je')

                        #treba da prekinemo igru i da dodamo mogucnost za ponovno igranje
                        self.create_restart_button()
                    else:
                        self.show_message(f"Dodata gumica između tačaka {start} i {end}")
                   
                    self.switch_player()
                else:
                    self.show_message("Gumica već postoji ili je vec obuhvacena!")

            else:
                self.show_message("Nevalidna gumica!")

            self.selected_points.clear()

        self.update_display()

    def onmove(self, event):
        if len(self.selected_points) == 1 and event.inaxes == self.ax:
        
            if self.temp_line:
                self.temp_line.remove()
                self.temp_line = None

            max_row = max([q for q, _ in self.tabla])
            start = self.selected_points[0]
            start_x = start[1] - (max_row - abs(start[0] - (self.n + 1))) / 2
            start_y = -(start[0] - 1)

            self.temp_line = self.ax.plot([start_x, event.xdata], 
                                           [start_y, event.ydata], 
                                           '-', color='lightblue', linewidth=2)[0]
            self.fig.canvas.draw_idle()

    def onrightclick(self, event):
        # na desni klik brisemo tu zapocetu liniju
        if event.button == 3 and len(self.selected_points):  # ako je desni klik pritisnut a pre toga nije selektovano nista nema onda akcije nikakve
            self.selected_points.clear()
            if self.temp_line:
                self.temp_line.remove()
                self.temp_line = None
            self.fig.canvas.draw_idle()
            # self.show_message("Izbor tacaka otkazan")


    def presek_tacaka(self, start, end):
        q1, r1 = start
        q2, r2 = end
        presecitemp = self.preseci[:] #cuvamo trenutnu vrednost liste preseci da bismo posle videli da li je doslo do promene, ako nije to znaci da se sve duzi gumice vec nalaze u preseci i samim tim gumica nije validna
        promenjenipreseci = True
        # horizontalna gumica
        if q1 == q2:
            for r in range(r1, r2):
                duz = ((q1, r), (q1, r + 1))
                if duz not in self.preseci:
                    self.preseci.append(duz)
                    self.check_new_triangle(duz)

        # dijagonalne gumice 
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


        # horizontalna gumica (fiksna duzina 3)
        if (q1 == q2 and r2 == r1+3):
            return True

        # dijagonalna (fiksna duzina 3)
        if q2 == q1 + 3:
            if (q2 <= self.n+1 and (r2 == r1+3 or r2==r1)):
                return True
            elif (q1 >= self.n+1 and (r2==r1 or  r2 == r1-3)):
                return True
            elif (q1<(self.n+1) and q2>(self.n+1) and (r2 == r1+((self.n+1)-q1) or r2 == r1-(q2-(self.n+1)))):
                return True
           
        return False

    def check_new_triangle(self, new_edge):
       
        q1, r1 = new_edge[0]
        q2, r2 = new_edge[1]

        for edge in self.preseci:
            q3, r3 = edge[0]
            q4, r4 = edge[1]

            # proveri zajednicke tacke izmedju nove duzi i postojece
            common_points = set([(q1, r1), (q2, r2)]).intersection(set([(q3, r3), (q4, r4)]))
            if len(common_points) == 1:  # ako postoji tacno jedna zajednicka tacka
                shared_point = common_points.pop()

                # pronadji trecu tacku trougla 
                remaining_points = list(set([(q1, r1), (q2, r2), (q3, r3), (q4, r4)]) - {shared_point})
                if len(remaining_points) == 2:
                    # formiraj trecu duz i proveri da li postoji u preseku
                    third_edge = tuple(sorted(remaining_points))
                    if third_edge in self.preseci or third_edge[::-1] in self.preseci:
                        # formiraj trougao sa tri tacke
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
            return True  # pobedio je X ili O ili je nereseno
        # igra nije zavrsena
        return False

    def update_display(self):
        self.draw_table()
        self.fig.canvas.draw_idle()

    def start_game(self):
        print(self.fig.canvas)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.inicijalizuj_preseke()
        self.update_display()
        plt.show()

        # print('preseci', self.preseci)
        # print('trouglici', self.trouglici)
        


def show_main_menu():
    root = tk.Tk()
    root.title("Podešavanja igre")
    root.geometry("400x400")
    root.configure(bg="black")

    size_frame = tk.Frame(root, bg="black")
    size_frame.pack(pady=20)
    
    size_label = tk.Label(size_frame, text="Veličina table (n):", font=("Helvetica", 14), bg="black", fg="white")
    size_label.pack()
    
    size_var = tk.IntVar()
    size_var.set(3)  # Set default value
    size_entry = tk.Entry(size_frame, textvariable=size_var, font=("Helvetica", 12), width=5, justify='center')
    size_entry.pack(pady=5)

    # Player selection
    player_label = tk.Label(root, text="Prvi igrač:", font=("Helvetica", 16, "bold"), bg="black", fg="white")
    player_label.pack(pady=20)
  
    button_style = {
        "font": ("Helvetica", 18, "bold"),
        "bg": "#1E1E1E",
        "fg": "white",
        "activebackground": "#1E1E1E",
        "activeforeground": "white",
        "relief": "flat",
        "width": 10,
        "height": 1,
    }

    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(pady=20)

    button_x = tk.Button(button_frame, text="X", command=lambda: on_choice(root, 'X', size_var.get()), **button_style)
    button_x.pack(side=tk.LEFT, padx=20)

    button_o = tk.Button(button_frame, text="O", command=lambda: on_choice(root, 'O', size_var.get()), **button_style)
    button_o.pack(side=tk.LEFT, padx=20)

    root.mainloop()

def on_choice(root, choice, n):
    if n < 3:
        messagebox.showerror("Greška", "Veličina table mora biti najmanje 3")
        return
    elif n > 8:
        messagebox.showerror("Greška", "Veličina table mora biti najviše 8")
        return
        
    root.destroy()  

    

    igra = Triggle(n=n, na_potezu=choice)
    #odkomentarisi za blizu kraja igre (n=3) ->igra.gumice = [((1, 1), (4, 4)), ((1, 4), (4, 4)), ((3, 1), (3, 4)), ((1, 2), (4, 5)), ((2, 5), (5, 4)), ((4, 2), (4, 5)), ((2, 1), (5, 3)), ((2, 3), (5, 2)), ((5, 1), (5, 4)), ((3, 3), (6, 4)), ((3, 5), (6, 3)), ((1, 4), (4, 7)), ((1, 3), (4, 6)), ((3, 3), (3, 6)), ((1, 1), (1, 4)), ((1, 1), (4, 1)), ((2, 1), (2, 4)), ((1, 3), (4, 3)), ((6, 1), (6, 4)), ((3, 1), (6, 2)), ((4, 1), (7, 1)), ((4, 4), (7, 1)), ((2, 3), (5, 5)), ((3, 6), (6, 4)), ((4, 7), (7, 4)), ((1, 2), (4, 2)), ((2, 2), (2, 5)), ((5, 3), (5, 6)), ((4, 1), (4, 4))]
    igra.start_game() 


show_main_menu()




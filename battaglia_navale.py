import random

class Griglia:
    def __init__(self, dimensione=10):
        self.dimensione = dimensione
        self.griglia = [[' ' for _ in range(dimensione)] for _ in range(dimensione)]
        self.navi = []

    def stampa(self, nascondi_navi=False):
        print('   ' + ' '.join([str(i) for i in range(self.dimensione)]))
        for i in range(self.dimensione):
            riga = [self.griglia[i][j] if not nascondi_navi or self.griglia[i][j] not in ['N', 'X'] else ' '
                   for j in range(self.dimensione)]
            print(f'{i:2} {" ".join(riga)}')

    def posiziona_nave(self, lunghezza, x, y, orizzontale):
        if orizzontale:
            if y + lunghezza > self.dimensione:
                return False
            for i in range(lunghezza):
                if self.griglia[x][y+i] != ' ':
                    return False
            for i in range(lunghezza):
                self.griglia[x][y+i] = 'N'
        else:
            if x + lunghezza > self.dimensione:
                return False
            for i in range(lunghezza):
                if self.griglia[x+i][y] != ' ':
                    return False
            for i in range(lunghezza):
                self.griglia[x+i][y] = 'N'
        self.navi.append((x, y, lunghezza, orizzontale))
        return True

    def colpisci(self, x, y):
        if not (0 <= x < self.dimensione and 0 <= y < self.dimensione):
            return False
        if self.griglia[x][y] == 'N':
            self.griglia[x][y] = 'X'
            return True
        elif self.griglia[x][y] == ' ':
            self.griglia[x][y] = 'O'
            return False
        return False

    def tutte_navi_affondate(self):
        return not any('N' in riga for riga in self.griglia)

class Bot:
    def __init__(self, dimensione=10):
        self.dimensione = dimensione
        self.colpi_precedenti = set()

    def posiziona_navi(self, griglia):
        lunghezze_navi = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for lunghezza in lunghezze_navi:
            while True:
                x = random.randint(0, self.dimensione-1)
                y = random.randint(0, self.dimensione-1)
                orizzontale = random.choice([True, False])
                if griglia.posiziona_nave(lunghezza, x, y, orizzontale):
                    break

    def fai_mossa(self):
        while True:
            x = random.randint(0, self.dimensione-1)
            y = random.randint(0, self.dimensione-1)
            if (x, y) not in self.colpi_precedenti:
                self.colpi_precedenti.add((x, y))
                return x, y

def gioca_contro_bot():
    print("\nBattaglia Navale - Giocatore vs Bot")
    griglia_giocatore = Griglia()
    griglia_bot = Griglia()
    bot = Bot()

    # Posizionamento navi del bot
    bot.posiziona_navi(griglia_bot)

    # Posizionamento navi del giocatore
    print("\nPosiziona le tue navi:")
    lunghezze_navi = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for lunghezza in lunghezze_navi:
        while True:
            print(f"\nPosizionamento nave di lunghezza {lunghezza}:")
            griglia_giocatore.stampa()
            try:
                x = int(input("Inserisci riga (0-9): "))
                y = int(input("Inserisci colonna (0-9): "))
                orizzontale = input("Orizzontale? (s/n): ").lower() == 's'
                if griglia_giocatore.posiziona_nave(lunghezza, x, y, orizzontale):
                    break
                print("Posizione non valida. Riprova.")
            except ValueError:
                print("Input non valido. Inserisci numeri tra 0 e 9.")

    # Gioco
    while True:
        # Turno del giocatore
        print("\nLa tua griglia:")
        griglia_giocatore.stampa()
        print("\nGriglia del bot:")
        griglia_bot.stampa(nascondi_navi=True)

        while True:
            try:
                x = int(input("\nInserisci riga per colpire (0-9): "))
                y = int(input("Inserisci colonna per colpire (0-9): "))
                if griglia_bot.colpisci(x, y):
                    print("Colpito!")
                else:
                    print("Mancato!")
                break
            except ValueError:
                print("Input non valido. Inserisci numeri tra 0 e 9.")

        if griglia_bot.tutte_navi_affondate():
            print("\nComplimenti! Hai vinto!")
            break

        # Turno del bot
        x, y = bot.fai_mossa()
        print(f"\nIl bot colpisce ({x}, {y})")
        if griglia_giocatore.colpisci(x, y):
            print("Il bot ti ha colpito!")
        else:
            print("Il bot ha mancato!")

        if griglia_giocatore.tutte_navi_affondate():
            print("\nHai perso! Il bot ha vinto!")
            break

def gioca_multiplayer():
    print("\nBattaglia Navale - Giocatore vs Giocatore")
    griglia_giocatore1 = Griglia()
    griglia_giocatore2 = Griglia()

    # Posizionamento navi per entrambi i giocatori
    for giocatore in range(1, 3):
        print(f"\nGiocatore {giocatore}, posiziona le tue navi:")
        griglia = griglia_giocatore1 if giocatore == 1 else griglia_giocatore2
        lunghezze_navi = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

        for lunghezza in lunghezze_navi:
            while True:
                print(f"\nPosizionamento nave di lunghezza {lunghezza}:")
                griglia.stampa()
                try:
                    x = int(input("Inserisci riga (0-9): "))
                    y = int(input("Inserisci colonna (0-9): "))
                    orizzontale = input("Orizzontale? (s/n): ").lower() == 's'
                    if griglia.posiziona_nave(lunghezza, x, y, orizzontale):
                        break
                    print("Posizione non valida. Riprova.")
                except ValueError:
                    print("Input non valido. Inserisci numeri tra 0 e 9.")

        print("\n" * 50)  # Pulisce lo schermo

    # Gioco
    turno = 1
    while True:
        giocatore_attuale = (turno % 2) + 1
        griglia_attacco = griglia_giocatore2 if giocatore_attuale == 1 else griglia_giocatore1
        griglia_difesa = griglia_giocatore1 if giocatore_attuale == 1 else griglia_giocatore2

        print(f"\nTurno del Giocatore {giocatore_attuale}")
        print("\nLa tua griglia:")
        griglia_difesa.stampa()
        print("\nGriglia avversaria:")
        griglia_attacco.stampa(nascondi_navi=True)

        while True:
            try:
                x = int(input("\nInserisci riga per colpire (0-9): "))
                y = int(input("Inserisci colonna per colpire (0-9): "))
                if griglia_attacco.colpisci(x, y):
                    print("Colpito!")
                else:
                    print("Mancato!")
                break
            except ValueError:
                print("Input non valido. Inserisci numeri tra 0 e 9.")

        if griglia_attacco.tutte_navi_affondate():
            print(f"\nComplimenti Giocatore {giocatore_attuale}! Hai vinto!")
            break

        turno += 1
        input("\nPremi Enter per continuare...")
        print("\n" * 50)  # Pulisce lo schermo

def main():
    while True:
        print("\nBattaglia Navale")
        print("1. Gioca contro il Bot")
        print("2. Gioca in multiplayer")
        print("3. Esci")

        scelta = input("\nScegli un'opzione (1-3): ")

        if scelta == "1":
            gioca_contro_bot()
        elif scelta == "2":
            gioca_multiplayer()
        elif scelta == "3":
            print("\nGrazie per aver giocato! Arrivederci!")
            break
        else:
            print("\nScelta non valida. Riprova.")

if __name__ == "__main__":
    main()
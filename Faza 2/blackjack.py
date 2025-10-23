# Importy
import pygame
import random
 
# Stale globalne z parametrami okna i gry
OKNO_SZER = 800
OKNO_WYS = 600
FPS = 60

TŁO = (2, 125, 48)

# Inicjalizacja gry i zegara
pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Blackjack")
zegarek = pygame.time.Clock()

# Implementacja przycisków start, zasady, hit i stand
przycisk_start = pygame.image.load("start.jpg").convert_alpha()
przycisk_zasady = pygame.image.load("zasady.jpg").convert_alpha()
przycisk_hit = pygame.image.load("hit.jpg").convert_alpha()
przycisk_stand = pygame.image.load("stand.jpg").convert_alpha()

# Zasady gry - obrazek
zasady_gry = pygame.image.load("zasady_gry.jpg").convert_alpha()

# Implementacja przycisków
class przycisk():
    # Init
    def __init__(self, x, y, grafika, skalowanie):
        
        grubość = grafika.get_width() # Grubość
        wysokość = grafika.get_height() # Szerokość
        self.grafika = pygame.transform.scale(grafika, (int(grubość * skalowanie), int(wysokość * skalowanie))) # Skalowanie grafik, aby nie trzeba było za każdym razem zmieniać grafiki samej w sobie. Jeżeli nie będzie potrzeby, to można usunąć.
        self.rect = self.grafika.get_rect()
        self.rect.topleft = (x,y) # Ustalenie rozpoczęcia 'x' i 'y'
        self.naciśnięcie = False # Zmienna naciśnięcia myszki
    
    # Stworzenie graficzne przycisków + zbieranie naciśnięcia myszki
    def narysuj(self):
       
        akcja = False
        pozycja_myszki = pygame.mouse.get_pos()

        # Wykrycie naciśnięcia lewego przycisku myszy
        if ( self.rect.collidepoint(pozycja_myszki) ):
            if ( pygame.mouse.get_pressed()[0] == 1 and self.naciśnięcie == False ):
                self.naciśnięcie = True
                akcja = True         
        if ( pygame.mouse.get_pressed()[0]==0 ):
            self.naciśnięcie = False
        
        okienko.blit(self.grafika, (self.rect.x, self.rect.y))
        return akcja

# Dane grafik przycisków start, zasady, hit i stand
pokaż_przycisk_start = przycisk(350, 225, przycisk_start, 0.4)
pokaż_przycisk_zasady = przycisk(350, 325, przycisk_zasady, 0.4)
pokaż_przycisk_hit = przycisk(100,200,przycisk_hit,0.4)
pokaż_przycisk_stand = przycisk(400,200,przycisk_stand,0.4)

# Implementacja kart
class Karta:
    # Init
    def __init__(self, kolor, figura):
        # Wartości figur w słowniku, żeby można było je w razie czego łatwiej zmienić
        wartości_figur={'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'walet': 10, 'dama': 10, 'król': 10, 'as': 1}
        self.kolor=kolor # Kolor
        self.figura=figura # Figura (przy generowaniu talii jest ustawiona na string, więc nic się nie wysypie)
        self.wartość=wartości_figur[figura] # Wartość karty
        self.ścieżka_do_pliku='karty/'+figura+'-'+kolor+'.png' # Ścieżka do pliku w formacie figura-kolor.png

    # Możliwość wydrukowania tego, co znajduje się w karcie, być może do usunięcia po zakończeniu testowania
    def __str__(self):
        return f"({self.kolor}, {self.figura})"
    
    # metoda służąca do generowania obrazu karty
    def pokaż_kartę(self, x, y, skala):
        obraz_karty = pygame.image.load(self.ścieżka_do_pliku).convert_alpha()
        szerokość = obraz_karty.get_width() 
        wysokość = obraz_karty.get_height() 
        obraz_karty = pygame.transform.scale(obraz_karty, (int(szerokość * skala), int(wysokość * skala)))
        okienko.blit(obraz_karty, (x,y))
        
# Wygenerowanie pełnej talii kart
karty=[]

for i in range(52):
    kolory=['karo', 'kier', 'trefl', 'pik'] # lista kolorów
    figury=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'walet', 'dama', 'król', 'as'] # lista figur
    karty.append(Karta(kolory[i%4], figury[i//4])) # wygenerowanie ich po kolei

# Przemieszanie kart w talii, aby stos stał się losowy
random.shuffle(karty)

# Początkowa ilość kart na ręce. Będzie można resetować ilość do dwóch przy rozpoczęciu nowej rozgrywki
ilość_kart_na_ręce=2
# Suma wartości kart
#suma_wartości_kart = karty[0].wartość+karty[1].wartość

### Główny kod gry ###
graj = True

start_i_zasady = True # na początku pokazują się tylko przyciski start i zasady oraz AS KIER NIE WIEDZIEĆ DLACZEGO
hit_i_stand = False # hit i stand są ustawione na False, potem pojawią się na ekranie, po wybraniu odpowiedniej opcji
zasady = False

# Pozycje wyświetlania kart gracza
karta_gracz_wysokość=499
karta_gracz_szerokość=13
karta_gracz_odstęp=71

while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
 
    # Wypełnienie okienka kolorem tła
    okienko.fill(TŁO)

    #print(karty[0], karty[1])
    
     # Obsługa przycisku start i zasady
    if start_i_zasady:

        if pokaż_przycisk_start.narysuj():
            print("Po naciśnięciu przyciku start, pokazuje się ekran z hit i stand.")
            start_i_zasady = False
            hit_i_stand = True # pojawiają się przyciski hit i stand
        
        if pokaż_przycisk_zasady.narysuj():
            print("Tu pojawiaja się okno z zasadami gry.")
            start_i_zasady = False
            zasady = True

    # Zasady pojawiają się na ekranie
    if zasady:
        okienko.blit(zasady_gry, (250, 200))
    
    # Obsługa przycisku hit i stand
    if hit_i_stand:

        # Pokazanie pierwszych dwóch kart po rozpoczęciu gry. Tutaj potrzebne będą pozostałe grafiki kart, aby je poprawnie wywołać
        for i in range(ilość_kart_na_ręce):
            karty[i].pokaż_kartę(karta_gracz_szerokość+karta_gracz_odstęp*i,karta_gracz_wysokość,0.1)
        #karty[0].pokaż_kartę(karta_gracz_szerokość,karta_gracz_wysokość,0.1)
        #karty[1].pokaż_kartę(karta_gracz_szerokość+karta_gracz_odstęp,karta_gracz_wysokość,0.1)
        # Wygenerowanie przycisków hit i stand w grze
        if pokaż_przycisk_hit.narysuj():
                
        # Zwiększenie ilości kart na ręce o 1
            ilość_kart_na_ręce += 1
                
            # Pokazanie 3 karty
            #karty[ilość_kart_na_ręce-1].pokaż_kartę(karta_gracz_szerokość+karta_gracz_odstęp*(ilość_kart_na_ręce-1),karta_gracz_wysokość,0.1)
            print('W przypadku naciśnięcia hit, gracz dobierze jedną kartę')
            
            # Zsumowanie wartości kart na ręce
            suma_wartości_kart=0
            for i in range(ilość_kart_na_ręce):
                suma_wartości_kart+=karty[i].wartość
                print(karty[i])
            print(suma_wartości_kart)
                
            # Jeżeli wartość kart na ręce przekroczy 21, wyskoczy komunikat o przegranej
            if(suma_wartości_kart > 21):
                print('przegrałeś')
                    
            # Jeżeli wartość kart na ręce będzie równa 21, wyskoczy komunikat o wygranej + zakończenie aktualnej rozgrywki
            if(suma_wartości_kart == 21):
                print('wygrałeś')
                
        if pokaż_przycisk_stand.narysuj():
                
            # Tutaj wrzucimy cały ruch komputera + rozstrzygnięcie gry. Prawdopodobnie dodamy jakiś komunikat w stylu 'Wygrałeś', "Przegrałeś"
            print('działa przycisk stand. tutaj wkleimy koniec tury, rozpoczęcie tury komputera')
 
    # Aktualizacja klatek i zegara
    pygame.display.update()
    zegarek.tick(FPS)

### Główny kod gry – end ###

# Zamknięcie gry
pygame.quit()

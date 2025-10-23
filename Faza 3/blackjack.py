# Importy
import pygame
import random
import textwrap
 
# Stale globalne z parametrami okna i gry
OKNO_SZER = 800
OKNO_WYS = 600
FPS = 60
TŁO = (2, 125, 48)
KOLOR=(255,255,255)

# Inicjalizacja gry i zegara
pygame.init()
pygame.mixer.init() # obsługa dźwięku
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32) # Okno
pygame.display.set_caption("Blackjack") # Podpis w oknie
zegarek = pygame.time.Clock() # Zegar
font = pygame.font.SysFont('Arial', 64) # Główna czcionka
font2=pygame.font.SysFont('Arial', 20) # Mniejsza czcionka do zasad i copyrightu
font3=pygame.font.SysFont('Arial', 40) # Czcionka pośrednia do porady na ekranie gry

# Dźwięki
dźwięk_klik = pygame.mixer.Sound("pliki/klik.wav")
dźwięk_wygrana = pygame.mixer.Sound("pliki/wygrana.wav")
dźwięk_przegrana = pygame.mixer.Sound("pliki/przegrana.wav")

# Logo gry
logo = pygame.image.load("pliki/logo.png").convert_alpha()

# Klasa przycisków
class Przycisk():
    # Init
    def __init__(self, x: int, y: int, grafika, skalowanie: int):
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
                dźwięk_klik.play() # Dźwięk kliknięcia
        if ( pygame.mouse.get_pressed()[0]==0 ):
            self.naciśnięcie = False
        
        okienko.blit(self.grafika, (self.rect.x, self.rect.y))
        return akcja
    
# Załadowanie obrazów przycisków
przycisk_start = pygame.image.load("pliki/graj.png").convert_alpha()
przycisk_zasady = pygame.image.load("pliki/zasady.png").convert_alpha()
przycisk_hit = pygame.image.load("pliki/hit.png").convert_alpha()
przycisk_stand = pygame.image.load("pliki/stand.png").convert_alpha()
przycisk_menu = pygame.image.load("pliki/menu.png").convert_alpha()
przycisk_nowa_gra = pygame.image.load("pliki/nowa-gra.png").convert_alpha()

# Utworzenie obiektów przycisków
pokaż_przycisk_start = Przycisk(250, 300, przycisk_start, 1)
pokaż_przycisk_zasady = Przycisk(250, 420, przycisk_zasady, 1)
pokaż_przycisk_hit = Przycisk(200,200,przycisk_hit,0.5)
pokaż_przycisk_stand = Przycisk(450,200,przycisk_stand,0.5)
pokaż_przycisk_menu = Przycisk(200,300,przycisk_menu,0.5)
pokaż_przycisk_nowa_gra = Przycisk(450,300,przycisk_nowa_gra,0.5)
pokaż_przycisk_menu_z = Przycisk(200,500,przycisk_menu,0.5)
pokaż_przycisk_graj_z = Przycisk(450,500,przycisk_start,0.5)

# Klasa kart
class Karta:
    # Init
    def __init__(self, kolor: str, figura: str):
        # Wartości figur w słowniku, żeby można było je w razie czego łatwiej zmienić
        wartości_figur={'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'walet': 10, 'dama': 10, 'król': 10, 'as': 1}
        self.kolor=kolor # Kolor
        self.figura=figura # Figura (przy generowaniu talii jest ustawiona na string, więc nic się nie wysypie)
        self.wartość=wartości_figur[figura] # Wartość karty
        self.ścieżka_do_pliku='karty/'+figura+'-'+kolor+'.png' # Ścieżka do pliku w formacie figura-kolor.png, w osobnym folderze karty
    
    # metoda służąca do generowania obrazu karty
    def pokaż_kartę(self, x: int, y: int, skala: int):
        obraz_karty = pygame.image.load(self.ścieżka_do_pliku).convert_alpha()
        szerokość = obraz_karty.get_width() 
        wysokość = obraz_karty.get_height() 
        obraz_karty = pygame.transform.scale(obraz_karty, (int(szerokość * skala), int(wysokość * skala)))
        okienko.blit(obraz_karty, (x,y))
        
# Wygenerowanie pełnej talii kart
karty=[]

kolory=['karo', 'kier', 'trefl', 'pik'] # lista kolorów
figury=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'walet', 'dama', 'król', 'as'] # lista figur

for i in range(52):
    karty.append(Karta(kolory[i%4], figury[i//4])) # wygenerowanie ich po kolei

# Przemieszanie kart w talii, aby stos stał się losowy
random.shuffle(karty)

# Początkowa liczba kart na ręce. Będzie można resetować ilość do dwóch przy rozpoczęciu nowej rozgrywki
liczba_kart_na_ręce=2
liczba_kart_komputera=0

# Sumowanie wartości kart użytkownika i komputera
punkty_użytkownika=karty[0].wartość+karty[1].wartość
punkty_komputera=0

# Pozycje wyświetlania kart gracza i komputera
karta_szerokość=13
karta_odstęp=71
karta_gracz_wysokość=499
karta_komputer_wysokość=13

# Funkcje pomocnicze
# Funckja dla wyświetlania punktów i rysowania kart użytkownika
def wyświetl_punkty_i_karty_użytkownika():
    tekst=font3.render(str('Twoje punkty: ') + str(punkty_użytkownika),True,KOLOR)
    okienko.blit(tekst, (10,karta_gracz_wysokość-10-tekst.get_rect().height))
    for i in range(liczba_kart_na_ręce):
        karty[i].pokaż_kartę(karta_szerokość+karta_odstęp*i,karta_gracz_wysokość,0.1)

# Funkcja do renderowania wieloliniowego tekstu
def render_text(tekst, font, KOLOR, max_width):
    linie = tekst.split('\n')  # Dzielimy tekst na linie w miejscu występowania '\n'
    rendered_linie = []
    for linia in linie:
        wrapped_linie = textwrap.wrap(linia, max_width)
        rendered_linie.extend([font.render(wrapped_line, True, KOLOR) for wrapped_line in wrapped_linie])
    return rendered_linie

# Zmienne sterujące rezultatem gry
graj = True # Przycisk sprawdzający, czy nie opuszczono gry
zagrany_dźwięk = False # sprawdza, czy został zagrany dźwięk przy ostatecznym rezultacie gry
stan="start_i_zasady" # Stan gry. Dostępne wartości: start_i_zasady, zasady, hit_i_stand, tura_komputera, koniec_gry
wynik="brak" # Wyniki gry

# Funkcja do generowania losowego koloru
def losowy_kolor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

# Klasa Kwadracików z ktorych składają sie fajerwerki
class Fajerwerki_kwadracik(pygame.sprite.Sprite):
    def __init__(self,x: int,y: int):
        super().__init__()
        self.image=pygame.Surface((4,4))
        self.image.fill(losowy_kolor())  # Kolorowy kwadracik
        self.rect=self.image.get_rect(center=(x,y))
        self.predkosc=[random.uniform(-4,4), random.uniform(-4,4)]
        self.czas_zycia=30  # Czas życia kwadracika

    def update(self):
        self.czas_zycia-=1
        if self.czas_zycia<=0:
            self.kill()  # Usuwa kwadracik
        self.rect.x+=self.predkosc[0]
        self.rect.y+=self.predkosc[1]

# Klasa fajerwerkow
class Fajerwerki(pygame.sprite.Sprite):
    def __init__(self,x: int,y: int):
        super().__init__()
        self.kwadraciki=pygame.sprite.Group()
        for _ in range(200):  # 200kwadracikow na fajerwerk
            self.kwadraciki.add(Fajerwerki_kwadracik(x,y))

    def update(self):
        self.kwadraciki.update()

    def rysuj(self, powierzchnia):
        self.kwadraciki.draw(powierzchnia)

fajerwerki = pygame.sprite.Group()

### Główny kod gry ###
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
 
    # Wypełnienie okienka kolorem tła
    okienko.fill(TŁO)
    
    # Obsługa przycisku start i zasady
    if stan=="start_i_zasady":
        # Pokazanie loga
        okienko.blit(logo, (0,0))

        # Pokazanie autorów na dole ekranu startowego
        copyright=font2.render('© Justyna Bladowska, Daria Grzelak, Wiktoria Jarząb, Dominika Szulc 2024',True,KOLOR)
        okienko.blit(copyright, ((OKNO_SZER//2)-(copyright.get_rect().width//2), OKNO_WYS-10-(copyright.get_rect().height)))

        # Obsługa przycisków start i zasady
        if pokaż_przycisk_start.narysuj() or (zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_g):
            stan="hit_i_stand"  # pojawiają się przyciski hit i stand
        
        if pokaż_przycisk_zasady.narysuj() or (zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_z):
            stan="zasady"

    # Zasady pojawiają się na ekranie
    elif stan=="zasady":
        # Tekst, który będzie wyświetlany. v_1 wersji tekstu.
        tekst=('Celem gry jest uzbieranie 21 punktów. Każda karta posiada określoną wartość punktową: as – 1 pkt, 2–10 – 2–10 pkt, walet – król – 10 pkt. Na początku gracz dostaje 2 karty. Następnie może nacisnąć jeden z 2 przycisków: HIT i STAND. Po naciśnięciu HIT, gracz dobiera kolejną kartę. Po naciśnięciu STAND, tura gracza kończy się. Zaczyna się tura komputera, w której to on dobiera karty. Gra zakończyć się może w jeden z następujących sposobów: \n'
                '1) Gracz uzbiera równo 21 pkt = wygrana. \n'
                '2) Gracz uzbiera ponad 21 pkt = przegrana. \n'
                '3) Gracz uzbiera mniej niż 21 pkt i mniej pkt niż komputer = przegrana. \n'
                '4) Gracz uzbiera mniej niż 21 pkt, a komputer powyżej 21pkt = wygrana. \n'
                '5) Gracz i komputer uzbierają dokładnie taką samą liczbę punktów = remis. \n'
                'Do nawigacji po grze użyj znajdujących się w niej przycisków. Możesz również skorzystać z klawiatury, klikając klawisze zgodne z pierwszymi literami wybranych przycisków (m = menu, g = graj, h = hit, s = stand).')

        # Renderowanie tekstu z ograniczeniem szerokości 
        rendered_tekst = render_text(tekst, font2, KOLOR, 80)

        # Wyświetlanie każdej linii tekstu
        y = OKNO_WYS*0.05
        linia_wysokość = font2.get_height()*1.25
        for line in rendered_tekst:
            okienko.blit(line, (OKNO_SZER*0.05, y))
            y += linia_wysokość
     
        # Powrót do menu głownego po naciśnięciu przycisku 'm'
        if pokaż_przycisk_menu_z.narysuj() or zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_m:
                stan="start_i_zasady"

        if pokaż_przycisk_graj_z.narysuj() or zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_g:
                stan="hit_i_stand"
    
    # Obsługa przycisku hit i stand
    elif stan=="hit_i_stand":

        porada=font3.render('Dobierz kartę (hit) lub zakończ turę (stand):',True,KOLOR)
        okienko.blit(porada, ((OKNO_SZER//2)-(porada.get_rect().width//2),20))

        # Pokazanie liczby punktów na ręce i kart użytkownika
        wyświetl_punkty_i_karty_użytkownika()
         
        # Wygenerowanie przycisków hit i stand w grze
        if pokaż_przycisk_hit.narysuj() or (zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_h):
                
        # Zwiększenie ilości kart na ręce o 1
            liczba_kart_na_ręce += 1
            
            # Zsumowanie wartości kart na ręce
            punkty_użytkownika=0
            for i in range(liczba_kart_na_ręce):
                punkty_użytkownika+=karty[i].wartość
                
            # Jeżeli wartość kart na ręce przekroczy 21, przegrana + przejście do końca gry
            if(punkty_użytkownika > 21):
                wynik="przegrana"
                stan="koniec_gry"
                    
            # Jeżeli wartość kart na ręce będzie równa 21, wygrana + przejście do końca gry 
            elif(punkty_użytkownika == 21):
                wynik="wygrana"
                stan="koniec_gry"
             
        # Przejście do tury komputera
        if pokaż_przycisk_stand.narysuj() or (zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_s):
            stan="tura_komputera"

    # Tura komputera
    elif stan=="tura_komputera":
        # Pętla zliczająca punkty komputera
        punkty_komputera=0
        liczba_kart_komputera=liczba_kart_na_ręce
        j=0
          
        while punkty_komputera < punkty_użytkownika:
            punkty_komputera+=karty[liczba_kart_komputera].wartość
            liczba_kart_komputera=liczba_kart_komputera+1

        # Sprawdzenie wyniku gry
        if punkty_komputera==punkty_użytkownika:
            wynik="remis"
        elif punkty_komputera<=21:
            wynik="przegrana"
        else:
            wynik="wygrana"
        
        # Przejście do końca gry
        stan="koniec_gry"

    # Implementacja końca gry
    elif stan=="koniec_gry":

        if wynik=="wygrana":
            # Dodaj fajerwerki po wygranej
            for _ in range(3):  # Tworzenie 3 fajerwerków
                x = random.randint(0, 800)
                y = random.randint(0, 800)
                fajerwerek = Fajerwerki(x, y)
                fajerwerki.add(fajerwerek)

        if wynik=="wygrana":
            # Aktualizacja i rysowanie fajerwerków
            fajerwerki.update()
            for fajerwerek in fajerwerki:
                fajerwerek.rysuj(okienko)
     
        # Pokazanie liczby punktów na ręce gracza i ewentualnie komputera praz ponowne narysowanie kart
        wyświetl_punkty_i_karty_użytkownika()

        if punkty_komputera>0:
            tekst=font3.render(str('Punkty komputera: ') + str(punkty_komputera),True,KOLOR)
            okienko.blit(tekst, (10,13+88+10))
            j=0
            for i in range(liczba_kart_na_ręce,liczba_kart_komputera):
                karty[i].pokaż_kartę(karta_szerokość+karta_odstęp*j,karta_komputer_wysokość,0.1)
                j=j+1

        # Renderowanie odpowiedniego tekstu w zależności od wyniku
        if wynik=="wygrana":
            if not zagrany_dźwięk:
                dźwięk_wygrana.play(-1)
                zagrany_dźwięk=True
            tekst=font.render('Wygrana!',True,KOLOR)

        elif wynik=="przegrana":
            if not zagrany_dźwięk:
                dźwięk_przegrana.play(-1)
                zagrany_dźwięk=True
            tekst=font.render('Przegrana!',True,KOLOR)

        elif wynik=="remis":
            if not zagrany_dźwięk:
                dźwięk_wygrana.play(-1)
                zagrany_dźwięk=True
            tekst=font.render('Remis!',True,KOLOR)

        # Wygenerowanie tekstu informującego o wyniku
        okienko.blit(tekst, ((OKNO_SZER//2)-(tekst.get_rect().width//2), (OKNO_WYS//2.5)-(tekst.get_rect().height//2)))

        if pokaż_przycisk_menu.narysuj() or (zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_m):
            # wyłączenie dźwięku informującego o wyniku
            if zagrany_dźwięk:
                if wynik == "wygrana" or wynik == "remis":
                    dźwięk_wygrana.stop()
                elif wynik == "przegrana":
                    dźwięk_przegrana.stop()
                zagrany_dźwięk = False
            random.shuffle(karty)
            punkty_użytkownika=karty[0].wartość+karty[1].wartość
            liczba_kart_na_ręce=2
            liczba_kart_komputera=0
            punkty_komputera = 0
            wynik="brak"
            stan="start_i_zasady"

        if pokaż_przycisk_nowa_gra.narysuj() or (zdarzenie.type == pygame.KEYUP and zdarzenie.key == pygame.K_g):
            # wyłączenie dźwięku informującego o wyniku
            if zagrany_dźwięk:
                if wynik == "wygrana" or wynik == "remis":
                    dźwięk_wygrana.stop()
                elif wynik == "przegrana":
                    dźwięk_przegrana.stop()
                zagrany_dźwięk = False
            random.shuffle(karty)
            punkty_użytkownika=karty[0].wartość+karty[1].wartość
            liczba_kart_na_ręce=2
            liczba_kart_komputera=0
            punkty_komputera = 0
            wynik="brak"
            stan="hit_i_stand"
 
    # Aktualizacja klatek i zegara
    pygame.display.update()
    zegarek.tick(FPS)

### Główny kod gry – end ###

# Zamknięcie gry
pygame.quit()

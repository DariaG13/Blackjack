import pygame

OKNO_SZER = 800
OKNO_WYS = 600
FPS = 60

TŁO = (2, 125, 48)

# Inicjalizacja gry i zegara
pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Blackjack")
zegarek = pygame.time.Clock()

## Menu startu ##

# pygame.Rect(odległość od lewej krawędzi na szerokość, odległość od górnego lewego rogu na wysokość, szerokość obiektu, wysokość obiektu)
przycisk_start = pygame.image.load("start.jpg").convert_alpha()
przycisk_zasady = pygame.image.load("zasady.jpg").convert_alpha()

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

# Pokazanie przycisków - trzeba to wrzuć przed przyciski stand i hit, wciśnięcie start powoduje pojawienie się okienka z grą
pokaż_przycisk_start = przycisk(350, 225, przycisk_start, 0.4)
pokaż_przycisk_zasady = przycisk(350, 325, przycisk_zasady, 0.4)


graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
 
    # Wypełnienie okienka kolorem tła
    okienko.fill(TŁO)

    if pokaż_przycisk_start.narysuj():
        print("Po naciśnięciu przyciku start, pokazuje się ekran z hit i stand.")

    if pokaż_przycisk_zasady.narysuj():
        print("Tu pojawiaja się okno z zasadami gry.")

    pygame.display.update()
    zegarek.tick(FPS)
pygame.quit()
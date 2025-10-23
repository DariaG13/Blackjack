import pygame
 
OKNO_SZER = 800
OKNO_WYS = 600
FPS = 60

TŁO = (2, 125, 48)
 
pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Blackjack")
zegarek = pygame.time.Clock()

przycisk_hit = pygame.image.load("hit.jpg").convert_alpha()
przycisk_stand = pygame.image.load("stand.jpg").convert_alpha()

class przycisk():
    def __init__(self, x, y, grafika, skalowanie):
        
        grubość = grafika.get_width() 
        wysokość = grafika.get_height() 
        self.grafika = pygame.transform.scale(grafika, (int(grubość * skalowanie), int(wysokość * skalowanie)))
        self.rect = self.grafika.get_rect()
        self.rect.topleft = (x,y)
        self.naciśnięcie = False
        
    def narysuj(self):
        
        akcja = False
        pozycja_myszki = pygame.mouse.get_pos()
        
        if ( self.rect.collidepoint(pozycja_myszki) ):
            if ( pygame.mouse.get_pressed()[0] == 1 and self.naciśnięcie == False ):
                self.naciśnięcie = True
                akcja = True         
        if ( pygame.mouse.get_pressed()[0]==0 ):
            self.naciśnięcie = False
        
        okienko.blit(self.grafika, (self.rect.x, self.rect.y))
        return akcja
        
pokaż_przycisk_hit = przycisk(100,200,przycisk_hit,0.4)
pokaż_przycisk_stand = przycisk(400,200,przycisk_stand,0.4)

graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
 
    okienko.fill(TŁO)
    
    if ( pokaż_przycisk_hit.narysuj() == True):
        print('działa przycisk hit. tutaj wkleimy dobieranie kart')
    if ( pokaż_przycisk_stand.narysuj() == True):
        print('działa przycisk stand. tutaj wkleimy koniec tury, rozpoczęcie tury komputera')
 
    pygame.display.update()
    zegarek.tick(FPS)

pygame.quit()

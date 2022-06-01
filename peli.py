import pygame
from math import pow, sqrt
from random import randint
 
class Main():

    def __init__(self):
 
        pygame.init()
 
        pygame.display.set_caption("Kerää kolikot")
 
        self.fontti_pieni = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.fontti_suuri = pygame.font.SysFont("Segoe UI", 50, bold=True)

        self.leveys, self.korkeus = 640, 480
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.kello = pygame.time.Clock()
 
        self.lataa_kuvat()
        self.luo_objektit()
        self.luoti()
 
        self.sijainti_x, self.sijainti_y = self.leveys / 2 - self.kuvat[0].get_width() / 2, self.korkeus - self.kuvat[0].get_height()
 
        self.vasemmalle = False
        self.oikealle = False
        self.putoamisnopeus = 1
        self.pisteet = 0
        self.ammukset = 0

        self.laser_aani = pygame.mixer.Sound("laser.mp3")
        self.kolikko_aani = pygame.mixer.Sound("coin.mp3.wav")
 
        self.silmukka()
 
    def lataa_kuvat(self):

        self.kuvat = []
        for kuva in ["pelaaja.png", "vihollinen.png", "bitcoin.png"]:
            self.kuvat.append(pygame.image.load(kuva))
 
    def tapahtumat(self):

        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_ESCAPE:
                    self.lopetusnaytto()      
                if tapahtuma.key == pygame.K_SPACE:
                    if self.lataa == False and self.ammukset >= 1:
                        self.luoti_x = self.sijainti_x
                        self.luoti_y = self.sijainti_y
                        self.ammu_luoti(self.luoti_x, self.luoti_y)
                        if self.ammukset >= 1:
                            self.ammukset -= 1
                            self.laser_aani.play()
 
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
 
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                if self.lataa == False and self.ammukset >= 1:
                    self.luoti_x = self.sijainti_x
                    self.luoti_y = self.sijainti_y
                    self.ammu_luoti(self.luoti_x, self.luoti_y)
                    if self.ammukset >= 1:
                        self.ammukset -= 1
                        self.laser_aani.play()
   
            if tapahtuma.type == pygame.QUIT:
                self.lopetusnaytto()
 
    def robotti_liike(self):

        if self.oikealle and self.sijainti_x + self.kuvat[0].get_width() <= self.leveys:
            self.sijainti_x += 5
        if self.vasemmalle and self.sijainti_x >= 0:
            self.sijainti_x -= 5
 
    def luoti(self):

        self.luoti_x = 0
        self.luoti_y = 480
        self.luoti_y_nopeus = 5
        self.lataa = False
 
    def ammu_luoti(self, x, y):

        self.lataa = True
        pygame.draw.rect(self.naytto, (255, 0, 0), (x + self.kuvat[0].get_width() / 2, y + 10, 4, 20))
    
    def osuma(self, sijainti_x, sijainti_y, luoti_x, luoti_y):

        etaisyys = sqrt((pow(sijainti_x - luoti_x, 2)) + (pow(sijainti_y - luoti_y, 2)))
        if etaisyys < 27:
            return True
        else:
            return False
 
    def luo_objektit(self):

        self.hirviot = []
        self.kolikot = [] 
 
        for i in range(10):
            hirvio_x, hirvio_y = randint(0, 640 - self.kuvat[1].get_width()), randint(- 1500, - 100) 
            self.hirviot.append([hirvio_x, hirvio_y])
 
        for j in range(5):
            kolikko_x, kolikko_y = randint(0, 640 - self.kuvat[2].get_width()), randint(- 1500, - 100)
            self.kolikot.append([kolikko_x, kolikko_y])
 
    def spawnaa_hirviot(self):

        for hirvio in self.hirviot:
            tormays = self.osuma(hirvio[0], hirvio[1], self.luoti_x, self.luoti_y)
            if tormays:
                self.luoti_y = 400
                self.lataa = False
                hirvio[0], hirvio[1] = randint(0, 640 - self.kuvat[1].get_width()), randint(- 1500, - 100)
 
            robo_rect = self.kuvat[0].get_rect(center = (self.sijainti_x, self.sijainti_y))
            if robo_rect.collidepoint(hirvio[0], hirvio[1]):
                self.lopetusnaytto()
 
            if hirvio[1] + self.kuvat[1].get_height() >= 480 + self.kuvat[1].get_height():
                hirvio[0], hirvio[1] = randint(0, 640 - self.kuvat[1].get_width()), randint(- 1500, - 100)
 
            hirvio[1] += self.putoamisnopeus
 
            self.naytto.blit(self.kuvat[1], (hirvio[0], hirvio[1]))
 
    def spawnaa_kolikot(self):

        for kolikko in self.kolikot:
            robo_rect = self.kuvat[0].get_rect(center = (self.sijainti_x, self.sijainti_y))
            if robo_rect.collidepoint(kolikko[0], kolikko[1]):
                kolikko[0], kolikko[1] = randint(0, 640 - self.kuvat[2].get_width()), randint(- 1500, - 100)
                self.pisteet += 1
                self.ammukset += 1
                self.kolikko_aani.play()
 
            if kolikko[1] + self.kuvat[2].get_height() >= 480:
                self.lopetusnaytto()
 
            if kolikko[1] + self.kuvat[2].get_height() <= 480:
                kolikko[1] += self.putoamisnopeus
 
            self.naytto.blit(self.kuvat[2], (kolikko[0], kolikko[1]))
 
    def lopetusnaytto(self):
        pisteet = self.fontti_suuri.render("Kerätyt kolikot: " + str(self.pisteet), True, (255, 255, 255))
        paras_tulos = self.fontti_suuri.render("Paras tulos: " + str(self.tiedosto()), True, (255, 255, 255))
        pelaa_uudestaan_valkoinen = self.fontti_suuri.render("Pelaa uudestaan", True, (255, 255, 255))
        pelaa_uudestaan_musta = self.fontti_suuri.render("Pelaa uudestaan", True, (0, 0, 0))

        teksti = pelaa_uudestaan_valkoinen.get_rect(center = (self.leveys / 2, self.korkeus / 1.6))
    
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()

                if tapahtuma.type == pygame.MOUSEBUTTONDOWN and teksti.collidepoint(pygame.mouse.get_pos()):
                    Main()

                if tapahtuma.type == pygame.QUIT:
                    exit()

            self.naytto.fill((105, 105, 105))
        
            self.naytto.blit(pisteet, (self.leveys / 2 - pisteet.get_width() / 2, self.korkeus / 2 - pisteet.get_height()))
            self.naytto.blit(paras_tulos, (self.leveys / 2 - paras_tulos.get_width() / 2, self.korkeus / 3 - pisteet.get_height()))

            if teksti.collidepoint(pygame.mouse.get_pos()):
                self.naytto.blit(pelaa_uudestaan_musta, (self.leveys / 2 - pelaa_uudestaan_musta.get_width() / 2, self.korkeus / 1.5 - pelaa_uudestaan_musta.get_height()))
            else:
                self.naytto.blit(pelaa_uudestaan_valkoinen, (self.leveys / 2 - pelaa_uudestaan_valkoinen.get_width() / 2, self.korkeus / 1.5 - pelaa_uudestaan_valkoinen.get_height()))

            pygame.display.flip()

            self.kello.tick()

    def tiedosto(self):

        f = open("pisteet.txt", "r")
        tiedosto = f.readlines()
        viimeinen = int(tiedosto[0])

        if viimeinen < int(self.pisteet):
            f.close()
            tiedosto = open("pisteet.txt", "w")
            tiedosto.write(str(self.pisteet))
            tiedosto.close()

            return self.pisteet

        return viimeinen
       
    def silmukka(self):

        while True:
            self.tapahtumat()
            self.piirra_naytto()
 
    def piirra_naytto(self):
 
        pisteet = self.fontti_pieni.render("Kolikot: " + str(self.pisteet), True, (255, 255, 255))
        ammukset = self.fontti_pieni.render("Ammukset: " + str(self.ammukset), True, (255, 255, 255))
 
        self.naytto.fill((105, 105, 105))
 
        self.robotti_liike()
 
        self.naytto.blit(self.kuvat[0], (self.sijainti_x, self.sijainti_y))
        self.naytto.blit(pisteet, ((self.leveys - 30) - pisteet.get_width(), 0))
        self.naytto.blit(ammukset, ((self.leveys - 30) - ammukset.get_width(), ammukset.get_height()))
        
        if self.luoti_y <= 0:
            self.luoti_y = 480
            self.lataa = False
 
        if self.lataa == True:
            self.ammu_luoti(self.luoti_x - 2, self.luoti_y - 23)
            self.luoti_y -= self.luoti_y_nopeus
 
        self.spawnaa_hirviot()
        self.spawnaa_kolikot()
 
        pygame.display.flip()
 
        self.kello.tick(60)
 
if __name__ == "__main__":

    Main()


import os, sys
import pygame
import time

class endScreen(pygame.sprite.Sprite):
    def __init__(self, game, settings,camera, clock):
        self.game = game
        self.settings = settings
        self.camera = camera
        self.clockFPS = clock

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()
        self.__updateText()
        self.__gameLoop()

    def __loadVariables(self):
        self.gameOverTextColor = self.settings.gameOverTextColor
        self.numCurrentImage = 0
        self.startChangeImage = time.time()
        self.endChangeImage = time.time()

    def __loadImages(self):
        self.__images = []
        for i in range(1,60):
            tempImage = self.settings.load_Images("dog"+str(i)+".png", "Screen/End")
            self.__images.append(tempImage)

        self.__currentImage = self.__images[0]

    def __updateText(self):
        self.textGameOver = self.settings.fontGeneral.font.render("GameOver", 1, self.gameOverTextColor)
        self.textGameOver2 = self.settings.fontGeneral.font.render("Press Enter", 1, self.gameOverTextColor)

    def __gameLoop(self):
        while self.game.gameOver:
            self.__draw()                    #Desenha os objetos na tela
            self.__updateImage()
            self.__checkEvents()             #Verifica se houve algum evento
            self.__update()                  #Atualiza os objetos na tela
            self.clockFPS.tick(60)           #FPS counter

    def __updateImage(self):
        self.endChangeImage = time.time()
        if self.endChangeImage - self.startChangeImage >= 0.07:
            self.startChangeImage = time.time()
            self.__setProxImage()

    def __setProxImage(self):
        if self.numCurrentImage == 58:
            self.__currentImage = self.__images[0]
            self.numCurrentImage = 0
        else:
            self.__currentImage = self.__images[self.numCurrentImage+1]
            self.numCurrentImage +=1

    def __draw(self):
        self.__blitAndResetScreen()
        self.camera.drawScreenFix(self.__currentImage, (self.settings.screen_width/2 - self.__currentImage.get_rect().w/2,self.settings.screen_height/2 - self.__currentImage.get_rect().h/2))
        self.camera.drawScreenFix(self.textGameOver,(self.settings.screen_width/2 - 100,self.settings.screen_height/2 - self.__currentImage.get_rect().h/2 - self.textGameOver.get_rect().h))
        self.camera.drawScreenFix(self.textGameOver2,(self.settings.screen_width/2 + 20,self.settings.screen_height/2 - self.__currentImage.get_rect().h/2 - self.textGameOver.get_rect().h))

    def __blitAndResetScreen(self):
        self.camera.drawScreenEnd()

    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.game.gameOver = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def __update(self):
        self.__updateText()
        pygame.display.update()
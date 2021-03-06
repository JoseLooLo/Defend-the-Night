import os, sys
import pygame
import time
from src.colision import Colision
from src.weapon import Weapon

class Player(pygame.sprite.Sprite):

	def __init__(self, settings, camera, playerID):
		pygame.sprite.Sprite.__init__(self)
		self.settings = settings
		self.playerID = playerID
		self.camera = camera
		self.weaponAtual = Weapon(self.settings, self, 0)

		self.__init()

	def __init(self):
		self.__loadVariables()
		self.__loadImages()

	def __loadVariables(self):
		#Variaveis de controle dos Frames
		self.qntImagePlayerWalk = self.settings.getPlayerQntImagesWalk(self.playerID)
		self.qntImagePlayerStop = self.settings.getPlayerQntImagesStop(self.playerID)
		self.qntImagePlayerAttack = self.settings.getPlayerQntImagesAttack(self.playerID)
		self.qntImagePlayerJump = self.settings.getPlayerQntImagesJump(self.playerID)
		self.numCurrentImagePlayer = 0
		self.velocityImagePlayer = self.settings.getPlayerVelocityImages(self.playerID)
		self.velocityImagePlayerAttack = self.settings.getPlayerVelocityImagesAttack(self.playerID)

		#Variaveis de Status
		self.playerDamage = self.settings.getPlayerStatusDamage(self.playerID)
		self.playerVelocity = self.settings.getPlayerStatusVelocity(self.playerID)
		self.playerLife = self.settings.getPlayerStatusLife(self.playerID)
		self.playerMoney = self.settings.getPlayerStatusMoney(self.playerID)
		self.playerImunityTime = self.settings.getPlayerStatusImunityTime(self.playerID)
		self.countImunityTime = 0

		#Jump
		self.playerVelocityJump = self.settings.getPlayerStatusVelocityJump(self.playerID)
		self.playerHeightJump = self.settings.getPlayerStatusHeightJump(self.playerID)
		self.playerStatusDefaultJumpTime = self.settings.playerStatusDefaultJumpTime
		self.countInJumpUp = self.playerHeightJump    #Contador para a subida no pulo
		self.countInJumpDown = 0                      #Contador para a descida do pulo
		self.countJumpPlayer = 0
		self.countAirJumpPlayer = 0

		#Variaveis de controle
		self.inMoving = False
		self.inJump = False
		self.inAirJump = False
		self.inDamage = False                  #Verifica se está dentro do tempo de invulnerabilidade 
		self.inAtack = False
		self.colisionRight = False
		self.colisionLeft = False
		self.posXMouseInScreenIsRightSide = False
		self.startMoviment = False

		#Time
		self.startChangeImage = time.time()
		self.endChangeImage = time.time()

	def __loadImages(self):
		self.__imagePlayerWalk = []
		for i in range(self.qntImagePlayerWalk):
			tempImage = self.settings.load_Images("walking"+str(i)+".png", "Player/ID"+str(self.playerID), -1)
			self.__imagePlayerWalk.append(tempImage)

		self.__imagePlayerStop = []
		for i in range(self.qntImagePlayerStop):
			tempImage = self.settings.load_Images("stopped"+str(i)+".png", "Player/ID"+str(self.playerID), -1)
			self.__imagePlayerStop.append(tempImage)

		self.__imagePlayerAttack = []
		for i in range(self.qntImagePlayerAttack):
			tempImage = self.settings.load_Images("attack"+str(i)+".png", "Player/ID"+str(self.playerID), -1)
			self.__imagePlayerAttack.append(tempImage)

		self.__imagePlayerJump = []
		for i in range(self.qntImagePlayerJump):
			tempImage = self.settings.load_Images("jump"+str(i)+".png", "Player/ID"+str(self.playerID), -1)
			self.__imagePlayerJump.append(tempImage)

		self.__currentImagePlayer = self.__imagePlayerStop[0]
		self.__rectPlayer = self.__currentImagePlayer.get_rect()
		self.__rectPlayer.y += self.camera.getPosYplayer()

	#-----------------------------------
	#Jump

	def __setImagePlayerJump(self, numImg):
		self.__currentImagePlayer = self.__imagePlayerJump[numImg]
		self.numCurrentImagePlayer = numImg
		self.__flipImage()

	def __setProxImagePlayerJump(self):
		if self.numCurrentImagePlayer == self.qntImagePlayerJump -1:
			pass
			#self.numCurrentImagePlayer = 0
			#self.__setImagePlayerJump(0)
		else:
			self.__setImagePlayerJump(self.numCurrentImagePlayer + 1)

	#-----------------------------------
	#-----------------------------------
	#Walk

	def __setImagePlayerWalk(self, numImg):
		self.__currentImagePlayer = self.__imagePlayerWalk[numImg]
		self.numCurrentImagePlayer = numImg
		self.__flipImage()

	def __setProxImagePlayerMoving(self):
		if self.inMoving:
			if self.numCurrentImagePlayer == self.qntImagePlayerWalk -1:
				self.__setImagePlayerWalk(0)
			else:
				self.__setImagePlayerWalk(self.numCurrentImagePlayer + 1)
		else:
			self.startMoviment = False
			if self.numCurrentImagePlayer == self.qntImagePlayerStop -1:
				self.__setImagePlayerStop(0)
			else:
				self.__setImagePlayerStop(self.numCurrentImagePlayer + 1)

	#-----------------------------------
	#-----------------------------------
	#Stop

	def __setImagePlayerStop(self, numImg):
		self.__currentImagePlayer = self.__imagePlayerStop[numImg]
		self.numCurrentImagePlayer = numImg
		self.__flipImage()
	
	#-----------------------------------
	#-----------------------------------
	#Attack

	def __setImagePlayerAttack(self, numImg):
		self.__currentImagePlayer = self.__imagePlayerAttack[numImg]
		self.numCurrentImagePlayer = numImg
		self.weaponAtual.setCurrentImage(self.numCurrentImagePlayer)
		self.weaponAtual.resetFlipDis()
		self.__flipImage()

	def __setProxImagePlayerAttack(self):
		if self.numCurrentImagePlayer == self.qntImagePlayerAttack -1:
			self.inAtack = False
			self.numCurrentImagePlayer = 0
			#self.__setImagePlayerAttack(0)
		else:
			self.__setImagePlayerAttack(self.numCurrentImagePlayer + 1)

	#-----------------------------------

	def __setProxImagePlayer(self):
		#Maquinas de estado do player, não podem ser chamadas ao mesmo
		if self.inAtack:
			self.__setProxImagePlayerAttack()
		elif self.inJump:
			self.__setProxImagePlayerJump()
		else:
			self.__setProxImagePlayerMoving()

	def setInMoving(self, inMoving):
		self.inMoving = inMoving
		if not inMoving and not self.inAtack:
			self.resetCurrentImagePlayer()
		self.inMoving = inMoving

	def setInJump(self, inJump):
		if self.inAtack:
			return
		self.inJump = inJump
		self.resetCurrentImagePlayer()

	def resetCurrentImagePlayer(self):
		self.numCurrentImagePlayer = 0

	def resetCurrentImagePlayerAfterJump(self):
		self.numCurrentImagePlayer = 1

	def getPlayerPosX(self):
		return self.camera.getPosXplayer() + self.settings.screen_width/2

	def update(self):
		self.__updateMousePosition()
		self.__updateImages()
		self.__updateStep()
		self.__updateJump()
		self.__updateCounters()

	def __updateCounters(self):
		if self.inDamage:
			self.countImunityTime+=1

	def __updateImages(self):
		tempVelocity = self.velocityImagePlayer
		if self.inAtack:
			tempVelocity = self.velocityImagePlayerAttack
		self.endChangeImage = time.time()
		if self.endChangeImage - self.startChangeImage >= tempVelocity:
			self.startChangeImage = time.time()
			self.__setProxImagePlayer()

	def __updateStep(self):
		if (self.numCurrentImagePlayer >= 1 or self.startMoviment) and self.inMoving:
			self.startMoviment = True
			self.__step()

	def __step(self):
		if not self.__verificaExtremos() and self.inMoving:
			if self.playerVelocity < 0 and not self.colisionLeft:    #Verifica se o jogador está se movendo para a esquerda e se não está colidindo pela esquerda
				self.camera.addPlayerPosX(self.playerVelocity)            #Altera a posição do jogador (Na real altera a posição posX que é do background, o personagem é fixo no meio do background)
			elif self.playerVelocity > 0 and not self.colisionRight:
				self.camera.addPlayerPosX(self.playerVelocity)

	def __verificaExtremos(self):
		if self.camera.getPosXplayer() + self.playerVelocity < self.settings.screen_width/2:
			return True
		if self.camera.getPosXplayer() + self.playerVelocity > self.camera.getBackgroundImageW() - self.settings.screen_width - self.__rectPlayer.w/2:
			return True
		return False

	def __updateJump(self):
		if self.inJump:
			self.__jump()
	
	def __jump(self):
		if self.countInJumpUp - self.playerStatusDefaultJumpTime > 0:
			self.countInJumpUp -= self.playerStatusDefaultJumpTime
			self.countInJumpDown += self.playerStatusDefaultJumpTime
			self.__rectPlayer.y += self.playerStatusDefaultJumpTime
		else:
			if self.countInJumpDown == 0:
				self.inJump = False
				self.resetCurrentImagePlayer()
				self.countInJumpUp = self.playerHeightJump
				self.countInJumpDown = 0
			else:
				self.countInJumpDown -= self.playerStatusDefaultJumpTime
				self.__rectPlayer.y -= self.playerStatusDefaultJumpTime

	def __updateMousePosition(self):
		#Muda a variavel de controle para verificar a posição do mouse na tela
		metadeTelaX = int(self.settings.screen_width/2)
		#pygame.mouse.get_pos()[0] pega a posição X do cursor do mouse atual
		if pygame.mouse.get_pos()[0] > metadeTelaX:
			self.posXMouseInScreenIsRightSide = True
		else:
			self.posXMouseInScreenIsRightSide = False

	def __flipImage(self):
		if not self.posXMouseInScreenIsRightSide:
			tempColorKey = self.__currentImagePlayer.get_colorkey()
			tempImage = pygame.transform.flip(self.__currentImagePlayer, True, False)
			tempImage.set_colorkey(tempColorKey)
			self.__currentImagePlayer = tempImage
			tempY = self.__rectPlayer.y
			self.__rectPlayer = self.__currentImagePlayer.get_rect()
			self.__rectPlayer.y = tempY
			self.weaponAtual.flipImage()

	def resetVariables(self):
		self.__loadVariables()

	def draw(self, camera):
		camera.drawScreenFix(self.__currentImagePlayer, (self.settings.screen_width/2, self.settings.valuePosY-self.__rectPlayer.h-self.__rectPlayer.y))
		if self.inAtack:
			camera.drawScreenFix(self.weaponAtual.getCurrentImage(), (self.settings.screen_width/2+self.weaponAtual.flipDis, self.settings.valuePosY-self.__rectPlayer.h-self.__rectPlayer.y-8))

	def getRectPlayer(self):
		tempRect = self.__rectPlayer.copy()
		tempRect.x = self.getPlayerPosX()
		return tempRect

	def getWeapon(self):
		return self.weaponAtual

	def removeColision(self):
		self.colisionLeft = False
		self.colisionRight = False

	def setDamage(self, damage):
		if self.inDamage:                       #Se já levou dano e está no tempo de invunerabilidade
			#A variabel contador de imunidade é incrementada no update de contadores
			if self.countImunityTime >= self.playerImunityTime:
				self.inDamage = False
				self.countImunityTime = 0
		else:
			self.inDamage = True
			self.countImunityTime = 0
			if self.playerLife - damage <= 0:
				self.playerLife = 0
			else:
				self.playerLife -= damage

			if self.settings.generalInfo:
				print ("Damage %d | Life %d" % (damage, self.playerLife))

	def attack(self):
		if self.inJump or self.inAtack:
			return
		self.inAtack = True
		self.numCurrentImagePlayer = 0

	def getMoneyFromChat(self, value):
		self.playerMoney += value
		print ("Get money %d (from chat)" % (value))

	def getWeaponDamageFromChat(self, value):
		self.playerDamage += value
		print ("Get weapon damage %d (from chat)" % (value))

	def getHPFromChat(self, value):
		self.playerLife += value
		print ("Get HP %d (from chat)" % (value))

	def setHPFromChat(self, value):
		self.playerLife = value
		print ("Set HP %d (from chat)" % (value))

	def getVelocityFromChat(self, value):
		self.playerVelocity += value
		print ("Get Velocity %d (from chat)" % (value))
import os, sys
import pygame

class Player(pygame.sprite.Sprite):

	def __init__(self, image, settings):
		pygame.sprite.Sprite.__init__(self)
		self.settings = settings
		self.image = image
		self.rect = image.get_rect()

		self.__init()

	def __init(self):
		self.__loadClass()
		self.__loadVariables()
		self.__setImagensPositions()

	def __loadClass(self):
		#Variaveis importantes
		self.__qntImages = 7                         #Quantidade de subImagens da imagem do personagem
		self.__vectorPosX = [0]*self.__qntImages     #Vetor com as posições das subImagens dentro da imagem
		self.__vectorPosY = [0]*self.__qntImages	 #Não irá ter cópia na loadVariables pois não é preciso resetar
		self.__currentImage = 0                      #Imagem Inicial
		self.__duracaoAirJump = 5                    #Tempo que o jogador irá permanecer no ar encostado no topo do jump
		self.__duracaoJump = 20
		self.__imunityTime = self.settings.imunityTime    #Tempo de imunidado após levar dano

		#Status
		self.__velocidadeJogador = self.settings.velocidadeJogador   #velocidade inicial do jogador
		self.__damageJogador = self.settings.damageJogador
		self.__vidaJogador = self.settings.vidaJogador

		#Contadores
		self.__VelocidadeImage = 6                     #Velocidade da troca de imagem do jogador
		self.__contadorImage = 0                       #Variavel auxiliar durante a troca de imagem
		self.__contadorJump = 0                        #Variavel auxiliar durante o jump
		self.__contadorAirJump = 0                     #Variavel auxiliar durante o Air Jump
		self.__contadorInDamage = 0                    #Variavel auxiliar durante o tempo que levar dano

		#Rect
		""">>>>>>>>>>>>>>>>>>>>> ALERTA DE GAMBIARRA DO JOSÉ <<<<<<<<<<<<<<<<<<<"""
		"""O jogador se manterá FIXO no meio do background. O background que irá se movimentar"""
		"""Com isso as variaveis rect.x e rect.y do jogador NÃO SE ALTERAM ALÉM DAQUI"""
		self.rect.x = int(self.settings.screen_width/2)    #X do personagem será no meio da janela
		self.rect.y = self.settings.posY                   #Y do personagem será na divisão do chão
		self.rect.w = self.settings.imageJogadorW
		self.rect.h = self.settings.imageJogadorH

		#Variaveis de controle iniciais
		self.__inMoving = False           #Verifica se o jogador está se movendo
		self.__colisionRight = False      #Verifica colisão
		self.__colisionLeft = False
		self.__inJump = False             #Verifica se o jogador está pulando
		self.__inInverseJump = False      #Verifica se o jogador está caindo
		self.__inAirJump = False          #Verifica se o jogador atigingiu a altura máxima
		self.__inDamage = False           #Verifica se levou dano


	def __loadVariables(self):
		#Status
		self.velocidadeJogador = self.__velocidadeJogador
		self.damageJogador = self.__damageJogador
		self.vidaJogador = self.__vidaJogador

		self.currentImage = self.__currentImage
		self.contadorImage = self.__contadorImage
		self.contadorJump = self.__contadorJump
		self.contadorAirJump = self.__contadorAirJump
		self.contadorInDamage = self.__contadorInDamage

		self.inMoving = self.__inMoving
		self.colisionRight = self.__colisionRight
		self.colisionLeft = self.__colisionLeft
		self.inJump = self.__inJump
		self.inInverseJump = self.__inInverseJump
		self.inAirJump = self.__inAirJump
		self.inDamage = self.__inDamage
		

	def resetVariables(self):
		self.__loadVariables()

	def draw(self, background):
		background.blit(self.image, (self.rect.x, self.rect.y), (self.__vectorPosX[self.currentImage],self.__vectorPosY[self.currentImage],96,96))

	def __setImagensPositions(self):
		self.__vectorPosX[0] = 0
		self.__vectorPosX[1] = 96
		self.__vectorPosX[2] = 192
		self.__vectorPosX[3] = 0
		self.__vectorPosX[4] = 96
		self.__vectorPosX[5] = 192
		self.__vectorPosX[6] = 96

		self.__vectorPosY[0] = 96
		self.__vectorPosY[1] = 96
		self.__vectorPosY[2] = 96
		self.__vectorPosY[3] = 192
		self.__vectorPosY[4] = 192
		self.__vectorPosY[5] = 192
		self.__vectorPosY[6] = 0

	def update(self):
		self.__contadores()                  #Atualiza contadores importantes
		if self.inMoving:
			if self.__verificaExtremos():    #Se o personagem não está nos extremos entra no if
				self.__step()                #Move o personagem
				self.__updateCurrentImage()  #Altera a imagem do personagem se movendo
		if self.inJump:
			self.__jump()                    #Pula

	def __step(self):
		if self.velocidadeJogador < 0 and not self.colisionLeft:    #Verifica se o jogador está se movendo para a esquerda e se não está colidindo pela esquerda
			self.settings.posX += self.velocidadeJogador            #Altera a posição do jogador (Na real altera a posição posX que é do background, o personagem é fixo no meio do background)
		elif self.velocidadeJogador > 0 and not self.colisionRight:
			self.settings.posX += self.velocidadeJogador

	def colisionMob(self, mob):
		if self.inJump:                   #Se está pulando não faz a checagem de colisão
			mob.inMoving = True           #Faz o mob voltar a se mover
			self.__removeColision(mob)    #Remove as colisoes
			return
		self.__checkColision(mob)

	def __removeColision(self, mob):
		self.colisionLeft = False
		self.colisionRight = False

	def __checkColision(self, mob):
		self.tempMobRect = mob.rect.copy()
		if mob.velocidadeMob > 0:
			self.tempMobRect.x -= self.settings.colisionDiferenceMob1  #Diminui a distancia entre o mob e o player para conseguir verificar a colisão
			if self.rect.colliderect(self.tempMobRect):                #Verifica a colisão entre o player e o rect
				self.__setDamage(mob.damageMob)
				mob.inMoving = False
				self.colisionLeft = True
			elif not mob.inMoving:
				self.colisionLeft = False
				mob.inMoving = True
		elif mob.velocidadeMob < 0:
			self.tempMobRect.x += self.settings.colisionDiferenceMob1  #Diminui a distancia entre o mob e o player para conseguir verificar a colisão
			if self.tempMobRect.colliderect(self.rect):                #Verifica a colisão entre o mod e o player
				self.__setDamage(mob.damageMob)
				mob.inMoving = False
				self.colisionRight = True
			elif not mob.inMoving:
				self.colisionRight = False
				mob.inMoving = True

	def __verificaExtremos(self):
		#Verifica se chegou no extremo do mapa
		#0 é o limite da direita e 4200 o limite da esquerda
		if self.settings.posX + self.velocidadeJogador < 0:
			self.currentImage = 6
			return False
		if self.settings.posX + self.velocidadeJogador > 4200:
			self.currentImage = 6
			return False
		return True    #Se não está no limite retorna True, caso contrario retorna False

	def __updateCurrentImage(self):
		if self.velocidadeJogador < 0:  #Caso esteja se movendo para a esquerda
			if self.currentImage == 6: #Caso ele esteja no extremo oposto faz ele voltar a imagem inicial de movimento
				self.currentImage = 0
				return

			#Caso a imagem atual seja uma de movimento para a esquerda e o personagem também está se movendo para a esquerda
			if self.currentImage < 3:
				#Altera para a proxima imagem do frame a cada self.__VelocidadeImage passos
				#Ao mudar a imagem, reseta o contador. Se não mudar, incrementa o contador
				if self.contadorImage == self.__VelocidadeImage:
					self.currentImage = (self.currentImage+1) % 3
					self.contadorImage = 0
				self.contadorImage += 1
			#Caso a imagem atual seja uma de movimento para a direita e o personagem está se movendo para a esquerda
			#Apenas reseta a imagem para a imagem inicial de movimento
			else:
				self.currentImage = 0
				self.contadorImage = 0
		elif self.velocidadeJogador > 0:   #Caso esteja se movendo para a direita
			if self.currentImage == 6:     #Caso ele esteja no extremo oposto faz ele voltar a imagem inicial de movimento
				self.currentImage = 3
				return

			#Caso a imagem atual seja uma de movimento para a direita e o personagem também está se movendo para a direita
			if self.currentImage > 2:
				if self.contadorImage == self.__VelocidadeImage:
					self.currentImage = ((self.currentImage+1) % 3) + 3
					self.contadorImage = 0
				self.contadorImage += 1
			else:
				self.currentImage = 3
				self.contadorImage = 0

	def __jump(self):
		#Verifica se está no limite do pulo e se mantém por mais self.__duracaoAirJump no ar
		if self.inAirJump and not self.contadorAirJump == self.__duracaoAirJump:
			self.contadorAirJump += 1
			return
		
		if self.inInverseJump:                            #Verifica se está caindo (Pulou, chegou no topo e está caindo)
			self.rect.y += self.settings.velocidadeJump
			self.contadorJump -= 1
		else:
			self.rect.y -= self.settings.velocidadeJump
			self.contadorJump += 1

		if self.contadorJump == self.__duracaoJump:  #Verifica se pulou até chegar no topo
			self.inInverseJump = True                #Variavel para começar a descer do pulo
			self.inAirJump = True                    #Variavel para se manter no ar por um tmepo
			self.contadorAirJump = 0				 #Reseta o contador
		elif self.contadorJump == 0:                 #Verifica se tocou o chão
			self.inInverseJump = False               #Reseta as variaveis de pulo para False // Acabou o pulo
			self.inJump = False
			self.inAirJump = False
	
	def __contadores(self):
		#Atualiza contadores que dependem do jogo rodar e não de outras variaveis externas
		if self.contadorInDamage < self.__imunityTime:
			self.contadorInDamage += 1

	def __setDamage(self, damage):
		if self.inDamage:                       #Se já levou dano e está no tempo de invunerabilidade
			if self.contadorInDamage == self.__imunityTime:
				self.inDamage = False
		else:
			self.inDamage = True
			self.contadorInDamage = 0
			if self.vidaJogador - damage <= 0:
				self.vidaJogador = 0
				self.settings.gameOver = 1
			else:
				self.vidaJogador -= damage
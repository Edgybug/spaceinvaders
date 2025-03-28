import pygame
from pygame.locals import *

#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size, *groups):
		super().__init__(*groups) 
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"img/exp{num}.png").convert_alpha()
			if size == 1:
				img = pygame.transform.scale(img,(20,20))
			if size == 2:
				img = pygame.transform.scale(img,(40,40))
			if size == 3:
				img = pygame.transform.scale(img,(160,160))
			self.images.append(img)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_frect(center = (x,y))
		self.counter = 0
	def animate(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()
			
	def update(self, dt):
		self.animate()

	def draw(self, screen):
		screen.blit(self.image, self.rect)



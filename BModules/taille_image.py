from    pygame.locals  import *
import  pygame

def ti(image, haut = 0, cote = 0):
	taille_x, taille_y = image.get_size()
	taille_x += cote
	taille_y += haut
	return taille_x, taille_y
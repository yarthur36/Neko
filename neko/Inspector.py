# # # # # # # # # # # #
# 24/04/2020          #
# CHEVALIER Arthur    #
# JAMBOU Clemence     #
# IPI S2 : Neko       #
# Prototype 1         #
# Module Inspector    #
# # # # # # # # # # # #

import sys

#Creation d'un inspecteur possedant une position en x et y, une vitesse en x et y ainsi que d une direction
def create():
	inspector={'x':70,'y':20,'vx':0,'vy':0,'direction':None,'no_clip':False}
	return inspector
#accesseur position en x
def get_x(inspector):
	return inspector['x']
#accesseur position en y
def get_y(inspector):
	return inspector['y']
#accesseur vitesse en x
def get_vx(inspector):
	return inspector['vx']
#accesseur position en y
def get_vy(inspector):
	return inspector['y']
#mutateur position en x
def set_x(inspector,new):
	inspector['x']=new
	return
#mutateur position en y
def set_y(inspector,new):
	inspector['y']=new
	return
#mutateur vitese en x
def set_vx(inspector,new):
	inspector['vx']=new
	return
#mutateur vitesse en y
def set_vy(inspector,new):
	inspector['vy']=new
	return
#accesseur direcion de l'inspecteur
def get_direction(inspector):
	return inspector['direction']
#mutateur direction de l'inspecteur
def set_direction(inspector,direction):
	inspector['direction']=direction
	return
#Calcul de la prochaine position de l'inspecteur
def get_next_position(dt,inspector):
	x=inspector['x']+dt*inspector['vx']
	y=inspector['y']+dt*inspector['vy']
	return x,y
#Fonction qui permet a l'inspecteur de se deplacer
def move(inspector,dt):
	inspector['x']=inspector['x']+dt*inspector['vx']
	inspector['y']=inspector['y']+dt*inspector['vy']
	return
#deplacement vers le haut
def move_up(inspector):
	inspector['vy']=-5.0
	inspector['vx']=0
	inspector['direction']='up'
	return
#deplacement vers le bas
def move_down(inspector):
	inspector['vy']=5.0
	inspector['vx']=0
	inspector['direction']='down'
	return
#deplacement vers la gauche
def move_left(inspector):
	inspector['vx']=-6.0
	inspector['vy']=0
	inspector['direction']='left'
	return
#deplacement vers la droite
def move_right(inspector):
	inspector['vx']=6.0
	inspector['vy']=0
	inspector['direction']='right'
	return

#affichage de l'inspecteur
def show(inspector,colorI,shape): 
	x=int(inspector["x"])
	y=int(inspector["y"])
	#on va a l enplacement x y 
	txt="\033["+str(y)+";"+str(x)+"H"
	#rien
	sys.stdout.write(txt)	
	#animat
	sys.stdout.write("\033[40m")
	sys.stdout.write(str(colorI) + shape )

#Le caractere present sur la prochaine position de l'inspecteur
def get_carac(x,y,FrameWork):
	assert type(FrameWork) is dict
	caractere = FrameWork['grid'][y-1][x-1]
	return caractere

#les déplacement de l'inspecteur sont stoppé
def stuck(inspector):
	x=inspector['x']
	y=inspector['y']
	inspector['x']=x
	inspector['y']=y
	return

#Si il y a collision dans une épreuve
def trap(inspector,tr,carte):
	#crimelab
	if tr['background'] == carte[6] :
		inspector['x']=10
		inspector['y']=21
		inspector['vx']=0
		inspector['vy']=0
	#Boucher lab
	elif tr['background'] == carte[7] :
		inspector['x']=7
		inspector['y']=18
		inspector['vx']=0
		inspector['vy']=0
	#postelab
	elif tr['background'] == carte[8] :
		inspector['x']=82
		inspector['y']=40
		inspector['vx']=0
		inspector['vy']=0	
	#voisinelab
	elif tr['background'] == carte[5] :
		inspector['x']=10
		inspector['y']=21
		inspector['vx']=0
		inspector['vy']=0 
	else : 
		pass
	return


def set_no_clip(inspector) :

	if inspector['no_clip']==False :
		inspector['no_clip']=True

	else :
		inspector['no_clip']=False
	
	return
		
def get_no_clip(inspector):
	return inspector['no_clip']	


#Changement de couleur de l'inspecteur'
def color_inspector(color_i):	
	if color_i=='\033[37m' :
		color_i = '\033[31m'
	elif color_i == '\033[31m' :
		color_i = '\033[32m'
	elif color_i == '\033[32m' :
		color_i = '\033[33m'
	elif color_i == '\033[33m' :
		color_i = '\033[34m'
	elif color_i == '\033[34m'  :
		color_i = '\033[35m'
	elif color_i == '\033[35m':
		color_i = '\033[36m' 
	elif color_i == '\033[36m' :
		color_i = '\033[37m'
	return color_i

if __name__=='__main__':
	pass
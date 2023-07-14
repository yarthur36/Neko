# # # # # # # # # # # #
# 24/04/2020          #
# CHEVALIER Arthur    #
# JAMBOU Clemence     #
# IPI S2 : Neko       #
# Prototype 1         #
# Module Transition   #
# # # # # # # # # # # #

import Inspector
import Story
import sys

#creation de la machine a etat qui va gerer les transitions de background
#Cette machine a etat est  constitue d'un nom, d'un background(contenant le background qui sera affiché) et de plusieurs variables,
#qui serviront a savoir si le joueur est déjà passé dans chaque labyrinthe
def create(name):
	tr={'name':name,'background':None,'map_number':0}
	return tr
#accesseur nom de la machine a etat
def get_name(tr):
	return tr['name']
#mutateur nom de la machine a etat
def set_name(tr,name):
	tr['name']=name
	return
#accesseur background qui est affiche
def get_bg(tr):
	return tr['background']
#mutateur background qui est affiche
def set_bg(tr,Bg):
	tr['background']=Bg
	return

def get_map_number(tr):
	return tr['map_number']

def set_map_number(tr,new):
	tr['map_number']=new
	return

def transition_carte(dt,inspector,color_i,color_f,tr,carte,x,talk,investigation,dial,step,goal):
	nx,ny=Inspector.get_next_position(dt,inspector)
	frame=get_bg(tr)
	map_number=get_map_number(tr)
	#tarnsition finale
	if investigation == 7 and frame==carte[0] :
		if float(carte[10]['transition'][0][0]) <= nx <= float(carte[10]['transition'][0][1]) :
			if float(carte[10]['transition'][0][2]) <= ny <= float(carte[10]['transition'][0][3]) :
				investigation = 8
				return
					
	#Si on est sur le main
	elif investigation <= 7 :
		for a in range(0,len(carte)-1) :
			if Story.get_on(talk) ==False : 
				if carte[a]==frame:
					for b in range(0,len(carte[a]['transition'])) :
						if float(carte[a]['transition'][b][0]) <= nx <= float(carte[a]['transition'][b][1]) :
							if float(carte[a]['transition'][b][2]) <= ny <= float(carte[a]['transition'][b][3]) :
								frame= carte[int(carte[a]['transition'][b][5])]
								map_number=int(carte[a]['transition'][b][5])
								Inspector.set_x(inspector,float(carte[a]['transition'][b][6]))								
								Inspector.set_y(inspector,float(carte[a]['transition'][b][7]))
								Inspector.set_vx(inspector,0)
								Inspector.set_vy(inspector,0)
								sys.stdout.write("\033[2J") 
								
	else :
		pass


if __name__ == '__main__' :
	pass
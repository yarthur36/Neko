# # # # # # # # # # # #
# 24/04/2020          #
# CHEVALIER Arthur    #
# JAMBOU Clemence     #
# IPI S2 : Neko       #
# Prototype 1         #   
# Module Main         #
# # # # # # # # # # # #

#Modules Externes
import time
import sys
import termios
import select
import tty
#Mes Modules 
import Inspector
import FrameWork
import Transition
import Story
#Initialisation des variables qui seront utilisés
inspector=None
#variables
carte=None
color_i=None
color_f=None
shape=None
x=None
talk=None
win = None
step = None
investigation=None

old_settings = termios.tcgetattr(sys.stdin)

def init():
	global dt,inspector,color_i,color_f,tr,carte,x,talk,investigation,dial,goal
	#variable de temps
	dt=0.1
	#creation des variables contenant toutes les maps et création machine a etat
	tr=Transition.create("Transition")
	main=FrameWork.create("Main.txt","tranmain.txt")
	crime=FrameWork.create("crime.txt","trancrime.txt")
	voisine=FrameWork.create("voisine.txt","tranvoisine.txt")
	poste=FrameWork.create("poste.txt","tranposte.txt")
	boucher=FrameWork.create("boucher.txt","tranboucher.txt")
	voisinelab=FrameWork.create("voisinelab.txt","tranvoisinelab.txt")
	crimelab=FrameWork.create("crimelab.txt","trancrimelab.txt")
	boucherlab=FrameWork.create("boucherlab.txt","tranboucherlab.txt")
	postelab=FrameWork.create("postelab.txt","tranpostelab.txt")
	framevide=FrameWork.create("FrameVide.txt","tranframevide.txt")
	commisariat=FrameWork.create("FrameVide.txt","trancommissariat.txt")
	carte=(main,crime,voisine,poste,boucher,voisinelab,crimelab,boucherlab,postelab,framevide,commisariat)
	tr['background']=carte[0]
	#Création des dialogues entre les personnages
	Policedial=Story.create('Police',"police.txt","trandialpolice.txt")
	Indicedial=Story.create('Indice',"indices.txt","trandialindice.txt")
	Dialvide=Story.create('Vide',"dialvide.txt","trandialvide.txt")
	Voisinedial=Story.create('Voisine',"voisinedial.txt","trandialvoisine.txt")
	Postedial1=Story.create('poste1',"postedial1.txt","trandialposte1.txt")
	Postedial2=Story.create('poste2',"postedial2.txt","trandialposte2.txt")
	Boucherdial=Story.create('boucher',"boucherdial.txt","trandialboucher.txt")
	dial=(Dialvide,Policedial,Indicedial,Voisinedial,Postedial1,Boucherdial,Postedial2)
	talk=dial[0]
	#initialisation des variables color sur la couleur blanche
	goal=Story.get_goal('goal.txt')
	color_i="\033[37m"
	color_f="\033[37m"
	#initialisation de la variable de début de jeu
	x=True
	#initialisation des variables qui vont enregistré l'avancé de l'histoire
	investigation = 1
	#creation de l'inspector
	inspector=Inspector.create()
	#Le mode cbreak permet de recuperer toutes les entrées claviers
	tty.setcbreak(sys.stdin.fileno())
	#mettre le curseur a 0 et clean le terminal
	sys.stdout.write("\033[0;0H")
	sys.stdout.write("\033[2J")
	return

def move():
	global dt,inspector,color_i,color_f,tr,carte,x,talk,investigation,dial,step,goal
	#Si le joueur entre dans une maison, la machine a etat s'occupe de gerer les transitions de background
	transition_carte()
	frame = Transition.get_bg(tr)
	no_clip=Inspector.get_no_clip(inspector)
	#Si l'inspecteur est sur une carte normal
	if frame == carte[0] or frame==carte[1] or frame==carte[2] or frame==carte[3] or frame==carte[4] :
		#vérification de la case suivante de l inspector
		if (FrameWork.collide(frame,inspector)==True):
			#si la case est vide, il se deplace
			Inspector.move(inspector,dt)
		else :
			#Si la case est pleine, il reste à sa position
			Inspector.stuck(inspector)
		return
	#Si l'inspecteur est sur une map labyrinthe
	elif frame == carte[5] or frame==carte[6] or frame==carte[7] or frame==carte[8] :
		####LA CONDITION NO_CLIP PERMET SI ON LE SOUHAITE D'ENLEVER LES COLLISIONS "PIEGE" POUR FACILITER L'EVALUATION DU PROJET####
		if no_clip==False :
			if (FrameWork.collide(frame,inspector)==True) :
					#si la case est vide, il se deplace
					Inspector.move(inspector,dt)
			else :
				#Si la case est pleine, il revient au point de départ
				Inspector.trap(inspector,tr,carte)
		elif no_clip==True :
			if (FrameWork.collide(frame,inspector)==True):
				#si la case est vide, il se deplace
				Inspector.move(inspector,dt)
			else :
				pass
	else :
		pass


def choose_inspector():
	global shape,x
	#On se place au milieu de l'écran
	txt="\033["+str(30)+";"+str(90)+"H"
	sys.stdout.write(txt)
	#On pose la question
	sys.stdout.write('Pour choisir votre personnage, tapez O ou 8 ')
	if keyboard():
		#On récupère le choix du joueur
		shape=sys.stdin.read(1)
		#Si le joueur appuie sur o, l'inspector sera O
		if shape == '0' :
			shape='O'
			x=False
			#Si le joueur appuie sur x, l'inspector sera X
		elif shape == '8' :
			shape = '8'
			x=False
		return shape

def keyboard():
	#On regarde si il y a eu une intéraction avec le clavier
 	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def interact():
	global animat,color_i,color_f
	#Si on a une interaction avec le clavier
	if keyboard():
		#on garde cette valeure correspondant a l'interaction clavier
		x=sys.stdin.read(1)
		#Si la touche pressee est echap,on quite le jeu
		if x=='\x1b' : 
			quitgame()
			#Si la touche pressee est z, le personnage monte
		elif x =='z':
			Inspector.move_up(inspector)
			#Si la touche pressee est s, le personnage descend
		elif x =='s':
			Inspector.move_down(inspector)
			#Si la touche pressee est d, le personnage se deplace vers la droite
		elif x =='d':
			Inspector.move_right(inspector)
			#Si la touche pressee est q, le personnage se déplace vers la gauche
		elif x =='q':
			Inspector.move_left(inspector)
			#Si la touche pressee est c, le personnage change de couleur
		elif x == 'p':
			Inspector.set_no_clip(inspector)
		elif x =='c':
			color_i = Inspector.color_inspector(color_i)
		elif x =='v':
			color_f = FrameWork.color_frameWork(color_f)
		else:
			pass


def show():
	global tr,inspector,dt,carte,color_i,color_f,talk,investigation,dial,goal
	#Affiche du background
	FrameWork.show(Transition.get_bg(tr),color_f)
	#affichage de l inspector
	Inspector.show(inspector,color_i,shape)
	#affichage des dialogues
	story_speak()
	Story.show_story(talk,dt)
	#affichage de l'objectif
	Story.show_goal(investigation,carte,tr,goal)
	#La map est en blanc
	sys.stdout.write("\033[37m")
	#Le background derriere la map est en noir
	sys.stdout.write("\033[40m")
	#On replace le curseur a la position 0
	sys.stdout.write("\033[0;0H\n")

	return


##################################################################################
#      Cette fonction devrait se trouver dans le module story mais  			 #
#	   les changements de valeurs de 'investigation' ne sont pas pris en compte  #
##################################################################################
def story_speak():
	global dial,inspector,talk,investigation,dt,carte
	nx,ny=Inspector.get_next_position(dt,inspector)
	map_number=Transition.get_map_number(tr)

	for a in range (0,len(dial)):
		if int(dial[a]['transition'][0][4])==int(map_number) :
			if int(dial[a]['transition'][0][5])==investigation :
				if float(dial[a]['transition'][0][0])<= nx <= float(dial[a]['transition'][0][1]) :
					if float(dial[a]['transition'][0][2]) <= ny <= float(dial[a]['transition'][0][3]):
						talk=dial[int(dial[a]['transition'][0][6])]
						Story.set_on(talk,True)
						investigation = investigation +1

def transition_carte():
	global dt,inspector,color_i,color_f,tr,carte,x,talk,investigation,dial,step,goal
	nx,ny=Inspector.get_next_position(dt,inspector)
	#tarnsition finale
	if investigation == 7 and tr['background']==carte[0] :
		if float(carte[10]['transition'][0][0]) <= nx <= float(carte[10]['transition'][0][1]) :
			if float(carte[10]['transition'][0][2]) <= ny <= float(carte[10]['transition'][0][3]) :
				investigation = 8
				return
					
	#Si on est sur le main
	elif investigation <= 7 :
		for a in range(0,len(carte)-1) :
			if Story.get_on(talk) ==False : 
				if carte[a]==tr['background']:
					for b in range(0,len(carte[a]['transition'])) :
						if float(carte[a]['transition'][b][0]) <= nx <= float(carte[a]['transition'][b][1]) :
							if float(carte[a]['transition'][b][2]) <= ny <= float(carte[a]['transition'][b][3]) :
								tr['background']=carte[int(carte[a]['transition'][b][5])]
								tr['map_number']=int(carte[a]['transition'][b][5])
								Inspector.set_x(inspector,float(carte[a]['transition'][b][6]))								
								Inspector.set_y(inspector,float(carte[a]['transition'][b][7]))
								Inspector.set_vx(inspector,0)
								Inspector.set_vy(inspector,0)
								sys.stdout.write("\033[2J") 
								
	else :
		pass
#######################################################################################################################################

def finish():
	global color_i,goal,investigation,carte,tr,win
	sys.stdout.write("\033[2J")
	color_i="\033[30m"
	Story.show_goal(investigation,carte,tr,goal)
	txt="\033["+str(30)+";"+str(90)+"H"
	sys.stdout.write(txt)
	sys.stdout.write('Il est maintenant tant de révéler l identité du coupable')
	txt="\033["+str(31)+";"+str(83)+"H"
	sys.stdout.write(txt)
	sys.stdout.write('Tapez 1 pour Garfield ; Tapez 2 pour Hello Kitty ; Tapez 3 pour Grosminet')
	sys.stdout.write("\033[0;0H\n")

	if keyboard():
		c=sys.stdin.read(1)
		if c == '1' :
			win = False
		elif c == '2' :
			win = True
		elif c == '3' :
			win = False
		else : 
			pass

	if win == True : 
		sys.stdout.write("\033[2J")
		txt="\033["+str(30)+";"+str(90)+"H"
		sys.stdout.write(txt)
		sys.stdout.write('Vous avez gagnez !!!! Hello Kitty Etait bien le coupable')	
		quitgame()
	elif win == False :
		sys.stdout.write("\033[2J")
		txt="\033["+str(30)+";"+str(90)+"H"
		sys.stdout.write(txt)
		sys.stdout.write('Vous avez perdu. Réessayer si vous voulez trouver le coupable')	
		quitgame()
	else : 
		pass
	return


def run():
	global inspector,tr,carte,dt,x,investigation,talk,win,color_i,goal
	#On execute la fonction ChooseAnimat() une seule fois 
	while x == True :
		choose_inspector()
		sys.stdout.write("\033[2J")
	while True :
		if investigation == 8 :
				finish()
		else : 
			interact()
			move()
			show()
		#print("y",Inspector.get_y(inspector),"x",Inspector.get_x(inspector),investigation,tr['map_number'],inspector['no_clip'])
		time.sleep(dt)


def quitgame():
	global old_settings

	sys.stdout.write("\033[37m")
	sys.stdout.write("\033[40m")

	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	sys.exit()




if __name__=='__main__':
	# Pour lancer la partie : on initialise
	init()
	#Puis on lance la boucle de jeu
	run()
	#Si on appuie sur echap ca s'arrête 
	quitgame()
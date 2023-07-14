# # # # # # # # # # # #
# 22/03/2020          #
# CHEVALIER Arthur    #
# JAMBOU Clemence     #
# IPI S2 : Neko       #
# Module Story        #
# # # # # # # # # # # #

import sys
import Inspector
def create(name,filename,filetran):
	#creation de l'animation
	story={'name': name,'filename':filename,'x':190,'y':5}


	story['state']=False
	#ouvrir le fichier texte
	file=open(filename, "r")
	chaine=file.read()
	#separer les images
	frames=chaine.split("frame\n")
	frames.pop()

	story['frames']=[]
	for f in frames :
		sentence=f.split('\n')
		sentence.pop()	
		story['frames'].append(sentence)

	file.close()

	file = open(filetran, "r")

	chaine=file.read()
	tran=chaine.split('\n<information>\n')
	story['transition']=[]
	i=None
	for e in tran:
		i=str(e)
		i=i.split('i')
		i.pop()
		story['transition'].append(i)
	file.close()


	story['duration']=18.
	story['timeLeft']=None
	return story

def get_x(story):
	return story['x']

def get_y(story):
	return story['y']

def set_x(story,new):
	story['x']=new
	return

def set_y(story,new):
	story['x']=new
	return

def set_state(story,state):
	assert type(state) is Bool
	story['state']=state
	return

def get_state(story):
	return story['state']

def get_name(story):
	return story['name']

def set_name(story,new):
	story['name']=new
	return

def get_on(story):
	return story["state"]

def set_on(story,state):
	if state == True:
		story["state"]=True
		story["timeLeft"]=story["duration"]
	else:
		story["state"]=False
		story["timeLeft"]=None
	return

def get_current_frame(story):
	timeleft=story["timeLeft"]
	duration=float(story["duration"])
	number_frame=float(len(story["frames"]))
	
	step=duration/number_frame
	frame=int((duration-timeleft)/step)

	if frame >(len(story["frames"])-1):
		frame=(len(story["frames"])-1)
	
	return frame

def show_story(story,dt):

	if (get_on(story) ==False ): 
		return 

	story["timeLeft"]=story["timeLeft"]-dt

	if story['timeLeft'] <= 0 :
		set_on(story,False)
		return

	x=story['x']
	y=story['y']
	#le dialogue sera écrit en blanc
	sys.stdout.write("\033[37m")
	#le dialogue sera écrit sur fond noir
	sys.stdout.write("\033[40m")
	#e correpond aux lignes de dialogues
	e=get_current_frame(story)
	#Pour toute les répliques de chaque groupement de réplique
	for i in range(0,len(story['frames'][e])):
		x=int(story['x'])
		y=int(story['y'])
		s="\033["+str(y+1*(i+1))+";"+str(x)+"H"
		sys.stdout.write(s)
		#on écrit le texte
		sys.stdout.write(story['frames'][e][i])
		#on met à la ligne
		sys.stdout.write("\n")

def get_goal(filegoal):

	goal={}

	file = open(filegoal, "r")

	chaine=file.read()

	newchaine=chaine.split('\n<information>\n')
	goal['information']=[]
	i=None
	for e in newchaine:
		i=str(e)
		i=i.split('%')
		i.pop()
		goal['information'].append(i)

	file.close()

	return goal

def show_goal(investigation,carte,tr,goal):
	sys.stdout.write("\033[37m")
	place="\033["+goal['information'][0][1]+";"+goal['information'][0][2]+"H"
	sys.stdout.write(place)
	#main
	if tr['background'] == carte[0] :
		place="\033["+goal['information'][0][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#crime
	elif tr['background'] == carte[1] :
		place="\033["+goal['information'][2][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#voisine
	elif tr['background'] == carte[2] :
		place="\033["+goal['information'][3][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#poste
	elif tr['background'] == carte[3] :
		place="\033["+goal['information'][4][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#boucher
	elif tr['background'] == carte[4] :
		place="\033["+goal["information"][5][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#voisinelab
	elif tr['background'] == carte[5] :
		place="\033["+goal['information'][0][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#crimelab
	elif tr['background'] == carte[6] :
		place="\033["+goal['information'][6][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#boucherlab
	elif tr['background'] == carte[7] :
		place="\033["+goal['information'][4][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)
	#postelab
	elif tr['background'] == carte[8] :
		place="\033["+goal['information'][4][1]+";"+goal['information'][0][2]+"H"
		sys.stdout.write(place)

		
	if investigation <= 7 :
		for e in range(0,len(goal['information'])-1):
			sys.stdout.write(goal['information'][investigation-1][3])
			return

	elif investigation == 8 :
		sys.stdout.write('  ')

	else :
		return


def story_speak(dial,inspector,talk,investigation,tr,dt,carte):
	nx,ny=Inspector.get_next_position(dt,inspector)
	for a in range (0,len(dial)):
		if int(dial[a]['transition'][0][4])==int(tr['map_number']) :
			print('map')
			if int(dial[a]['transition'][0][5])==investigation :
				print('in')
				if float(dial[a]['transition'][0][0])<= nx <= float(dial[a]['transition'][0][1]) :
					if float(dial[a]['transition'][0][2]) <= ny <= float(dial[a]['transition'][0][3]):
						print('pl')
						talk=dial[int(dial[a]['transition'][0][6])]
						set_on(talk,True)
						investigation = investigation + 1


	return


if __name__ == '__main__' :
	Voisinedial=create('Voisine',"voisinedial.txt","trandialvoisine.txt")
	print(Voisinedial)
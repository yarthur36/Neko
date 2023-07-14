# # # # # # # # # # # #
# 24/04/2020          #
# CHEVALIER Arthur    #
# JAMBOU Clemence     #
# IPI S2 : Neko       # 
# Prototype 1         #     
# Module FrameWork    #
# # # # # # # # # # # #

import sys 
import Inspector

FrameWork=None

def create(filemap,filetran):

	FrameWork=dict()
	#création de la map
	file = open(filemap, "r")

	chaine=file.read()

	listeLignes=chaine.splitlines()
 
	FrameWork['grid']=[]

	#création de la map
	for line in listeLignes:
		#print("line",line)
		listeChar=list(line)
		FrameWork["grid"].append(listeChar)
	file.close()


	#création des transitions
	file = open(filetran, "r")

	chaine=file.read()
	tran=chaine.split('\n<information>\n')
	FrameWork['transition']=[]
	i=None
	for e in tran:
		i=str(e)
		i=i.split('i')
		i.pop()
		FrameWork['transition'].append(i)

	file.close()

	
	return FrameWork


def get_bg(FrameWork,x,y):
	return FrameWork['grid'][y][x]

def set_bg(FrameWork,x,y,new):
	FrameWork['grid'][y][x]=new
	return
	
def show(FrameWork,colorF) :
	sys.stdout.write("\033[40m")
	sys.stdout.write(colorF)

	for y in range(0,len(FrameWork['grid'])):
		for x in range(0,len(FrameWork["grid"][y])):
			s="\033["+str(y+1)+";"+str(x+1)+"H"
			carac=Inspector.get_carac(x+1,y+1,FrameWork)
			if carac != 'ç' :
				sys.stdout.write(s)
				sys.stdout.write(FrameWork["grid"][y][x])
			else :
				pass

#Cette fonction regarde la case suivante dans la direction où se déplace l'inspecteur et en déduit si il doit s'arrêter ou non
def collide(FrameWork,inspector):
	x=Inspector.get_x(inspector)
	y=Inspector.get_y(inspector)
	assert type(FrameWork) is dict

	if inspector['direction']=='right' :
		if Inspector.get_carac(int(x+1.6),int(y), FrameWork) == ' ' :	
			return True

	elif inspector['direction'] == 'left':
		if Inspector.get_carac(int(x-1), int(y), FrameWork) == ' ' :
			return True

	elif inspector['direction']=='up' :
		if Inspector.get_carac(int(x), int(y)-1, FrameWork) == ' ' :
			return True

	elif inspector['direction']=='down' :
		if Inspector.get_carac(int(x), int(y)+1, FrameWork) == ' ' :
			return True
	else :
		return False


def color_frameWork(color_f):	
	if color_f=='\033[37m' :
		color_f = '\033[31m'
	elif color_f == '\033[31m' :
		color_f = '\033[32m'
	elif color_f == '\033[32m' :
		color_f = '\033[33m'
	elif color_f == '\033[33m' :
		color_f = '\033[34m'
	elif color_f == '\033[34m'  :
		color_f = '\033[35m'
	elif color_f == '\033[35m':
		color_f = '\033[36m' 
	elif color_f == '\033[36m' :
		color_f = '\033[37m'
	return color_f


if __name__=='__main__':
	main=create("Main.txt","tranmain.txt")
	print(main)
	crime =create("crime.txt","trancrime.txt")
	print(crime)


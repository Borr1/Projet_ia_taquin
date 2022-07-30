import random
import itertools
import collections
from tkinter import *


def afficher_taquin(t):
    for col in t:
        ch=""
        print("+---+---+---+")
        for row in col:
            if row==0:
                ch+="|   "
            else:
                ch+="| "+str(row)+" "
        print(ch+"|")
    print("+---+---+---+")

def etat_depart():
    t=[[],[],[]]
    count=1
    val=[]
    for i in range(3):
        for j in range(3):
            afficher_taquin(t)
            inp=input("Inserer valeu n°"+str(count)+" : ")
            while(inp.isnumeric()==False or int(inp) not in[0,1,2,3,4,5,6,7,8] or int(inp) in val ):
                    
                    if(inp.isnumeric()==False):
                        print("La valeu doit etre numerique")
                    elif (int(inp) in val):
                        print("valeur deja insere")

                    else:
                        print("Les cases du taquin does etre numerotées de 1 à 8")
                    inp=input("Inserer valeu n°"+str(count)+" : ")
            count+=1
            val.append(int(inp))
            t[i].append(int(inp))
    afficher_taquin(t)
    return t

def numero(t,x,y):
    try:
        return t[x][y]
    except Exception as e:
        if x>2:
            print(x," est out of index")
        elif y>2:
            print(y, "est out of index")
        return e

class Node:

    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action

    @property
    def state(self):
        return str(self)

    @property 
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def estEtatFinal(self):
        return self.puzzle.estEtatFinal

    @property
    def transitions(self):
        return self.puzzle.transitions

    def __str__(self):
        return str(self.puzzle)



class Resolution:

    def __init__(self, start ,fenetre):
        self.start = start
        self.fenetre = fenetre

    def recherche_heuristique(self):
        def diff(node):
            
            diff=0
            verif="123804765"
            for i in range(9):
                if node.state[i]!="0":
                    if node.state[i]!=verif[i]:
                        diff+=1
            return diff
        print("Recherche en A*")
        print(self.start.board)
        queue = collections.deque([Node(self.start)])
        seen  = set()
        n=0
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            n+=1
            if node.estEtatFinal:
            	z= list(node.path)
            	self.afficher(z)
            	print("solution trouvée en", len(z) , " coups et ",len(seen)," noeuds explorés")
            	break
            decouverts=[]
            val=[]
            for move, action in node.transitions:
                child = Node(move(), node, action)             
                if child.state not in seen:
                    heuristique=diff(child)+n
                    decouverts.append(child)
                    val.append(heuristique)
            for heur,child in zip(val,decouverts):
                if(heur==min(val)):            
                    queue.appendleft(child)
                    seen.add(child.state)
    def recherche_largeur(self):
        print("Recherche de largeur :")
        queue = collections.deque([Node(self.start)])
        seen  = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.estEtatFinal:
            	z= list(node.path)
            	self.afficher(z)
            	print("solution trouvée en", len(z) , " coups et ",len(seen)," noeuds explorés")
            	break
            for move, action in node.transitions:
                child = Node(move(), node, action)
                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)
    def recherche_profondeur(self):
        print("Recherche en profondeur :")
        queue = collections.deque([Node(self.start)])
        seen  = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.estEtatFinal:
            	z= list(node.path)
            	self.afficher(z)
            	print("solution trouvée en", len(z) , " coups et ",len(seen)," noeuds explorés")
            	break
            for move, action in node.transitions:
                child = Node(move(), node, action)
                if child.state not in seen:
                    queue.append(child)
                    seen.add(child.state)

    
    def recherche_prof_lim(self):
        def profondeur(node):
            n=0    
            while node.parent!=None:
                n+=1
                node=node.parent
            return n
        
        print("Recherche en profondeur limité en 3 :")
        queue = collections.deque([Node(self.start)])
        seen  = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.estEtatFinal:
            	z= list(node.path)
            	self.afficher(z)
            	print("solution trouvée en", len(z) , " coups et ",len(seen)," noeuds explorés")
            	break
            for move, action in node.transitions:
                child = Node(move(), node, action)
                if profondeur(child)==4:
                    break
                if child.state not in seen:
                    queue.append(child)
                    seen.add(child.state)
        print("pas de solution trouvée avec ",len(seen)," noeuds explorés")

    
    def afficher(self , p , i=1):
    	node = p[0]
    	p=p[1:]
    	x=node.puzzle.convL()
    	print("permuation n°",i," : ",x)
    	node.puzzle.afficher2(x)
    	if p:
            self.fenetre.after(1500, self.afficher, p, i+1)
    	else :
        	print("Succes")


class Puzzle:

    def __init__(self, board , root , Lph):
        self.board = board
        self.can = root
        self.Lph = Lph

    @property
    def estEtatFinal(self):
        if self.board==[[1,2,3],[8,0,4],[7,6,5]]:
            return True
        return False


    @property 
    def transitions(self):
        def create_move(c1, c2):
            return lambda: self.permuter(c1, c2)

        moves = []
        for i, j in itertools.product(range(3),
                                      range(3)):
            direcs = {'R':(i, j-1),
                      'L':(i, j+1),
                      'D':(i-1, j),
                      'U':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < 3 and c < 3 and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves



    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board,self.can,self.Lph)

    def permuter(self, c1, c2):
        copy = self.copy()
        i, j = c1
        r, c = c2
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def afficher2 (self,liste1):
        "afficher les images sur le canvas"
        for k in range(len(liste1)) :
            eff =self.can.create_image((30+ 150*(k % 3)), 30+(150*( k // 3)), anchor=NW, image=self.Lph[0])
            aff =self.can.create_image((30+ 150*(k % 3)), 30+(150*( k // 3)), anchor=NW ,image = self.Lph[liste1[k]])

    def pprint(self):
        for row in self.board:
            print(row)
        print()

    def convL(self):
    	L=[]
    	for row in self.board:
    		L.extend(row)
    	return L 

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row


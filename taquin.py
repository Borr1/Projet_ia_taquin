from tkinter import * 
from resolution import *

global puzzl ,vals

board =etat_depart()
vals=[]
for row in board:
    vals.extend(row)
print(vals)
fenetre = Tk()
photos=[]
for i in range(9):
	photos.append(PhotoImage(file=r"C:\Users\Borr\Documents\Projet_ia_taquin\img"+'\\'+str(i)+".png"))
can=Canvas( width=540,height=540,bg='white')
can.pack( side =TOP, padx =20, pady =20)
fenetre['bg']='white'
fenetre.title (' TP JEUX DE REFLEXION : JEU DE TAQUIN')

puzzl = Puzzle(board,can,photos)
s = Resolution(puzzl,fenetre)


menubar = Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Quitter", command=fenetre.quit)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Recherche en largeur", command=s.recherche_largeur)
menu2.add_command(label="Recherche en profondeur", command=s.recherche_profondeur)
menu2.add_command(label="Recherche en profondeur limite : N=3", command=s.recherche_prof_lim)
menu2.add_command(label="Heuristique A *", command=s.recherche_heuristique)
menubar.add_cascade(label="Résoudre", menu=menu2)
fenetre.config(menu=menubar)

for k in range(len(photos)) :
    eff = can.create_image((30+ 150*(k % 3)), 30+(150*( k // 3)), anchor=NW, image=photos[0])
    aff = can.create_image((30+ 150*(k % 3)), 30+(150*( k // 3)), anchor=NW ,image = photos[vals[k]])
can.pack()
fenetre.mainloop()
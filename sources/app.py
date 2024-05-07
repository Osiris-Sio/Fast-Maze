# -*- coding: utf-8 -*-

'''
-> Fast Maze

Studio : I.V.L Games (Innovation, Vision and Liberty Games)
Auteur : AMEDRO Louis (alias Osiris Sio)

licence CC BY SA
''' 

######################################################
### Importation Module :
######################################################

import pyxel, random, time

######################################################
### Classe Personnage :
######################################################

class Personnage() :
    
    def __init__(self):
        #Position :
        self.x = 160
        self.y = 37
        #Apparence :
        self.apparence = 0
        
    ###Accesseur :
    
    def acc_x(self):
        return self.x
    
    def acc_y(self):
        return self.y
    
    def acc_apparence(self):
        return self.apparence
    
    ###Changement apparence :
    
    def changement_apparence(self, valeur) :
        self.apparence += valeur
    
    ###Placement :
    
    def placer_menu(self):
        self.x = 160
        self.y = 37
        
    def placer_partie(self):
        self.x = 96
        self.y = 20
        
    ###Mouvements :
    
    def gauche(self, vitesse = 1):
        self.x -= vitesse
        
    def droite(self, vitesse = 1):
        self.x += vitesse
        
    def haut(self, vitesse = 1):
        self.y -= vitesse
        
    def bas(self, vitesse = 1):
        self.y += vitesse
        
    ###Affichage :
    
    def afficher(self):
        pyxel.blt(self.x, self.y, 1, 0, 8 * self.apparence, 8, 8, 0)
   
######################################################
### Classe Labyrinthe :
######################################################
        
class Labyrinthe() :
    
    ##############################################################################
    ### Fonctions de la classe :
    ##############################################################################
        
    def lire(nom_fichier): 
        '''
        Auteur : Christophe Mieszczak
        Lit le fichier (.txt) passé en paramètre et renvoie son contenu.
        Ce n'est pas une méthode mais une fonction de la classe !
        : param nom_fichier (str)
        return (list), un tableau avec chaque élément, une ligne du fichier (.txt).
        '''
        #Précondition :
        assert isinstance(nom_fichier, str), 'nom_fichier doit être une chaîne !'
        #Code :
        try :
            # ouvre un canal en lecture vers text.txt :
            lecture = open(nom_fichier, 'r',encoding = 'utf_8') 
        except FileNotFoundError :
            raise # renvoie une erreur si le fichier n'existe pas
        # stocke toutes les lignes du fichier dans la liste toutes_les_lignes :
        toutes_les_lignes = lecture.readlines() 
        lecture.close()
        return toutes_les_lignes
    
    def generer_laby(toutes_les_lignes) :
        '''
        Auteur : CAPPONI DELY Arthur
        Renvoie une liste de listes modélisant le labyrinthe.
        Ce n'est pas une méthode mais une fonction de la classe !
        : param toutes_les_lignes (list), un tableau avec chaque élément, une ligne du fichier (.txt) lu par la méthode lire(nom_fichier).
        : return (list), un tableau contenant des chaines de caractères qui correspondent à une ligne du fichier (.txt).
        
        >>> toutes_les_lignes = Labyrinthe.lire('lab1.txt')
        >>> Labyrinthe.generer_laby(toutes_les_lignes)
        [['#', '#', '#', '#', '#', '#', '#'], ['#', 'X', '#', ' ', ' ', ' ', 'S'], ['#', ' ', '#', ' ', '#', '#', '#'], ['#', ' ', '#', ' ', ' ', ' ', '#'], ['#', ' ', '#', '#', '#', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', '#'], ['#', '#', '#', '#', '#', '#', '#']]
        '''
        #Précondition :
        assert isinstance(toutes_les_lignes, list), 'le paramètre doit être un tableau de tableaux.'
        #Code :
        lab = [] # Création d'un tableau.
        for ligne in toutes_les_lignes : # Pour les lignes dans toutes les lignes du labyrinthe.
            ligne_lab = [] # On créé un tableau de ligne. 
            for carac in ligne : # Pour les caractères (str) dans la ligne.
                if carac != '\n' : # Si str n'est pas égal au str '\n'(passer à la ligne du dessous).
                    ligne_lab.append(carac) # On ajoute le str dans le tableau de ligne.
            lab.append(ligne_lab) # On ajoute la ligne dans le tableau labyrinthe.
        return lab # Renvoie le labyrinthe.
    
    ##############################################################################
    ### Accesseurs :
    ##############################################################################
    
    def acc_lab(self, x, y) :
        '''
        Auteur : CAPPONI DELY Arthur
        Renvoie le contenu (`#` ou ' ' ou 'X' ou 'S') du labyrinthe aux coordonnées passé en paramètre.
        : params 
            x (int)
            y (int)
        : return (str)
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.acc_lab(1, 4)
        ' '
        >>> l.acc_lab(2, 2)
        '#'
        '''
        #Préconditions:
        assert isinstance(x, int), 'x doit être un entier positif.'
        assert isinstance(y, int), 'y doit être un entier positif.'
        #Code :
        return self.lab[y][x] # Renvoie l'élément contenu de la case aux coordonnées x, y.

    def acc_position_joueur(self):
        '''
        Auteur : AMEDRO Louis
        Renvoie les coordonnées x et y du joueur dans le labyrinthe.
        : return (tuple)
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.acc_position_joueur()
        (1, 1)
        >>> l.mut_lab(1, 1, ' ')
        >>> l.acc_position_joueur()
        False
        >>> l.mut_lab(1, 2, 'X')
        >>> l.acc_position_joueur()
        (1, 2)
        '''
        position_joueur = False #Définit la position du joueur en Faux (n'a pas de position)
        y = -1 #Définit l'indice y en -1
        while y < len(self.lab) - 1 and not position_joueur : #Tant que la recherche du joueur n'a pas dépassé chaque ligne du labyrinthe et que les coordonnées de joueur n'est pas définit (qu'il est en Faux), alors :
            y += 1 #Augmente la recherche de la ligne de 1 (ligne à ligne du labyrinthe)
            x = 0 #Défini x à 0.
            while x <= len(self.lab[y]) - 1 and not position_joueur : #Tant que la recherche du joueur dans la ligne y n'est pas dépassé (pour chaque élément) et que les coordonnées du joueur n'est pas définit (qu'il est en Faux), alors :
                if self.acc_lab(x, y) == 'X' : #Si l'élément de coordonnées (x, y) dans le labyrinthe est le caractère du joueur ('X') :
                    position_joueur = (x, y) #La position devient un tuple comprenant les coordonnées du joueur (x, y)
                x += 1 #Sinon, augmente x de 1.
        return position_joueur #Renvoie la position du joueur (x, y)

    def acc_position_sortie(self):
        '''
        Auteur : AMEDRO Louis
        Renvoie les coordonnées x et y de la sortie dans le labyrinthe.
        : return (tuple)
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.acc_position_sortie()
        (6, 1)
        >>> l.mut_lab(6, 1, 'X')
        >>> l.acc_position_sortie()
        False
        >>> l.mut_lab(5, 1, 'S')
        >>> l.acc_position_sortie()
        (5, 1)
        '''
        position_sortie = False #Définit la position de la sortie en Faux (n'a pas de position)
        y = -1 #Définit l'indice y en -1
        while y < len(self.lab) - 1 and not position_sortie : #Tant que la recherche de la sortie n'a pas dépassé chaque ligne du labyrinthe et que les coordonnées de la sortie n'est pas définit (qu'il est en Faux), alors :
            y += 1 #Augmente la recherche de la ligne de 1 (ligne à ligne du labyrinthe)
            x = 0 #Défini x à 0.
            while x <= len(self.lab[y]) - 1 and not position_sortie : #Tant que la recherche de la sortie dans la ligne y n'est pas dépassé (pour chaque élément) et que les coordonnées de la sortie n'est pas définit (qu'il est en Faux), alors :
                if self.acc_lab(x, y) == 'S' : #Si l'élément de coordonnées (x, y) dans le labyrinthe est le caractère du joueur ('X') :
                    position_sortie = (x, y) #La position devient un tuple comprenant les coordonnées de la sortie (x, y)
                x += 1 #(Sinon) augmente x de 1.
        return position_sortie #Renvoie la position de la sortie (x, y)
    
    ##############################################################################
    ### Initialisation :
    ##############################################################################
    
    def __init__(self, nom_fichier):
        '''
        Auteur : AMEDRO Louis
        Initialise le labyrinthe (objet) à partir du fichier (.txt) passé en paramètre.
        Le labyrinthe a pour attributs :
            -> lab, une liste de listes pour les coordonnées de chaque mur, joueur et sortie (x, y).
            -> position_joueur, un tuple donnant les coordonnées du joueur 'X' (x, y).
            -> position_sortie, un tuple donnant les coordonnées de la sortie 'S' (x, y).
        : param nom_fichier (str)
        : pas de return, on initialise.
        '''
        #Précondition :
        assert isinstance(nom_fichier, str), 'Le paramètre doit être une chaine de caractère (str).'
        #Code :
        self.lab = Labyrinthe.generer_laby(Labyrinthe.lire(nom_fichier)) #Défini l'attribut lab qui sera une liste de listes généré grâce à nom_fichier passé en paramètre et aux fonctions de la classe (generer_laby et lire)
        self.position_joueur = self.acc_position_joueur() #Défini l'attribut position_joueur qui sera un tuple (x, y) grâce à la méthode acc_position_joueur
        self.position_sortie = self.acc_position_sortie() #Défini l'attribut position_sortie qui sera un tuple (x, y) grâce à la méthode acc_position_sortie
        
    ##############################################################################
    ### __str__ et __repr__ :
    ##############################################################################

    def __str__(self) :
        '''
        Auteur : AMEDRO Louis
        Renvoie une chaine pour afficher le labyrinthe, le joueur et la sortie également.
        : return (str)
        '''
        chaine = '' #Définit une chaine de caractère qui contiendra toutes les lignes du labyrinthe à afficher.
        for ligne in self.lab : #Pour chaque ligne du labyrinthe :
            ligne_chaine = '' #Définit une chaine de caractères qui sera ajouté ensuite à chaine pour chaque ligne du labyrinthe. 
            for carac in ligne : #Pour chaque element/caractère (str) dans la ligne du labyrinthe :
                ligne_chaine += carac #Ajoute à ligne_chaine le caractère (str)
            chaine = chaine + ligne_chaine + '\n' #A chaque ligne finit, on ajoute à chaine -> ligne_chaine et un retour à la ligne (\n)
        return chaine #Renvoi le labyrinthe en affichage dans la console.
    
    def __repr__(self) :
        '''
        Auteur : CAPPONI DELY Arthur
        Renvoie une chaine pour la description du labyrinthe.
        : return (str)
        '''
        return ('Un labyrinthe comprenant un joueur (X) et une sortie (S).') # Renvoie la description du labyrinthe dans la console.
    
    ##############################################################################
    ### Mutateurs :
    ##############################################################################
    
    def mut_lab(self, x, y, carac) :
        '''
        Auteur : AMEDRO Louis
        Modifie le labyrinthe en écrivant le caractère carac passé en paramètre aux 
        coordonnées x, y passé également en paramètre.
        : params
            x (int)
            y (int)
            carac (str), de longueur 1
        : pas de return, modifie l'attribut lab
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.acc_lab(1, 4)
        ' '
        >>> l.mut_lab(1, 4, '#')
        >>> l.acc_lab(1, 4)
        '#'
        '''
        #Préconditions :
        assert isinstance(x, int), 'x doit être un entier (int).'
        assert isinstance(y, int), 'y doit être un entier (int).'
        assert isinstance(carac, str) and len(carac) == 1, 'carac doit être une chaine de caractère (str) de longueur 1.'
        #Code :
        self.lab[y][x] = carac #Change à la liste d'indice y et d'élément d'indice x le caractère passé en paramètre.
        
    ##############################################################################
    ### Méthodes :
    ##############################################################################
        
    def deplacer(self, direction):
        '''
        Auteur : AMEDRO Louis
        Modifie les coordonnées du joueur 'X' dans la direction souhaitée si possible.
        : param direction (str), 'z' ou 'q' ou 's' ou 'd'
        : pas de return, on change l'attribut position_joueur.
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.acc_position_joueur()
        (1, 1)
        >>> l.deplacer('s')
        >>> l.acc_position_joueur()
        (1, 2)
        '''
        #Précondition :
        assert isinstance(direction, str) and direction in ['z', 'q', 's', 'd'], 'Le paramètre doit être une chaine de caractère (str).'
        #Code :
        if self.est_possible(direction) : #Si le déplacement vers la direction passé en paramètre est possible, alors :
            self.mut_lab(self.position_joueur[0], self.position_joueur[1], ' ') #Change le caractère du labyrinthe aux coordonnées du joueur (x, y) en un chemin/caractère vide.
            self.position_joueur = self.future_position(direction) #Change la position du joueur en sa nouvelle position dans la direction souhaité.
            self.mut_lab(self.position_joueur[0], self.position_joueur[1], 'X') #Change le caractère du labyrinthe aux coordonnées du joueur (x, y) en 'X'.
            
    def est_gagne(self) :
        '''
        Auteur : CAPPONI DELY Arthur
        Renvoie True si la partie est finie, False sinon.
        : return (boolean)
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.est_gagne() 
        False
        >>> l.position_joueur = (6, 1)
        >>> l.est_gagne()
        True
        '''
        return self.position_joueur == self.position_sortie # Renvoie True si la position du joueur est égal à la position de la sortie. 
    
    def est_possible(self, direction):
        '''
        Auteur : CAPPONI DELY Arthur
        Renvoie True si le déplacement dans la direction est possible (c'est à dire s'il n'y a pas de mur à la prochaine position/coordonnées du joueur),
        False sinon.
        : param direction (str), 'z' ou 'q' ou 's' ou 'd'
        : return (boolean)
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.est_possible('z')
        False
        >>> l.est_possible('s')
        True
        '''
        #Précondition :
        assert isinstance(direction, str) and direction in ['z', 'q', 's', 'd'], 'Le paramètre doit être une chaine de caractère (str).'
        #Code :
        future_position = self.future_position(direction) # On créé une variable future_position qui est égal à la méthode future_position.
        return self.acc_lab(future_position[0], future_position[1]) != '#' # Renvoie le contenu de la case pour la future position.
        
    def future_position(self, direction):
        '''
        Auteur : AMEDRO Louis
        Renvoie les coordonnées de la prochaine position du joueur.
        S'il se déplaçait dans la direction passé en paramètre.
        : param direction (str), 'z' ou 'q' ou 's' ou 'd'
        : return (tuple)
        
        >>> l = Labyrinthe('lab1.txt')
        >>> l.acc_position_joueur()
        (1, 1)
        >>> l.future_position('s')
        (1, 2)
        '''
        #Précondition :
        assert isinstance(direction, str) and direction in ['z', 'q', 's', 'd'], 'Le paramètre doit être une chaine de caractère (str).'
        #Code :
        directions = { 'z' : (0, -1), #en haut
                       's' : (0, 1),  #en bas
                       'd' : (1, 0),  #à droite
                       'q' : (-1, 0)  #gauche
                     }
        return (directions[direction][0] + self.position_joueur[0], directions[direction][1] + self.position_joueur[1]) #Renvoie, si on admet la direction, la nouvelle position du joueur en fonction de la direction passé en paramètre en ajoutant la valeur de x et de y pas la valeur du x et du y du dictionnaire de direction.       
        
######################################################
### Classe Jeu :
######################################################

class Jeu() :
    
    def __init__(self) :
        
        #Intro :
        self.intro = True
        self.temps_commence_intro = time.time()
        
        #Menu :
        self.menu = False
        self.clavier = True
        
        #Personnage :
        self.longueur = 5
        self.hauteur = 3
        self.personnage = Personnage()
        
        #Partie :
        self.nombre_deplacements = 0
        self.fin_partie = False
        
        #Initialisation de la fenêtre Pyxel:
        pyxel.init(200, 92, title='Fast Maze', fps=60, capture_scale=3, capture_sec=0)
        pyxel.mouse(True)
        pyxel.load('ressources.pyxres')
        pyxel.playm(0)
        pyxel.run(self.calculs, self.affichages)
    
    ######################################################
    ### Calculs :
    ######################################################
    
    ###Intro :
    
    def finir_intro(self):
        if time.time() - self.temps_commence_intro >= 2 :
            self.intro = False
            self.menu = True
    
    ###Boutons :
    
    def boutons_menu(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            
            #Jouer :
            if 76 <= pyxel.mouse_x <= 124 and 65 <= pyxel.mouse_y <= 81:
                self.menu = False
                self.temps_commence = time.time()
                self.personnage.placer_partie()
            
            #Plateforme :
            elif 179 <= pyxel.mouse_x <= 195 and 5 <= pyxel.mouse_y <= 21 :
                self.clavier = not self.clavier
                pyxel.mouse(self.clavier)
                
            ###Longueur :    
            #Gauche :
            if 18 <= pyxel.mouse_x <= 26 and 35 <= pyxel.mouse_y <= 43 and 2 < self.longueur :
                self.longueur -= 1
            
            #Droite :
            elif 35 <= pyxel.mouse_x <= 43 and 35 <= pyxel.mouse_y <= 43 and self.longueur < 6 :
                self.longueur += 1
                
            ###Hauteur :
            #Gauche :
            if 18 <= pyxel.mouse_x <= 26 and 60 <= pyxel.mouse_y <= 68 and 2 < self.hauteur :
                self.hauteur -= 1
            
            #Droite :
            elif 35 <= pyxel.mouse_x <= 43 and 60 <= pyxel.mouse_y <= 68 and self.hauteur < 5 :
                self.hauteur += 1
               
            ###Personnage :                        
            #Gauche :
            elif 152 <= pyxel.mouse_x <= 160 and 55 <= pyxel.mouse_y <= 63 and 0 < self.personnage.acc_apparence() :
                self.personnage.changement_apparence(-1)
                
            #Droite :
            elif 168 <= pyxel.mouse_x <= 176 and 55 <= pyxel.mouse_y <= 63 and self.personnage.acc_apparence() < 11 :
                self.personnage.changement_apparence(1)
    
    def bouton_retour(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            if 10 <= pyxel.mouse_x <= 58 and 69 <= pyxel.mouse_y <= 85 :
                self.tab_balles = []
                self.personnage.placer_menu()
                self.score = 0
                self.menu = True
                self.fin_partie = False
                    
    ###Contrôles :
                    
    def controle_clavier_manette(self):
        if (pyxel.btnr(pyxel.KEY_Q) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.personnage.acc_x() > 0:
            self.personnage.gauche()
        if (pyxel.btnr(pyxel.KEY_D) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.personnage.acc_x() < 192 :
            self.personnage.droite()
        if (pyxel.btnr(pyxel.KEY_Z) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.personnage.acc_y() > 0:
            self.personnage.haut()
        if (pyxel.btnr(pyxel.KEY_S) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.personnage.acc_y() < 52 :
            self.personnage.bas()
        
    def controle_tactile(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            #Gauche :
            if 136 <= pyxel.mouse_x <= 152 and 76 <= pyxel.mouse_y <= 92 and self.personnage.acc_x() > 0:
                self.personnage.gauche()
            #Droite :
            if 168 <= pyxel.mouse_x <= 184 and 76 <= pyxel.mouse_y <= 92 and self.personnage.acc_x() < 192:
                self.personnage.droite()
            #Haut :
            if 152 <= pyxel.mouse_x <= 168 and 60 <= pyxel.mouse_y <= 76 and self.personnage.acc_y() > 0:
                self.personnage.haut()
            #Bas :
            if 152 <= pyxel.mouse_x <= 168 and 76 <= pyxel.mouse_y <= 92 and self.personnage.acc_y() < 52:
                self.personnage.bas()
    
    def controle_personnage(self):
        if self.clavier :
            self.controle_clavier_manette()
        else :
            self.controle_tactile()
    
    ###Calculs :
       
    def calculs(self) :
        
        ### Intro :
        if self.intro :
            self.finir_intro()
        
        ### Menu :
        elif self.menu :
            self.boutons_menu()
        
        ### Partie :
        else :
            if not self.est_fini() :
                self.controle_personnage()
                self.actions_balles()
                self.prendre_piece()
                self.temps = int(time.time() - self.temps_commence)
            self.bouton_retour()
            
    ######################################################
    ### Affichages :
    ######################################################
    
    def afficher_intro(self) :
        pyxel.blt(84, 38, 0, 0, 56, 32, 16)
        pyxel.text(100, 55, 'Games', 7)
    
    def afficher_menu(self):
        #Version :
        pyxel.text(2, 85, '0.0.1', 7)
        
        #Titre :
        pyxel.rect(81, 18, 39, 9, 9)
        pyxel.rectb(81, 18, 39, 9, 7)
        pyxel.text(83, 20, 'Fast Maze', 7)
        
        ###Boutons Longueur:
        pyxel.text(15, 27, 'Longueur', 7)
        pyxel.text(29, 36, str(self.longueur), 7)
        
        #Gauche :
        if 2 < self.longueur :
            pyxel.blt(18, 35, 0, 0, 48, 8, 8)
        else :
            pyxel.blt(18, 35, 0, 16, 48, 8, 8)
        
        #Droite :
        if self.longueur < 6 :
            pyxel.blt(35, 35, 0, 8, 48, 8, 8)
        else :
            pyxel.blt(35, 35, 0, 24, 48, 8, 8)
            
        ###Boutons Hauteur:
        pyxel.text(17, 52, 'Hauteur', 7)
        pyxel.text(29, 61, str(self.hauteur), 7)
        
        #Gauche :
        if 2 < self.hauteur :
            pyxel.blt(18, 60, 0, 0, 48, 8, 8)
        else :
            pyxel.blt(18, 60, 0, 16, 48, 8, 8)
        
        #Droite :
        if self.hauteur < 5 :
            pyxel.blt(35, 60, 0, 8, 48, 8, 8)
        else :
            pyxel.blt(35, 60, 0, 24, 48, 8, 8)
        
        ###Boutons Personnage :
        #Gauche :
        if 0 < self.personnage.acc_apparence() :
            pyxel.blt(152, 55, 0, 0, 48, 8, 8)
        else :
            pyxel.blt(152, 55, 0, 16, 48, 8, 8)
        
        #Droite :
        if self.personnage.acc_apparence() < 11 :
            pyxel.blt(168, 55, 0, 8, 48, 8, 8)
        else :
            pyxel.blt(168, 55, 0, 24, 48, 8, 8)
        
        #Boutons Jouer:
        pyxel.blt(76, 65, 0, 0, 0, 48, 16)
        
        #Bouton Plateforme :
        dic = {
            True : 0,
            False : 16
        }
        pyxel.blt(179, 5, 0, dic[self.clavier], 16, 16, 16)
        
    def afficher_partie(self):      
        #Information :
        pyxel.rect(0, 60, 200, 33, 5)
        pyxel.rectb(0, 60, 200, 33, 7)
        pyxel.text(50, 70, 'Nombre Deplacements : ' + str(self.nombre_deplacements), 7)
        
        #Bouton Retour :
        pyxel.blt(10, 69, 0, 0, 32, 48, 16)
        
        #Touche :
        if self.clavier :
            pyxel.blt(136, 60, 0, 0, 104, 48, 32, 0)
        else :
            pyxel.blt(136, 60, 0, 0, 72, 48, 32, 0)
                
    def afficher_fin(self):
        pyxel.text(78, 18, 'Tu es\n  Sorti !', 7)
        
    def affichages(self):
        #Fond Noir :
        pyxel.cls(0)
        
        if self.intro :
            self.afficher_intro()
        
        ### Menu :
        elif self.menu :
            self.afficher_menu()
            self.personnage.afficher()
        
        ### Partie :
        else :
            self.afficher_partie()
            if not self.fin_partie :
                self.piece.afficher()
                self.personnage.afficher()
                self.afficher_balles()
            else :
                self.afficher_fin()
                
Jeu() #Lancement du jeu automatiquement
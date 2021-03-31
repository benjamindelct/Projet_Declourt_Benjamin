import numpy as np
import pygame
import sys
import math


class Game_JvsJ:
    def __init__(self):
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.NB_LIGNE = 6
        self.NB_COLONNE = 7
        self.TAILLE_CARREE = 100
        self.width = self.NB_COLONNE * self.TAILLE_CARREE
        self.height = (self.NB_LIGNE + 1) * self.TAILLE_CARREE
        self.SIZE = (self.width, self.height)
        self.RAYON = int(self.TAILLE_CARREE / 2 - 5)
        self.plateau = np.zeros((self.NB_LIGNE, self.NB_COLONNE))
        self.jeu = True
        self.tour = 0

    # Place un jeton sur le plateau
    def placer_jeton(self, ligne, colonne, jeton):
        self.plateau[ligne][colonne] = jeton

    # Vérifie que la colonne ne soit pas remplis
    def est_position_valide(self, colonne):
        return self.plateau[self.NB_LIGNE - 1][colonne] == 0

    # récupère la hauteur à laquelle un jeton peut être déposé
    def get_hauteur_ligne_dispo(self, colonne):
        for l in range(self.NB_LIGNE):
            if self.plateau[l][colonne] == 0:
                return l

    # affiche le plateau de jeu (on doit l'inverser les matrice numpy commence par le bas)
    def print_plateau(self):
        print(np.flip(self.plateau, 0))

    # Vérification des lignes/colonnes/diagonales gagnante selon le joueur
    def verification_jeton_gagnant(self, jeton):
        # Vérification horizontale
        for c in range(self.NB_COLONNE - 3):
            for r in range(self.NB_LIGNE):
                if self.plateau[r][c] == jeton and self.plateau[r][c + 1] == jeton and self.plateau[r][c + 2] == jeton and self.plateau[r][c + 3] == jeton:
                    return True

        # Vérification verticale
        for c in range(self.NB_COLONNE):
            for r in range(self.NB_LIGNE - 3):
                if self.plateau[r][c] == jeton and self.plateau[r + 1][c] == jeton and self.plateau[r + 2][c] == jeton and self.plateau[r + 3][c] == jeton:
                    return True

        # Vérification diagonale (gauche à droite)
        for c in range(self.NB_COLONNE - 3):
            for r in range(self.NB_LIGNE - 3):
                if self.plateau[r][c] == jeton and self.plateau[r + 1][c + 1] == jeton and self.plateau[r + 2][c + 2] == jeton and self.plateau[r + 3][c + 3] == jeton:
                    return True

        # Vérification diagonale (droite à gauche)
        for c in range(self.NB_COLONNE - 3):
            for r in range(3, self.NB_LIGNE):
                if self.plateau[r][c] == jeton and self.plateau[r - 1][c + 1] == jeton and self.plateau[r - 2][c + 2] == jeton and self.plateau[r - 3][c + 3] == jeton:
                    return True

    def draw_plateau(self, ecran):
        for c in range(self.NB_COLONNE):
            for r in range(self.NB_LIGNE):
                pygame.draw.rect(ecran, self.BLUE, (c * self.TAILLE_CARREE, r * self.TAILLE_CARREE + self.TAILLE_CARREE, self.TAILLE_CARREE,self.TAILLE_CARREE))
                pygame.draw.circle(ecran, self.BLACK, (int(c * self.TAILLE_CARREE + self.TAILLE_CARREE / 2), int(r * self.TAILLE_CARREE + self.TAILLE_CARREE + self.TAILLE_CARREE / 2)), self.RAYON)

        for c in range(self.NB_COLONNE):
            for r in range(self.NB_LIGNE):
                if self.plateau[r][c] == 1:
                    pygame.draw.circle(ecran, self.RED, (int(c * self.TAILLE_CARREE + self.TAILLE_CARREE / 2), self.height - int(r * self.TAILLE_CARREE + self.TAILLE_CARREE / 2)), self.RAYON)
                elif self.plateau[r][c] == 2:
                    pygame.draw.circle(ecran, self.YELLOW, (int(c * self.TAILLE_CARREE + self.TAILLE_CARREE / 2), self.height - int(r * self.TAILLE_CARREE + self.TAILLE_CARREE / 2)), self.RAYON)
        pygame.display.update()

    def start(self):
        print("--- Mode Game Joueur vs Joueur ---")
        pygame.init()
        ecran = pygame.display.set_mode(self.SIZE)
        font = pygame.font.SysFont("monospace", 75)
        while self.jeu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(ecran, self.BLACK, (0, 0, self.width, self.TAILLE_CARREE))
                    posx = event.pos[0]

                    # affiche un jeton au dessus du plateau de la couleur du joueur qui doit jouer
                    if self.tour == 0:
                        pygame.draw.circle(ecran, self.RED, (posx, int(self.TAILLE_CARREE / 2)), self.RAYON)
                    else:
                        pygame.draw.circle(ecran, self.YELLOW, (posx, int(self.TAILLE_CARREE / 2)), self.RAYON)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(ecran, self.BLACK, (0, 0, self.width, self.TAILLE_CARREE))

                    # Si tour = 0, Joueur 1 joue
                    if self.tour == 0:
                        posx = event.pos[0]
                        colonne = int(math.floor(posx / self.TAILLE_CARREE))

                        if self.est_position_valide(colonne):
                            ligne = self.get_hauteur_ligne_dispo(colonne)
                            self.placer_jeton(ligne, colonne, 1)

                            if self.verification_jeton_gagnant(1):
                                label = font.render("Joueur 1 Gagne!!", True, self.RED)
                                ecran.blit(label, (40, 10))
                                self.jeu = False

                    # Sinon, Joueur 2 joue
                    else:
                        posx = event.pos[0]
                        colonne = int(math.floor(posx / self.TAILLE_CARREE))

                        if self.est_position_valide(colonne):
                            ligne = self.get_hauteur_ligne_dispo(colonne)
                            self.placer_jeton(ligne, colonne, 2)

                            if self.verification_jeton_gagnant(2):
                                label = font.render("Joueur 2 Gagne!!", True, self.YELLOW)
                                ecran.blit(label, (40, 10))
                                self.jeu = False

                    self.print_plateau()
                    self.draw_plateau(ecran)

                    if self.tour == 0:
                        self.tour = 1
                    else:
                        self.tour = 0

        pygame.time.wait(1000)
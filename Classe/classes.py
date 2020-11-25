# -*- coding: utf-8 -*-

import random
import json
from datetime import date
import csv


def aleatoire(questions, nbr_questions):
    """
    Renvoie x questions aléatoirement provenant de préférence d'un dictionnaire ou d'une
    liste, où x est précisé à l'appel de la fonction.

    Post : les questions sont renvoyées dans une liste.
    """
    liste = []
    compteur = 0
    liste_questions = list(questions)
    while compteur < nbr_questions:
        x = random.randint(0, len(liste_questions) - 1)
        if liste_questions[x] not in liste:
            liste.append(liste_questions[x])
            compteur += 1

    return liste


def recup_donnees_fichier(fichier_a_ouvrir):
    """
    Récupère les informations d'un fichier pour pouvoir les utiliser.

    Pré : fichier csv.

    Post : retourne les informations sour forme de liste.
    """
    try:
        with open(fichier_a_ouvrir) as file:
            lecture = csv.reader(file)
            liste = list(map(lambda x: x, lecture))
            del liste[0]
            return liste

    except FileNotFoundError:
        print('Fichier introuvable.')
    except IOError:
        print('Erreur IO.')


def separation():
    """
    Crée une ligne de séparation afin d'avoir un écran plus clair, avec un retour
    chariot au dessus et en dessous.
    """
    print("                                         ")
    print("-----------------------------------------")
    print("                                         ")


##############################################################################

class Bibliotheque:
    def __init__(self, nom_bibliotheque, nom_fichier_bibliotheque):
        self.nom_bibliotheque = nom_bibliotheque
        self.__nom_fichier_bibliotheque = nom_fichier_bibliotheque
        self.liste_themes = []
        self.dictionnaire_themes = {}
        self.question = Question("cc")

    def retourne_fichier_bibliotheque(self):
        return recup_donnees_fichier(self.__nom_fichier_bibliotheque)

    def creation_theme(self, nom_theme):
        """
        Crée un objet Theme et l'ajoute à la liste de l'objet Bibliotheque.
        """
        objet_t = Theme(nom_theme)
        self.liste_themes.append(objet_t)

    def retourne_themes(self):
        """
        Renvoie tous les objets Theme que l'objet Bibliotheque contient dans une liste.

        Post : renvoie les thèmes dans une liste.
        """
        liste = []
        for theme in self.liste_themes:
            liste.append(theme.retourne_theme())
        return liste

    def recuperer_theme(self, nom_theme):
        """
        Retourne l'objet Theme sur base de son nom ou du nom de son fichier.
        """
        for theme in range(len(self.liste_themes)):
            if self.liste_themes[theme].retourne_theme()[0] == nom_theme or self.liste_themes[theme].retourne_theme()[
                1] == nom_theme:
                return self.liste_themes[theme]

    def retourne_total(self):
        """
        Renvoie les questions et réponses de tous les objet Theme de l'objet Bibliotheque.

        Post : renvoie un dictionnaire, avec comme clé le nom du thème (pas le nom du fichier).
        """
        for theme in self.liste_themes:
            self.dictionnaire_themes[theme.retourne_theme()[0]] = theme.retourne_question_theme()
        return self.dictionnaire_themes


##############################################################################

class Theme:
    def __init__(self, nom_fichier):
        self.__nom_theme = nom_fichier[:-4]
        self.__nom_fichier = "fichier/" + nom_fichier
        self.dictionnaire = {}
        self.__liste_questions = []

    def retourne_theme(self):
        """
        Renvoie le nom de l'objet Theme et le nom du fichier qui contient les questions
        de l'objet Theme.

        Post : renvoie les deux informations dans une liste.
        """
        return [self.__nom_theme, self.__nom_fichier]

    def retourne_question_theme(self):
        """
        Renvoie les questions et réponses de tous les objet Theme de l'objet Bibliotheque.

        Post : renvoie un dictionnaire.
        """
        return self.dictionnaire

    def recuperer_question(self, question_a_recuperer):
        """
        Retourne l'objet Theme sur base de son nom ou du nom de son fichier.
        """
        for question in range(len(self.__liste_questions)):
            if self.__liste_questions[question].retourne_question() == question_a_recuperer:
                return self.__liste_questions[question]

    def creation_question(self, nom_question, reponses):
        """
        Permet de créer un objet Question et de l'ajouter au dictionnaire de l'objet Theme.
        Ces informations sont rajoutées avec la question comme clé du dictionnaire et
        les réponses comme valeurs du dictionnaire.
        Crée également les objet Réponse pour pouvoir les rajouter dans le dictionnaire.
        """
        objet_q = Question(nom_question)
        objet_q.creation_reponses(reponses)
        self.dictionnaire[objet_q.retourne_question()] = objet_q.retourne_reponses_question()
        self.__liste_questions.append(objet_q)

    def ecriture_question(self, liste):
        try:
            with open(self.__nom_fichier, "a") as fichier:
                nouveau_fichier = csv.writer(fichier, quotechar=',')
                nouveau_fichier.writerow(liste)
        except FileNotFoundError:
            print('Fichier introuvable.')
        except IOError:
            print('Erreur IO.')

    def suppression_question(self, question):
        # objet_question = self.recuperer_question(question)
        # print(self.dictionnaire)
        del self.dictionnaire[question]
        try:
            with open(self.__nom_fichier, "w", newline='') as fichier:
                nouveau_fichier = csv.writer(fichier, quotechar=',', quoting=csv.QUOTE_MINIMAL)
                nouveau_fichier.writerow(["questions", "bonneReponse", "reponseA", "reponseB", "reponseC", "reponseD"])
                for question in self.dictionnaire:
                    reponses = self.dictionnaire[question]
                    nouveau_fichier.writerow([question, list(filter(lambda x: x[1] == True, reponses))[0][0],
                                              reponses[0][0], reponses[1][0], reponses[2][0], reponses[3][0]])

        except FileNotFoundError:
            print('Fichier introuvable.')
        except IOError:
            print('Erreur IO.')


##############################################################################

class Question():
    def __init__(self, nom_question):
        self.nom_question = nom_question
        self.liste_reponse = []

    def retourne_question(self):
        """
        Renvoie la question de l'objet Question.

        Post : renvoie une string.
        """
        return self.nom_question

    def retourne_reponses_question(self):
        """
        Renvoie les reponses de l'objet Question.

        Post : renvoie une liste de liste.
        """
        return self.liste_reponse

    def creation_reponses(self, reponses):
        """
        Permet de créer un objet Réponse et de l'ajouter à la liste de l'objet Question.
        """
        for reponse in reponses:
            objet_r = Reponse(reponse[0], reponse[1])
            self.liste_reponse.append(objet_r.retourne_reponse())


##############################################################################

class Reponse():
    def __init__(self, nom_reponse, type_bonne_reponse):
        self.__nom_reponse = nom_reponse
        self.__type_bonne_reponse = type_bonne_reponse

    def retourne_reponse(self):
        """
        Renvoie le nom de la reponse de l'objet Reponse ainsi que son type (vraie ou fausse).

        Post : renvoie une liste contenant les deux informations.
        """
        return [self.__nom_reponse, self.__type_bonne_reponse]


##############################################################################

class Utilisateur():
    def __init__(self, nom):
        self.__nom = nom

    @property
    def nom(self):
        """
        Permet d'accéder à l'attribut nom en dehors de l'objet Utilisateur.

        Post : retourne une string.
        """
        return self.__nom

    def init_resultats(self):
        """
        Initialise les thèmes de base pour le joueur.

        Post : renvoie les thèmes de base de l'application sous forme de dictionnaire
        (donc pas les thèmes que les utilisateurs auraient pu rajouter).
        """
        return {'geographie': [], 'math': []}

    def resultats(self, dico):
        """
        Affiche tout résultats confondus de l'utilisateur connecté.
        """
        for theme in dico[self.__nom]:
            print(theme, " : ")
            for score in dico[self.__nom][theme]:
                print("    ", score[0], "% - ", score[1])
            print("")

    def creation_manche(self, theme):
        """
        Crée un objet Manche et le lance.
        """
        self.__manche = Manche(theme)
        self.__manche.lancer_manche()


##############################################################################


class Manche():
    def __init__(self, theme):
        self.__theme = theme
        self.__nbr_questions = 0
        self.__pourcentage = 0
        self.__date = date.today().strftime('%d/%m/%Y')

    def lancer_manche(self):
        """
        Permet de lancer une manche, c'est à dire de répondre à des questions,
        puis de noter le score de cette manche de l'Utilisateur qui a lancé la manche.
        """
        liste_questions = librairie.retourne_total()[self.__theme]

        valid = False
        while True:
            try:
                nombre_questions = int(input("Combien de questions pour la partie ? (entrer un chiffre entre 1 et " +
                                             str(len(liste_questions)) + ") : "))
                if 0 < nombre_questions <= len(liste_questions):
                    break
                else:
                    print("Veuillez entrez un chiffre entre 1 et " + str(len(liste_questions)) + ".")
            except:
                print('Veuillez entrer un nombre naturel.')

        self.__nbr_questions = nombre_questions
        separation()

        liste_questions_aleatoires = aleatoire(liste_questions, self.__nbr_questions)
        points_joueur = 0
        for question in liste_questions_aleatoires:
            print(question)
            reponses = librairie.recuperer_theme(self.__theme).recuperer_question(question).retourne_reponses_question()
            for i in range(len(reponses)):
                print("    " + str(i + 1) + ". " + reponses[i][0])

            reponse_joueur = int(input("Entrer un chiffre de 1 à " + str(len(reponses)) + " : "))

            if reponses[reponse_joueur - 1][1]:
                print("\nCorrect !")
                points_joueur += 1
            else:
                print("\nFaux !")

            separation()

        print("Vous avez", points_joueur, "bonne(s) réponse(s) sur " + str(len(liste_questions_aleatoires)) + ".")
        self.__pourcentage = points_joueur / len(liste_questions_aleatoires) * 100

        self.ajout_score()

        separation()
        menu()

    def ajout_score(self):
        """
        Permet d'ajouter un score à l'objet Utilisateur.
        """
        try:
            with open('fichier/scores.json', 'r') as file:
                dico_python = json.load(file)
                dico_python[joueur.nom][self.__theme].append([round(self.__pourcentage, 2), self.__date])
            with open('fichier/scores.json', 'w') as fichier:
                dico_json = json.dumps(dico_python)
                fichier.write(dico_json)

        except FileNotFoundError:
            print('Fichier introuvable.')
        except IOError:
            print('Erreur IO.')


##initialisation
"""
Initalise les informations de l'application, telles que
la librairie, les thèmes, les questions et réponses.
Initialise ces informations en global pour que tout le monde
puisse y accéder de n'importe où.
"""
librairie = Bibliotheque("Application", "fichier/themes.csv")

themes = librairie.retourne_fichier_bibliotheque()
for theme in themes:
    for nom in theme:
        librairie.creation_theme(nom)

for theme_fichier in librairie.retourne_themes():
    liste_questions = recup_donnees_fichier(theme_fichier[1])
    for question in liste_questions:
        liste_reponses = []
        for reponse in range(2, len(question)):
            if question[reponse] == question[1]:
                liste_reponses.append([question[reponse], True])

            else:
                liste_reponses.append([question[reponse], False])
        librairie.recuperer_theme(theme_fichier[1]).creation_question(question[0], liste_reponses)


def introduction():
    """
    Lance l'application en demandant le pseudo du joueur.
    Si le joueur est déjà encodé dans la base, on affiche ses scores précédents.
    Si il n'est pas encore encodé, son pseudo est enregistré dans l'application.
    """
    try:
        with open('fichier/scores.json') as file:
            dictionnaire = json.load(file)

            if joueur.nom not in dictionnaire:
                dictionnaire[joueur.nom] = joueur.init_resultats()
                try:
                    with open('fichier/scores.json', 'w') as fichier:
                        nouveau_dictionnaire = json.dumps(dictionnaire)
                        fichier.write(nouveau_dictionnaire)

                except FileNotFoundError:
                    print('Fichier introuvable.')
                except IOError:
                    print('Erreur IO.')
                print("Bienvenue dans le jeu.")
            else:
                print("Vos scores précédents :\n")
                joueur.resultats(dictionnaire)
                separation()

    except FileNotFoundError:
        print('Fichier introuvable.')
    except IOError:
        print('Erreur IO.')


def jouer():
    """
    Selon le thème choisi par le joueur, la fonction lance une manche.
    """
    print("Thèmes : ")
    for i in range(len(librairie.retourne_themes())):
        print("    " + str(i + 1) + ". " + librairie.retourne_themes()[i][0])
    print("")

    question = "Choisir un thème (entre 1 et " + str(len(librairie.retourne_themes())) + ") : "
    choix_theme = int(input(question))
    separation()

    theme_manche = librairie.retourne_themes()[choix_theme - 1][0]
    joueur.creation_manche(theme_manche)


def ajouter_questions():
    """
    Ajoute une question et ses réponses dans le thème précisé (dans l'objet Bibliothèque
    et dans le fichier du thème précisé).
    """
    print("Thèmes : ")
    for i in range(len(librairie.retourne_themes())):
        print("    " + str(i + 1) + ". " + librairie.retourne_themes()[i][0])
    print("")
    choix_theme = input("Choisir un thème dans lequel rajouter une question (entre 1 et " + str(
        len(librairie.retourne_themes())) + ") : ")
    theme_a_modifier = librairie.recuperer_theme(librairie.retourne_themes()[int(choix_theme) - 1][0])
    separation()
    question = input("Entrez la question : ")
    print(
        "\nVous allez maintenant devoir entrer des réponses. Une seule réponse peut être bonne, les 3 autres doivent être fausses.")
    print("L'ordre n'a pas d'importance.\n")
    print("Lorsque vous ne voulez plus ajouter de réponse, tapez 'quitter' \n")

    liste_reponses = []
    reponse = ""
    for i in range(4):
        reponse = input("Entrez la réponse " + str(i + 1) + " : ")
        liste_reponses.append(reponse)

    bonne_reponse = int(input("\nQuelle réponse est la bonne ? (entrez le numéro de la réponse, entre 1 et 4) : ")) - 1

    # Ajout de la question et réponses dans l'objet Theme
    liste = []
    for reponse in liste_reponses:
        correction = False
        if reponse == liste_reponses[bonne_reponse]:
            correction = True
        liste.append([reponse, correction])
    theme_a_modifier.creation_question(question, liste)

    # Ajout de la question dans le fichier theme
    liste_reponses.insert(0, liste_reponses[bonne_reponse])
    liste_reponses.insert(0, question)
    theme_a_modifier.ecriture_question(liste_reponses)

    separation()

    refaire = input("Voulez-vous rajouter une nouvelle question ? (oui ou non) : ")
    if refaire == "oui":
        ajouter_questions()
    else:
        modifier()


def supprimer_questions():
    print("Thèmes : ")
    for i in range(len(librairie.retourne_themes())):
        print("    " + str(i + 1) + ". " + librairie.retourne_themes()[i][0])
    print("")
    choix_theme = input("Choisir un thème dans lequel supprimer une question (entre 1 et " + str(
        len(librairie.retourne_themes())) + ") : ")
    theme_a_modifier = librairie.recuperer_theme(librairie.retourne_themes()[int(choix_theme) - 1][0])
    separation()

    print("Questions du thème " + librairie.retourne_themes()[int(choix_theme) - 1][0])
    indice = 1
    questions_theme = list(theme_a_modifier.retourne_question_theme().keys())
    for question in questions_theme:
        print("    ", indice, ". ", question)
        indice += 1

    question_a_supprimer = input("Choisir la question à supprimer (entre 1 et " + str(indice - 1) + ") : ")
    separation()

    while True:
        validation_question = input("Etes-vous sur de vouloir supprimer la question '" + questions_theme[
            int(question_a_supprimer) - 1] + "' ? (oui ou non) : ")
        try:
            if validation_question == "oui" or validation_question == "non":
                break
            else:
                print("Les seules réponses acceptées sont 'oui' et 'non'.")
        except:
            print("Les seules réponses acceptées sont 'oui' et 'non'.")

    if validation_question == "oui":
        theme_a_modifier.suppression_question(questions_theme[int(question_a_supprimer) - 1])
        print("\nLa question '" + questions_theme[int(question_a_supprimer) - 1] + "' a été supprimée !")

    else:
        print("\nAnnulation. Aucune question n'a été supprimée.")

    separation()
    modifier()


def modifier():
    """
    Permet au joueur de modifier l'application en ajoutant/supprimant des thèmes/questions.
    """
    print("Menu > Modifier :")
    print("    1. Ajouter un thème")
    print("    2. Ajouter des questions")
    print("    3. Supprimer un thème")
    print("    4. Supprimer des questions")
    print("    5. Revenir en arrière")
    print("")
    mode = input("Choisir une option (1, 2, 3, 4 ou 5) : ")
    separation()
    # clear

    if mode == "1":
        ajouter_theme()
    elif mode == "2":
        ajouter_questions()
    elif mode == "3":
        supprimer_theme()
    elif mode == "4":
        supprimer_questions()
    else:
        menu()


def quitter():
    """
    Permet de fermer le programme. Si on veut le relancer, il faudra l'exécuter à nouveau.
    """
    print("Au revoir ", joueur.nom, ".\n")
    print("Application fermée.")


def menu():
    """
    Affiche les différentes options dans le menu et appelle la fonction selon le choix du joueur.
    """
    print("Menu :")
    print("    1. Jouer")
    print("    2. Modifier")
    print("    3. Quitter")
    print("")
    mode = input("Choisir une option (1, 2 ou 3) : ")
    separation()
    # clear

    if mode == "1":
        jouer()
    elif mode == "2":
        modifier()
    elif mode == "3":
        quitter()


pseudo = input("Bonjour. Veuillez entrez votre pseudo : ")
joueur = Utilisateur(pseudo)


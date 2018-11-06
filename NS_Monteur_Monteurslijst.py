#Hier wordt het tekst bestand ingelezen
import NS_Monteur

infile = open("NS_Monteur_Monteurslijst","r")
lines = infile.readlines()
monteurs = list()
for line in lines:
    line = line.strip("\n")
    content = line.split("; ")
    monteur = NS_Monteur.monteur(content[0],content[1],content[2],content[3],content[4])
    monteurs.append(monteur)
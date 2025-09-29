import csv

def lire_csv(fichier):
    tableau = []
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            lecteur = csv.reader(f, delimiter=",")  # ou ";" selon ton fichier
            for ligne in lecteur:
                tableau.append(ligne)
        return tableau
    except FileNotFoundError:
        print(f"Erreur : le fichier {fichier} n'existe pas.")
        return []

def is_numeric_column(tableau, col_index):
    if col_index == 0:
        return False  # Ignorer la première colonne
    numeric_count = 0
    for row in tableau[1:]:
        if col_index < len(row) and row[col_index].strip():  # ignorer les cellules vides
            try:
                float(row[col_index])
                numeric_count += 1
            except ValueError:
                return False  # Si une valeur n'est pas numérique, la colonne ne l'est pas

    return numeric_count > 0  # Au moins une valeur numérique trouvée

def find_index(header, subject_name):
    for subject_index in range(6, len(header)):
        if header[subject_index] == subject_name:
            return subject_index
    return -1


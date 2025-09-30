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

def get_course_name(index):
    course_names = [
        "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
        "Divination", "Muggle Studies", "Ancient Runes", "History of Magic",
        "Transfiguration", "Potions", "Care of Magical Creatures", "Charms",
        "Flying"
    ]
    if 0 <= index < len(course_names):
        return course_names[index]
    return "Unknown Course"

def get_houses(all_students, index_course):
    # Recuperer les notes
    gryffindor_origin = []
    slytherin_origin = []
    hufflepuff_origin = []
    ravenclaw_origin = []
    for student in all_students:
        house = student[1]
        note = student[index_course + 6]
        if note:
            try:
                if house == "Gryffindor":
                    gryffindor_origin.append(float(note))
                elif house == "Slytherin":
                    slytherin_origin.append(float(note))
                elif house == "Hufflepuff":
                    hufflepuff_origin.append(float(note))
                elif house == "Ravenclaw":
                    ravenclaw_origin.append(float(note))

            except ValueError:
                pass

    return gryffindor_origin, slytherin_origin, hufflepuff_origin, ravenclaw_origin

def get_house_xy(all_students, index1, index2):
    # Recuperer les notes des matieres pour le scatter plot par maison
    x_gryff, y_gryff = [], []
    x_huff, y_huff = [], []
    x_raven, y_raven = [], []
    x_slyth, y_slyth = [], []
    for student in all_students[1:]:
        note1 = student[index1]
        note2 = student[index2]
        house = student[1]
        if note1 and note2:
            try:
                score1 = float(note1)
                score2 = float(note2)
                
                if house == 'Gryffindor':
                    x_gryff.append(score1)
                    y_gryff.append(score2)
                elif house == 'Hufflepuff':
                    x_huff.append(score1)
                    y_huff.append(score2)
                elif house == 'Ravenclaw':
                    x_raven.append(score1)
                    y_raven.append(score2)
                elif house == 'Slytherin':
                    x_slyth.append(score1)
                    y_slyth.append(score2)
            except ValueError:
                pass

    return x_gryff, y_gryff, x_huff, y_huff, x_raven, y_raven, x_slyth, y_slyth

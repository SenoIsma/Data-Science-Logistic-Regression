import sys
import csv
import matplotlib.pyplot as plt

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

def mean(tableau, col_index, house):
    total = 0
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        if (house == row[1] or house is None) and row[col_index].strip():
            total += float(row[col_index])
            count += 1
        else:
            continue
    return total / count if count > 0 else 0

def std(tableau, col_index, house):
    m = mean(tableau, col_index, house)
    total = 0
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        if (house == row[1] or house is None) and row[col_index].strip():
            val = float(row[col_index])
            total += (val - m) ** 2
            count += 1
        else:
            continue
    variance = total / count if count > 0 else 0
    return variance ** 0.5

# def mean(tableau, col_index):
#     total = 0
#     count = 0
#     for row in tableau[1:]:  # Ignorer l'en-tête
#         try:
#             total += float(row[col_index])
#             count += 1
#         except (ValueError, IndexError):
#             continue
#     return total / count if count > 0 else 0

# def std(tableau, col_index):
#     m = mean(tableau, col_index)
#     total = 0
#     count = 0
#     for row in tableau[1:]:  # Ignorer l'en-tête
#         try:
#             val = float(row[col_index])
#             total += (val - m) ** 2
#             count += 1
#         except (ValueError, IndexError):
#             continue
#     variance = total / count if count > 0 else 0
#     return variance ** 0.5

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <fichier>")
        return

    fichier = sys.argv[1]  # le premier argument après le script
    data = lire_csv(fichier)

    labels = ["", "Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
    results = [[label] for label in labels]  # transforme chaque label en sous-liste

    for col_index in range(len(data[0])):  # pour chaque cours on cherche l'écart-type
        if is_numeric_column(data, col_index):
            results[0].append(data[0][col_index])
            for house in range(0, 4):
                results[house + 1].append(std(data, col_index, labels[house + 1]))

    house = 0
    diff = [None] * 4
    for col_index in range(1, len(results[0])):
        print(col_index)
        diff[house] =  std(results, col_index, None)
    for col_index in range(len(data[0])):  # pour chaque colonne
        if is_numeric_column(data, col_index):
            results[0].append(data[0][col_index])
            gryffindor_scores = [float(row[col_index]) for row in data[1:]
                                if row[1] == "Gryffindor" and row[col_index].strip()]
            ravenclaw_scores = [float(row[col_index]) for row in data[1:]
                                if row[1] == "Ravenclaw" and row[col_index].strip()]
            hufflepuff_scores = [float(row[col_index]) for row in data[1:]
                                if row[1] == "Hufflepuff" and row[col_index].strip()]
            slytherin_scores = [float(row[col_index]) for row in data[1:]
                                if row[1] == "Slytherin" and row[col_index].strip()]

    for row in results:
        print(row)
    # print("Gryffindor:", gryffindor_scores)
    # print("Ravenclaw:", ravenclaw_scores)
    # print("Hufflepuff:", hufflepuff_scores)
    # print("Slytherin:", slytherin_scores)
    
    plt.hist(gryffindor_scores, bins=20, alpha=0.7, label="Gryffindor")
    plt.hist(ravenclaw_scores, bins=20, alpha=0.7, label="Ravenclaw")
    plt.hist(hufflepuff_scores, bins=20, alpha=0.7, label="Hufflepuff")
    plt.hist(slytherin_scores, bins=20, alpha=0.7, label="Slytherin")
    plt.legend()
    plt.title("Histogramme des écarts-types par maison")
    plt.xlabel("Valeurs")
    plt.ylabel("Ecarts-types")
    # plt.show()

    return 0

if __name__ == "__main__":
    main()

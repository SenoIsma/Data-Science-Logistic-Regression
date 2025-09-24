import sys
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

def count(tableau, col_index):
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            float(row[col_index])
            count += 1
        except (ValueError, IndexError):
            continue
    return count

def mean(tableau, col_index):
    total = 0
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            total += float(row[col_index])
            count += 1
        except (ValueError, IndexError):
            continue
    return total / count if count > 0 else 0

def std(tableau, col_index):
    m = mean(tableau, col_index)
    total = 0
    count = 0
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            total += (val - m) ** 2
            count += 1
        except (ValueError, IndexError):
            continue
    variance = total / count if count > 0 else 0
    return variance ** 0.5

def min(tableau, col_index):
    minimum = float('inf')
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            if val < minimum:
                minimum = val
        except (ValueError, IndexError):
            continue
    return minimum if minimum != float('inf') else None

def max(tableau, col_index):
    maximum = float('-inf')
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            if val > maximum:
                maximum = val
        except (ValueError, IndexError):
            continue
    return maximum if maximum != float('-inf') else None

def percentile(tableau, col_index, percent):
    values = []
    for row in tableau[1:]:  # Ignorer l'en-tête
        try:
            val = float(row[col_index])
            values.append(val)
        except (ValueError, IndexError):
            continue
    if not values:
        return None
    values.sort()
    if percent == 0:
        return values[0]
    if percent == 100:
        return values[-1]
    k = (len(values)-1) * (percent/100)
    f = int(k)
    c = k - f
    if f + 1 < len(values):
        return values[f] + c * (values[f + 1] - values[f])
    else:
        return values[f]

def print_formatted_table(results):
    if not results or not results[0]:
        return
    
    # Calculer la largeur optimale pour chaque colonne
    col_widths = []
    
    for col_idx in range(len(results[0])):
        max_width = 0
        
        for row_idx in range(len(results)):
            if col_idx < len(results[row_idx]):
                cell_content = str(results[row_idx][col_idx])
                # Pour les nombres, formatter avec 6 décimales pour calculer la largeur
                if row_idx > 0 and isinstance(results[row_idx][col_idx], (int, float)):
                    cell_content = f"{results[row_idx][col_idx]:.6f}"
                max_width = max_width if max_width > len(cell_content) else len(cell_content)
        
        # Largeur minimale de 12 caractères pour les colonnes numériques
        if col_idx > 0:
            max_width = max_width if max_width > 12 else 12
        else:
            max_width = max_width if max_width > 8 else 8  # Pour la première colonne (labels)
        
        col_widths.append(max_width)
    
    # Afficher chaque ligne avec l'espacement correct
    for row_idx, row in enumerate(results):
        formatted_cells = []
        
        for col_idx, cell in enumerate(row):
            if col_idx == 0:  # Première colonne (labels) - alignement à gauche
                formatted_cells.append(f"{str(cell):<{col_widths[col_idx]}}")
            else:  # Colonnes numériques - alignement à droite
                if isinstance(cell, (int, float)):
                    formatted_cells.append(f"{cell:>{col_widths[col_idx]}.6f}")
                else:
                    formatted_cells.append(f"{str(cell):>{col_widths[col_idx]}}")
        
        print(" ".join(formatted_cells))

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <fichier>")
        return

    fichier = sys.argv[1]  # le premier argument après le script
    data = lire_csv(fichier)

    labels = ["", "Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
    results = [[label] for label in labels]  # transforme chaque label en sous-liste

    for col_index in range(len(data[0])):  # pour chaque colonne
        if is_numeric_column(data, col_index):
            results[0].append(data[0][col_index])
            results[1].append(f"{count(data, col_index):.6f}")
            results[2].append(mean(data, col_index))
            results[3].append(std(data, col_index))
            results[4].append(min(data, col_index))
            results[5].append(percentile(data, col_index, 25))
            results[6].append(percentile(data, col_index, 50))
            results[7].append(percentile(data, col_index, 75))
            results[8].append(max(data, col_index))

    # for row in results:
    #     print(row)

    print_formatted_table(results)

    return 0


if __name__ == "__main__":
    main()

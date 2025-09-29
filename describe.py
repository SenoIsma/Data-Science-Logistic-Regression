import utils, maths, sys

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
        print("Usage: python describe.py <file.csv>")
        return

    fichier = sys.argv[1]  # le premier argument après le script
    data = utils.lire_csv(fichier)

    labels = ["", "Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
    results = [[label] for label in labels]  # transforme chaque label en sous-liste

    for col_index in range(len(data[0])):  # pour chaque colonne
        if utils.is_numeric_column(data, col_index):
            results[0].append(data[0][col_index])
            results[1].append(f"{maths.count(data, col_index):.6f}")
            results[2].append(maths.mean(data, col_index))
            results[3].append(maths.std(data, col_index))
            results[4].append(maths.min(data, col_index))
            results[5].append(maths.percentile(data, col_index, 25))
            results[6].append(maths.percentile(data, col_index, 50))
            results[7].append(maths.percentile(data, col_index, 75))
            results[8].append(maths.max(data, col_index))

    print_formatted_table(results)

    return 0


if __name__ == "__main__":
    main()

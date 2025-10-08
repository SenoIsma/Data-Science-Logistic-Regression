import matplotlib.pyplot as plt
import utils, histogram, scatter_plot

def wrap_label(label, max_len=15):
    # Coupe le nom des features en plusieurs lignes si trop long
    words = label.split()
    lines = []
    current = ""
    for word in words:
        if len(current + " " + word) > max_len:
            lines.append(current)
            current = word
        else:
            if current:
                current += " " + word
            else:
                current = word
    if current:
        lines.append(current)
    return "\n".join(lines)

def main():
    all_students = utils.lire_csv("./datasets/dataset_train.csv")
    if not all_students:
        print("Error reading the CSV file.")
        return 1

    # Créer la figure avec plus d'espace
    fig, axes = plt.subplots(13, 13, figsize=(20, 20))
    
    # Créer les subplots
    for i in range(6, 19):
        for j in range(6, 19):
            ax = axes[i-6, j-6]
            
            if i == j:
                # Diagonale : histogrammes
                histogram.histogram_plot(all_students, i - 6, ax=ax)
            else:
                # Hors diagonale : scatter plots
                x_gryff, y_gryff, x_huff, y_huff, x_raven, y_raven, x_slyth, y_slyth = utils.get_house_xy(all_students, i, j)
                scatter_plot.scatter_plot(x_gryff, y_gryff, x_huff, y_huff, x_raven, y_raven, x_slyth, y_slyth, ax=ax)
            
            # Labels uniquement sur les bords
            if i == 18:  # Dernière ligne : labels en bas
                xlabel = wrap_label(utils.get_course_name(j - 6), max_len=15)
                ax.set_xlabel(xlabel, fontsize=7, rotation=45, ha='right')
            else:
                ax.set_xlabel("")
            
            if j == 6:  # Première colonne : labels à gauche
                ylabel = wrap_label(utils.get_course_name(i - 6), max_len=15)
                ax.set_ylabel(ylabel, fontsize=7, rotation=0, ha='right', va='center')
            else:
                ax.set_ylabel("")
            
            # Réduire la taille des ticks (= graduations)
            ax.tick_params(axis='both', which='both', labelsize=5, length=2)
            ax.grid(True, linestyle=':', linewidth=0.3, alpha=0.3)
    
    # Légende - positionnée en dehors de la zone des graphiques
    handles, labels = axes[0, 0].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, 
                  loc='lower left',           # Position de base
                  fontsize=9, 
                  bbox_to_anchor=(0., 0.),  # Positionné dans le coin
                  framealpha=0.95,            # Fond légèrement transparent
                  edgecolor='black',          # Bordure noire
                  fancybox=True)              # Coins arrondis
    
    # Titre principal
    plt.suptitle("Pair Plot of Student Grades by Hogwarts Course", 
                fontsize=18, fontweight='bold', y=0.995)
    
    # Ajuster les espacements pour laisser de la place aux labels
    plt.subplots_adjust(
        hspace=0.35,    # Espace vertical entre subplots
        wspace=0.35,    # Espace horizontal entre subplots
        left=0.08,      # Marge gauche (pour les labels Y)
        right=0.98,     # Marge droite
        top=0.97,       # Marge haute (pour le titre)
        bottom=0.08     # Marge basse (pour les labels X)
    )
    
    plt.show()
    return 0

if __name__ == "__main__":
    main()
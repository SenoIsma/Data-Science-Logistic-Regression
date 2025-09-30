import matplotlib.pyplot as plt
import sys
import utils
import maths

def scatter_plot(x_gryff, y_gryff, x_huff, y_huff, x_raven, y_raven, x_slyth, y_slyth, ax=None):
    if ax is None:
        ax = plt
    if ax is plt:
        plt.scatter(x_gryff, y_gryff, color='red', label='Gryffindor', alpha=0.6)
        plt.scatter(x_huff, y_huff, color='gold', label='Hufflepuff', alpha=0.6)
        plt.scatter(x_raven, y_raven, color='blue', label='Ravenclaw', alpha=0.6)
        plt.scatter(x_slyth, y_slyth, color='green', label='Slytherin', alpha=0.6)
        return plt
    else:
        ax.scatter(x_gryff, y_gryff, color='red', label='Gryffindor', alpha=0.5, s=1)
        ax.scatter(x_huff, y_huff, color='gold', label='Hufflepuff', alpha=0.5, s=1)
        ax.scatter(x_raven, y_raven, color='blue', label='Ravenclaw', alpha=0.5, s=1)
        ax.scatter(x_slyth, y_slyth, color='green', label='Slytherin', alpha=0.5, s=1)
        return ax

def main():
    if len(sys.argv) < 2:
        print("Usage: python scatter_plot.py <file.csv>")
        return
    file = sys.argv[1]
    all_students = utils.lire_csv(file)

    # Boucler sur chaque paire de matière
    corr_coef = []

    for course in range(6, len(all_students[0]) - 1):
        for other_course in range(course + 1, len(all_students[0])):
            if all_students[0][course] and all_students[0][other_course]:
                course_name = all_students[0][course]
                other_course_name = all_students[0][other_course]

                course_notes = []
                other_course_notes = []
                for student in all_students[1:]:
                    note = student[course]
                    other_note = student[other_course]
                    if note and other_note:
                        try:
                            course_notes.append(float(note))
                            other_course_notes.append(float(other_note))
                        except ValueError:
                            pass

                if len(course_notes) > 1 and len(other_course_notes) > 1:
                    coef = maths.calculate_correlation_coefficient(course_notes, other_course_notes)
                    corr_coef.append((course_name, other_course_name, coef))
    
    # Trouver la paire avec le coefficient de corrélation le plus élevé
    highest = 0

    for course1, course2, coef in corr_coef:
        if abs(coef) > abs(highest):
            highest = coef
            best_pair = (course1, course2)
    print(f"Highest correlation is between {best_pair[0]} and {best_pair[1]}: {highest:.4f}")

    # Recuperer les notes des matieres pour le scatter plot par maison
    for course1, course2, coef in corr_coef:
        if (course1 == best_pair[0] and course2 == best_pair[1]):
            x_gryff, y_gryff, x_huff, y_huff, x_raven, y_raven, x_slyth, y_slyth = \
            utils.get_house_xy(all_students, utils.find_index(all_students[0], best_pair[0]), 
                               utils.find_index(all_students[0], best_pair[1]))
            break

    plt = scatter_plot(x_gryff, y_gryff, x_huff, y_huff, x_raven, y_raven, x_slyth, y_slyth)

    plt.title(f'Scatter Plot between {best_pair[0]} and {best_pair[1]}')
    plt.xlabel(best_pair[0])
    plt.ylabel(best_pair[1])
    plt.legend()
    plt.show()

    return 0

if __name__ == "__main__":
    main()
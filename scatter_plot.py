import matplotlib.pyplot as plt
import sys
import utils
import maths

def main():
    if len(sys.argv) < 2:
        print("Usage: python describe.py <file.csv>")
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
            x_gryff, y_gryff = [], []
            x_huff, y_huff = [], []
            x_raven, y_raven = [], []
            x_slyth, y_slyth = [], []
            for student in all_students[1:]:
                note1 = student[utils.find_index(all_students[0], best_pair[0])]
                note2 = student[utils.find_index(all_students[0], best_pair[1])]
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
            break

    # Créer le scatter plot
    plt.scatter(x_gryff, y_gryff, color='red', label='Gryffindor', alpha=0.6)
    plt.scatter(x_huff, y_huff, color='gold', label='Hufflepuff', alpha=0.6)
    plt.scatter(x_raven, y_raven, color='blue', label='Ravenclaw', alpha=0.6)
    plt.scatter(x_slyth, y_slyth, color='green', label='Slytherin', alpha=0.6)
    plt.title(f'Scatter Plot between {best_pair[0]} and {best_pair[1]}')
    plt.xlabel(best_pair[0])
    plt.ylabel(best_pair[1])
    plt.legend()
    plt.show()

    return 0

if __name__ == "__main__":
    main()
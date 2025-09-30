import matplotlib.pyplot as plt
import sys, utils, maths

def histogram_plot(all_students, index_course, ax=None):
    gryffindor_origin, slytherin_origin, hufflepuff_origin, ravenclaw_origin = utils.get_houses(all_students, index_course)
    if ax is None:
        ax = plt
    # Construire l'histogramme
    if ax is plt:
        plt.hist(ravenclaw_origin, bins=20, alpha=0.7, label="Ravenclaw")
        plt.hist(hufflepuff_origin, bins=20, alpha=0.7, label="Hufflepuff") 
        plt.hist(gryffindor_origin, bins=20, alpha=0.7, label="Gryffindor")
        plt.hist(slytherin_origin, bins=20, alpha=0.7, label="Slytherin")
        return plt
    else:
        ax.hist(ravenclaw_origin, bins=20, alpha=0.7, label="Ravenclaw")
        ax.hist(hufflepuff_origin, bins=20, alpha=0.7, label="Hufflepuff") 
        ax.hist(gryffindor_origin, bins=20, alpha=0.7, label="Gryffindor")
        ax.hist(slytherin_origin, bins=20, alpha=0.7, label="Slytherin")
        return ax

def main():
    if len(sys.argv) < 2:
        print("Usage: python describe.py <file.csv>")
        return
    file = sys.argv[1]
    all_students = utils.lire_csv(file)

    # Calculer le minimum global sur toutes les matières
    global_min = float('inf')
    header = all_students[0]

    for subject_index in range(6, len(header)):
        if header[subject_index]:
            for student in all_students:
                note = student[subject_index]
                if note:
                    try:
                        global_min = min(global_min, float(note))
                    except ValueError:
                        pass

    # Pour chaque matiere, calculer le coefficient de variation
    all_cv = []
    for subject_index in range(6, len(header)):
        if header[subject_index]:
            gryffindor_notes = []
            slytherin_notes = []
            hufflepuff_notes = []
            ravenclaw_notes = []

            # Recuperer les notes par maison
            for student in all_students:
                house = student[1]
                note = student[subject_index]
                if note:
                    try:
                        if house == "Gryffindor":
                            gryffindor_notes.append(float(note))
                        elif house == "Slytherin":
                            slytherin_notes.append(float(note))
                        elif house == "Hufflepuff":
                            hufflepuff_notes.append(float(note))
                        elif house == "Ravenclaw":
                            ravenclaw_notes.append(float(note))

                    except ValueError:
                        pass

            # Normalisation avec le minimum global
            gryffindor_notes = maths.normalize_positive(gryffindor_notes, global_min)
            slytherin_notes = maths.normalize_positive(slytherin_notes, global_min)
            hufflepuff_notes = maths.normalize_positive(hufflepuff_notes, global_min)
            ravenclaw_notes = maths.normalize_positive(ravenclaw_notes, global_min)

            # Coefficient de Variation
            averages = [
                maths.calculate_average(gryffindor_notes),
                maths.calculate_average(slytherin_notes),
                maths.calculate_average(hufflepuff_notes),
                maths.calculate_average(ravenclaw_notes)
            ]
            std = maths.calculate_std(averages)
            if maths.calculate_average(averages) == 0 :
                print("division par 0")
            cv = (std / maths.calculate_average(averages)) * 100
            print(cv)
            all_cv.append(cv)

    min_cv = min(all_cv)
    min_index = all_cv.index(min_cv)

    # Retrouver le nom de la matière
    subject_names = []
    for subject_index in range(6, len(header)):
        if header[subject_index]:
            subject_names.append(header[subject_index])

    most_homogeneous = subject_names[min_index]

    print(f"🏆 MOST HOMOGENEOUS COURSE: {most_homogeneous}")
    print(f"📊 COEFFICIENT OF VARIATION: {min_cv:.2f}%")

    plt = histogram_plot(all_students, min_index)
    plt.title(f"Distribution of grades - {most_homogeneous}")
    plt.xlabel("GRADES")
    plt.ylabel("NUMBER OF STUDENTS")
    plt.legend()
    plt.show()
    return 0

if __name__ == "__main__":
    main()